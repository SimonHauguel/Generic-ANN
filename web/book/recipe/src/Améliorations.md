# Améliorations

## Changer les entrées et coefficients à la volée

La solution proposee ne permet pas de changer les matrices de poids ni les entrées à la volée. Cependant, c'est une tâche plutôt simple. Voilà une ébauche de stratégie :

1. Ajouter un flag qui viendra se lever quand l'instance UART lira un nouveau paquet de données.
2. Traiter le cas de changement d'entrées et de matrice de poids. Le premier etant beaucoup plus simple et frequents que le second. On peut imaginer spécifier ceci en UART par un premier paquet de bits (0 si entrées, 1 sinon).
3. Comme nous connaissons la taille de chaque élément à la compilation, il est facile de changer les coefficients, voir même gratuitement.
```vhdl
process (UART_NEW_DATA_FLAG)

    variable accumulator : STD_LOGIC_VECTOR(INPUTS_SIZE downto 0) := (other => '0');

begin

    if (rising_edge(UART_NEW_DATA_FLAG) and STATE_CHANGE_INPUTS='1') begin

        accumulator := accumulator(INPUTS_SIZE DOWNTO 7) & NEW_DATA_UART;
        inputs <= accumulator;

    end if;

end process;
```
Vous pouvez aussi attendre d'avoir reçu l'intégralité des paquets avant de changer les inputs/coefficients. Cela reduira la volatilité de la sortie.
Pour les matrices, il nous faudra changer sequentiellement chacun des coefficients, mais comme nous avons la possibilité d'hardcoder la solution, cela ne devrait pas poser de problèmes.

Note, tous ces changements devront se faire dans le fichier `main.py`.