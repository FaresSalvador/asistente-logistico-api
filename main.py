from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby5PGub1SJtHZxRYUdHQHc_KbzHCTTd7emuzAF4FwhRSCx7mDN2K9Pwut7R_Q00BPIQ/exec"

@app.route('/consultar', methods=['GET'])
def consultar():
    try:
        # Obtenemos todos los parámetros de la URL como diccionario
        params = request.args.to_dict()

        # Hacemos la petición al Apps Script con los mismos parámetros
        response = requests.get(APPS_SCRIPT_URL, params=params)

        # Convertimos la respuesta a JSON
        data = response.json()

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Configuración para que Render detecte el puerto correctamente
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
