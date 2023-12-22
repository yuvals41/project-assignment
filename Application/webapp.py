from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
#Listening on route uselessfact
@app.route('/uselessfact')
def useless_fact():
    target_url = os.environ.get('USELESS_FACT_URL')
    if not target_url:
        return jsonify({"error": "USELESS_FACT_URL not set"}), 500

    response = requests.get(target_url)
    return jsonify(response.json())

#Listening on route funnyfact
@app.route('/funnyfact')
def funny_fact():
    target_url = os.environ.get('FUNNY_FACT_URL')
    if not target_url:
        return jsonify({"error": "FUNNY_FACT_URL not set"}), 500

    response = requests.get(target_url)
    return jsonify(response.json())

@app.route('/ready')
def ready():
    return 'healthy', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
