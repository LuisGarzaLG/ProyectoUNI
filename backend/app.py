from flask import Flask, request, jsonify
import subprocess
import tempfile
import json

app = Flask(__name__)

@app.route('/simular', methods=['POST'])
def simular():
    datos = request.get_json()

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_json:
        json.dump(datos, temp_json)
        temp_json.flush()

        resultado = subprocess.run(
            ['python3', 'simulador.py', temp_json.name],
            capture_output=True,
            text=True
        )

        if resultado.returncode != 0:
            return jsonify({'error': 'Error al ejecutar simulación'}), 500

        output = json.loads(resultado.stdout)
        return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
