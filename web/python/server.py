import main
from html_source_code import *
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return main_html_app

def go(content, path):
    inp, info, out = main.parse_matrix(content)

    return main.generate_progam(inp, info, out, path)


@app.route("/neuron", methods=['GET'])
def neuron(): return neuron_html_code

@app.route("/uart", methods=['GET'])
def uart(): return uart_html_code

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fichier' not in request.files:
        return "Aucun fichier n'a été envoyé."

    fichier = request.files['fichier']

    path = request.form["path"]

    if fichier.filename == '':
        return "Aucun fichier sélectionné."

    fichier.save("weight_matrixes")

    with open("weight_matrixes", 'r') as f:
        return code_html_app(go(f.read(), path))

if __name__ == '__main__':
    app.run(debug=True)
