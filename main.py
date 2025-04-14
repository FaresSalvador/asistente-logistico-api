from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby5PGub1SJtHZxRYUdHQHc_KbzHCTTd7emuzAF4FwhRSCx7mDN2K9Pwut7R_Q00BPIQ/exec"

@app.route('/consultar', methods=['GET'])
def consultar():
    try:
        # Obtenemos los parámetros que el usuario envía
        params = request.args.to_dict()

        # Llamamos al Apps Script con esos parámetros
        response = requests.get(APPS_SCRIPT_URL, params=params)
        data = response.json()

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
