# app.py

from flask import Flask, request, jsonify
from simulador import correr_simulacion
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/simular', methods=['POST'])
def simular():
    params = request.json

    df = correr_simulacion(
        num_personas=params.get('num_personas', 100),
        tiempo_entre_llegadas=params.get('tiempo_entre_llegadas', 10),
        tiempo_simulacion=params.get('tiempo_simulacion', 1000),
        duracion_bn=tuple(params.get('duracion_bn', [1, 3])),
        duracion_color=tuple(params.get('duracion_color', [4, 10])),
        impresoras_bn=params.get('impresoras_bn', 1),
        impresoras_color=params.get('impresoras_color', 1)
    )

    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
