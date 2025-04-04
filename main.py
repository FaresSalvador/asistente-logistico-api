from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "🚛 Asistente Logístico API funcionando"

@app.route('/recibir', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    with open("datos_recibidos.json", "w") as archivo:
        json.dump(data, archivo, indent=4)
    return jsonify({"mensaje": "Datos recibidos correctamente ✅"}), 200

@app.route('/consultar', methods=['GET'])
def consultar_datos():
    try:
        with open("datos_recibidos.json", "r") as archivo:
            data = json.load(archivo)
    except FileNotFoundError:
        return jsonify({"mensaje": "Aún no se han recibido datos"}), 404

    # Filtros desde la URL
    semana = request.args.get('semana')
    naviera = request.args.get('naviera')
    buque = request.args.get('buque')

    filtrado = []

    for item in data:
        if naviera and naviera.lower() not in item.get('Naviera', '').lower():
            continue
        if buque and buque.lower() not in item.get('Buque', '').lower():
            continue
        if semana:
            eta_str = item.get('ETA')
            if eta_str:
                try:
                    eta = datetime.strptime(eta_str, "%Y-%m-%d")
                    semana_del_ano = eta.isocalendar().week
                    if int(semana) != semana_del_ano:
                        continue
                except:
                    continue
        filtrado.append(item)

    return jsonify(filtrado)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
