from flask import Flask, request, jsonify
import serial
import meshtastic
from meshtastic.serial_interface import SerialInterface
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

app = Flask(__name__)
interface = None

def encrypt_message(key, plaintext):
    cipher = Cipher(algorithms.AES(key), modes.CFB(b'16byteIV1234567'), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return base64.b64encode(ciphertext).decode()

def decrypt_message(key, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CFB(b'16byteIV1234567'), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(base64.b64decode(ciphertext)) + decryptor.finalize()
    return plaintext.decode()

@app.route('/connect', methods=['POST'])
def connect():
    global interface
    try:
        interface = SerialInterface('COM25')  # עדכן את השם של ה-serial port לפי המערכת שלך
        return jsonify({'status': 'connected'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/disconnect', methods=['POST'])
def disconnect():
    global interface
    if interface:
        interface.close()
        interface = None
        return jsonify({'status': 'disconnected'})
    else:
        return jsonify({'status': 'error', 'message': 'Not connected'}), 500

@app.route('/send_message', methods=['POST'])
def send_message():
    global interface
    if not interface:
        return jsonify({'status': 'error', 'message': 'Not connected'}), 500

    data = request.json
    key = b'sixteen byte key'  # עדכן את המפתח לפי הצורך
    encrypted_message = encrypt_message(key, data['message'])

    try:
        interface.sendText(encrypted_message)
        return jsonify({'status': 'message sent'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_messages', methods=['GET'])
def get_messages():
    # אתה צריך להוסיף את הקוד הנכון כדי לקבל הודעות ממכשירי ה-LoRa שלך
    return jsonify([])

@app.route('/get_locations', methods=['GET'])
def get_locations():
    # אתה צריך להוסיף את הקוד הנכון כדי לקבל את המיקומים של המכשירים ברשת
    return jsonify([])

if __name__ == '__main__':
    app.run(port=5000)
