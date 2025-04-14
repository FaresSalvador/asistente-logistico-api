from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/consultar", methods=["GET"])
def consultar():
    url = "https://script.google.com/macros/s/AKfycby5PGub1SJtHZxRYUdHQHc_KbzHCTTd7emuzAF4FwhRSCx7mDN2K9Pwut7R_Q00BPIQ/exec"
    params = request.args.to_dict()

    try:
        response = requests.get(url, params=params)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    from os import environ
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)))
