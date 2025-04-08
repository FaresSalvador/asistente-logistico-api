from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Carga la data desde el archivo una vez
with open('datos.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)

@app.route("/consultar", methods=["GET"])
def consultar():
    # Filtros desde la URL
    semana = request.args.get("semana")
    eta = request.args.get("eta")
    naviera = request.args.get("naviera")
    buque = request.args.get("buque")
    
    # Filtrar por parámetros opcionales
    datos_filtrados = datos

    if semana:
        datos_filtrados = [d for d in datos_filtrados if str(d.get("Semana", "")).zfill(2) == str(semana).zfill(2)]
    if eta:
        datos_filtrados = [d for d in datos_filtrados if d.get("ETA", "").startswith(eta)]
    if naviera:
        datos_filtrados = [d for d in datos_filtrados if naviera.lower() in d.get("NAVIERA", "").lower()]
    if buque:
        datos_filtrados = [d for d in datos_filtrados if buque.lower() in d.get("VESSEL - VOYAGE", "").lower()]

    # Agrupar por ETA, NAVIERA y VESSEL
    resumen = {}
    for item in datos_filtrados:
        clave = (item.get("ETA", ""), item.get("NAVIERA", ""), item.get("VESSEL - VOYAGE", ""))
        if clave not in resumen:
            resumen[clave] = set()
        resumen[clave].add(item.get("Contenedor", ""))

    resultado = []
    for clave, contenedores in resumen.items():
        resultado.append({
            "ETA": clave[0],
            "Naviera": clave[1],
            "Buque": clave[2],
            "Contenedores": len(contenedores)
        })

    return jsonify(resultado)
