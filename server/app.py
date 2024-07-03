from flask import Flask, request, jsonify
import serial
import threading
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import meshtastic
from meshtastic.serial_interface import SerialInterface

app = Flask(__name__)
serial_port = None
meshtastic_interface = None
received_messages = []
locations = []
running = False

# המפתח להצפנה והפענוח
encryption_key = b'sixteen byte key'  # יש להחליף במפתח אמיתי באורך 16 בייטים

def encrypt_message(message, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message.encode('utf-8')) + encryptor.finalize()
    return iv + encrypted_message

def decrypt_message(encrypted_message, key):
    iv = encrypted_message[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message[16:]) + decryptor.finalize()
    return decrypted_message.decode('utf-8')

def on_receive(packet, interface):
    global received_messages, locations
    try:
        message = packet.get('payload').decode('utf-8')
        message = decrypt_message(message, encryption_key)
        print(f"Received message: {message}")
        if message.startswith("LOC:"):
            _, lat, lon = message.split(",")
            locations.append({"latitude": float(lat), "longitude": float(lon)})
        else:
            received_messages.append(message)
    except Exception as e:
        print(f"Receive error: {str(e)}")

def connect():
    global meshtastic_interface, running
    try:
        print("Attempting to open Meshtastic interface...")
        meshtastic_interface = SerialInterface('COM25')  # השתמש ב-COM port הנכון
        meshtastic_interface.onReceive = on_receive
        print("Meshtastic interface opened.")
        running = True
    except Exception as e:
        print(f"Connection error: {str(e)}")
        raise e

def disconnect():
    global meshtastic_interface, running
    try:
        if meshtastic_interface:
            running = False
            meshtastic_interface.close()
            meshtastic_interface = None
            print("Meshtastic interface closed.")
    except Exception as e:
        print(f"Disconnection error: {str(e)}")
        raise e

@app.route('/connect', methods=['POST'])
def api_connect():
    try:
        connect()
        return jsonify({"status": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/disconnect', methods=['POST'])
def api_disconnect():
    try:
        disconnect()
        return jsonify({"status": "disconnected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/send_message', methods=['POST'])
def send_message():
    if not meshtastic_interface:
        return jsonify({"status": "error", "message": "Not connected"}), 400
    try:
        data = request.json
        message = data.get('message')
        if not message:
            return jsonify({"status": "error", "message": "Message is required"}), 400
        encrypted_message = encrypt_message(message, encryption_key)
        meshtastic_interface.sendData(encrypted_message)
        return jsonify({"status": "message sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(received_messages), 200

@app.route('/get_locations', methods=['GET'])
def get_locations():
    return jsonify(locations), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
