def generate_signal_input(nb_input, vals, nb_output):

    init = f"""
   constant output_size : INTEGER range 255 downto 0 := {nb_output};
   constant D_WIDTH : INTEGER := 8;
   constant RESET_N : STD_LOGIC := '1';

   signal RX : STD_LOGIC := '0';
   signal RX_BUSY : STD_LOGIC := '0';
   signal RX_ERROR : STD_LOGIC := '0';
   signal RX_DATA : STD_LOGIC_VECTOR(d_width-1 DOWNTO 0) := "00000000";
   signal TX : STD_LOGIC := '0';
   signal TX_BUSY : STD_LOGIC := '0';
   signal TX_ENABLE : STD_LOGIC := '0';
   signal TX_DATA : STD_LOGIC_VECTOR(d_width-1 DOWNTO 0) := "10000000";

   signal TRIGGER_TX_ENABLE : STD_LOGIC := '0';\n
   """

    # print(generate_signal_input(6, [8, 8, 8, 0, 0, 0]))
    prev = f"signal inputs : STD_LOGIC_VECTOR({nb_input*8-1} downto 0) := "

    formatted_values = '"' + "".join(f'{i:08b}' for i in vals) + '";\n'

    return init + prev + formatted_values


def generate_header():
    return """LIBRARY ieee;
USE ieee.std_logic_1164.all;

entity ProjectM1 is

port (
    CLOCK_50 : IN STD_LOGIC;
    GPIO_1 : OUT STD_LOGIC_VECTOR(5 downto 0);

    LEDR : OUT STD_LOGIC_VECTOR(7 downto 0)
);

end entity;
"""

def generate_uart_send(output_number, nb_total_neuron):

    acc = f"if (number_to_send=0) then TX_DATA <= output_n{nb_total_neuron-output_number+1};\n"

    for i in range(1, output_number):
        acc += f"\t\t\t\telsif (number_to_send={i}) then TX_DATA <= output_n{nb_total_neuron-output_number+i+1};\n"

    acc += "\t\t\t\tend if;"

    return acc

def generate_architecture(inputs, neuron_info_per_layer, output_number):

    nb_total_neuron = 0
    nb_inputs = len(inputs)

    acc_header = "architecture CLASSICAL of ProjectM1 is\n"
    acc_header += "\t" + generate_signal_input(nb_inputs, inputs, output_number) + "\n"

    acc_bottom = ""

    prev_layer = None

    for layer in neuron_info_per_layer:

        layer_wmatrix = layer["wmatrix"]
        bias = layer["bias"]

        for bias, n_weights in zip(bias, layer_wmatrix):

            nb_total_neuron += 1

            weights = '"' + "".join(map(lambda m: f"{m:08b}", n_weights)) + '";\n'

            acc_header += f"\tsignal weights_n{nb_total_neuron} : STD_LOGIC_VECTOR({len(n_weights)*8-1} downto 0) := {weights}"
            acc_header += f"\tsignal bias_n{nb_total_neuron} : INTEGER range 255 downto 0 := {bias};\n"
            acc_header += f'\tsignal output_n{nb_total_neuron} : STD_LOGIC_VECTOR(7 downto 0) := "00000000";\n\n'

            if (prev_layer==None):
                acc_bottom += f"""\t
    neuron{nb_total_neuron} : entity work.Neuron(Dynamic)
        generic map( input_number => {len(inputs)} )
        port map (
            inputs => inputs,
            weights => weights_n{nb_total_neuron},
            bias => bias_n{nb_total_neuron},
            output => output_n{nb_total_neuron}
        );\n"""

            else:
                n_inputs = "&".join(f"output_n{nb_total_neuron-i}" for i in range(len(prev_layer["bias"]), 0, -1))

                acc_bottom += f"""\t
    neuron{nb_total_neuron} : entity work.Neuron(Dynamic)
        generic map( input_number => {len(prev_layer["bias"])} )
        port map (
            inputs => {n_inputs},
            weights => weights_n{nb_total_neuron},
            bias => bias_n{nb_total_neuron},
            output => output_n{nb_total_neuron}
        );\n"""

        prev_layer = layer

    acc_header += "begin\n"

    if (output_number==1): acc_bottom += f"\n\t LEDR <= output_n{nb_total_neuron};\n"

    acc_bottom += f"""
    uart : entity work.UARTWrapper(logic)

        port map (
            clk      =>  CLOCK_50,
            reset_n  =>  RESET_N,
            tx_ena   =>  TX_ENABLE,
            tx_data  =>  TX_DATA,
            rx       =>  RX,
            rx_busy  =>  RX_BUSY,
            rx_error =>  RX_ERROR,
            rx_data  =>  RX_DATA,
            tx_busy  =>  TX_BUSY,
            tx       =>  TX
        );

	process (CLOCK_50)
		variable acc : INTEGER range 12500000 downto 0 := 0;
	begin
		if (rising_edge(CLOCK_50)) then
			if (acc=12500000) then
				TRIGGER_TX_ENABLE <= '1';
				acc := 0;
			else
				acc := acc+1;
				TRIGGER_TX_ENABLE <= '0';
			end if;
		end if;
	end process;

   TX_ENABLE <= TRIGGER_TX_ENABLE;

   process (TRIGGER_TX_ENABLE)

		variable number_to_send : integer range 255 downto 0 := 0;

	begin

		if (rising_edge(TRIGGER_TX_ENABLE)) then

			if (number_to_send=output_size) then
				number_to_send := 0;
				TX_DATA <= "00000000";
			else
            {generate_uart_send(output_number, nb_total_neuron)}
				number_to_send := number_to_send+1;
			end if;

		end if;

	end process;

	GPIO_1(5) <= TX;
"""

    acc_bottom += "end architecture;"

    return acc_header + acc_bottom


def generate_progam(inputs, neuron_info_per_layer, outputs_number, filename):


    to_write = generate_header() + generate_architecture(inputs, neuron_info_per_layer, outputs_number)

    if (filename==""): return to_write

    with open(filename, "w+") as f:
        f.write(to_write)
        return to_write

def parse_matrix(content):

    raw_value = eval(content)

    inputs = raw_value.pop(0)
    
    acc = [{"wmatrix":x, "bias":y} for x, y in zip(raw_value[0::2], raw_value[1::2])]
    return inputs, acc, len(acc[-1]["bias"])