from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
api_url = "http://localhost:5000"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    response = requests.post(f"{api_url}/send_message", json={"message": message})
    return jsonify(response.json())

@app.route('/get_messages', methods=['GET'])
def get_messages():
    response = requests.get(f"{api_url}/get_messages")
    return jsonify(response.json())

@app.route('/get_locations', methods=['GET'])
def get_locations():
    response = requests.get(f"{api_url}/get_locations")
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5001)
