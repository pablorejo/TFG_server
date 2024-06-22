# app.py
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/admin')
def hello_world():
    return 'Hello, Admin!'

@app.route('/admin/sync')
def sync_files():
    try:
        response = requests.post('http://inferency_motor:8000/sync')
        if response.status_code == 200:
            return jsonify({"sync": "success"})
        else:
            return jsonify({"sync": "failed", "error": response.text}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"sync": "failed", "exception": str(e)}), 500
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
    

