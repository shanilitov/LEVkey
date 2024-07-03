from flask import Flask, request, jsonify
import serial
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import meshtastic
from meshtastic.serial_interface import SerialInterface
import os

app = Flask(__name__)

interface = None
encryption_key = os.urandom(32)  # Generate a random 256-bit encryption key


def encrypt_message(message):
    iv = os.urandom(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(encryption_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = iv + encryptor.update(message.encode()) + encryptor.finalize()
    return encrypted_message


def decrypt_message(encrypted_message):
    iv = encrypted_message[:16]
    cipher = Cipher(algorithms.AES(encryption_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message[16:]) + decryptor.finalize()
    return decrypted_message.decode()


@app.route('/connect', methods=['POST'])
def connect():
    global interface
    try:
        interface = SerialInterface(devPath="COM26")  # לשנות לפי השם של החיבור הטורי המקומי...
        return jsonify({"status": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/disconnect', methods=['POST'])
def disconnect():
    global interface
    if interface:
        interface.close()
        interface = None
        return jsonify({"status": "disconnected"}), 200
    else:
        return jsonify({"status": "error", "message": "No active connection"}), 400


@app.route('/send_message', methods=['POST'])
def send_message():
    global interface
    if not interface:
        return jsonify({"status": "error", "message": "Not connected"}), 400

    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"status": "error", "message": "No message provided"}), 400

    encrypted_message = encrypt_message(message)
    try:
        interface.sendData(encrypted_message)
        return jsonify({"status": "message sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/get_messages', methods=['GET'])
def get_messages():
    global interface
    if not interface:
        return jsonify({"status": "error", "message": "Not connected"}), 400

    try:
        messages = interface.getReceivedMessages()
        decrypted_messages = [decrypt_message(msg) for msg in messages]
        return jsonify({"messages": decrypted_messages}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/get_locations', methods=['GET'])
def get_locations():
    global interface
    if not interface:
        return jsonify({"status": "error", "message": "Not connected"}), 400

    try:
        nodes = interface.nodes
        locations = [{"id": node.id, "latitude": node.latitude, "longitude": node.longitude} for node in nodes.values()]
        return jsonify({"locations": locations}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000)
