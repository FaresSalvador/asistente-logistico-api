from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

datos_globales = []

@app.route("/")
def home():
    return "🚛 Asistente Logístico API funcionando"

@app.route("/recibir", methods=["POST"])
def recibir():
    global datos_globales
    try:
        datos = request.get_json()
        if not isinstance(datos, list):
            return jsonify({"error": "La data no es una lista válida"}), 400
        datos_globales = datos
        return jsonify({"mensaje": "Datos recibidos correctamente ✅"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/consultar", methods=["GET"])
def consultar():
    global datos_globales
    if not datos_globales:
        return jsonify({"mensaje": "Aún no se han recibido datos"}), 404

    filtros = {
        "semana": request.args.get("semana"),
        "mes": request.args.get("mes"),
        "naviera": request.args.get("naviera"),
        "buque": request.args.get("buque"),
        "producto": request.args.get("producto"),
        "bl": request.args.get("bl"),
        "booking": request.args.get("booking"),
        "contenedor": request.args.get("contenedor"),
        "eta": request.args.get("eta"),
        "etd": request.args.get("etd")
    }

    def cumple_filtro(valor, filtro):
        return filtro.lower() in str(valor).lower()

    resultados = []
    for fila in datos_globales:
        incluir = True

        # Filtro por semana
        if filtros["semana"]:
            try:
                eta_str = fila.get("ETA", "")
                eta = datetime.strptime(eta_str[:10], "%Y-%m-%d")
                semana = eta.isocalendar()[1]
                if int(filtros["semana"]) != semana:
                    incluir = False
            except:
                incluir = False

        # Filtro por mes
        if filtros["mes"]:
            try:
                eta_str = fila.get("ETA", "")
                eta = datetime.strptime(eta_str[:10], "%Y-%m-%d")
                mes_nombre = eta.strftime("%B").lower()
                if filtros["mes"].lower() != mes_nombre:
                    incluir = False
            except:
                incluir = False

        # Filtros generales por campos
        for campo, nombre_real in [
            ("naviera", "Naviera"),
            ("buque", "VESSEL - VOYAGE"),
            ("producto", "Material"),
            ("bl", "BL"),
            ("booking", "Booking"),
            ("contenedor", "Contenedor"),
        ]:
            if filtros[campo] and not cumple_filtro(fila.get(nombre_real, ""), filtros[campo]):
                incluir = False

        # Filtros por ETA y ETD exactos
        for fecha_campo in ["eta", "etd"]:
            if filtros[fecha_campo]:
                try:
                    valor_fecha = fila.get(fecha_campo.upper(), "")[:10]
                    if valor_fecha != filtros[fecha_campo]:
                        incluir = False
                except:
                    incluir = False

        if incluir:
            resultados.append(fila)

    return jsonify(resultados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
