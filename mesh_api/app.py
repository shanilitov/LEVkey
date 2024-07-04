from flask import Flask, request, jsonify
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import meshtastic
from meshtastic.serial_interface import SerialInterface
import logging
from pubsub import pub
from messages import decrypt_message, encrypt_message, load_key_table

app = Flask(__name__)

# הגדרת רמת הלוגים ל-Debug כדי לראות את כל ההודעות
logging.basicConfig(level=logging.DEBUG)

interface = None
received_messages = []
'''
# יצירת טבלת מפתחות בגודל 1000
key_table = [os.urandom(32) for _ in range(1000)]

def encrypt_message(message):
    # בחירת מפתח רנדומלי מהטבלה
    key_index = os.urandom(1)[0] % 1000
    key = key_table[key_index]
    iv = os.urandom(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = iv + encryptor.update(message.encode()) + encryptor.finalize()
    # הוספת אינדקס המפתח המוצפן בתחילת ההודעה
    return key_index.to_bytes(2, byteorder='big') + encrypted_message

def decrypt_message(encrypted_message):
    key_index = int.from_bytes(encrypted_message[:2], byteorder='big')
    key = key_table[key_index]
    iv = encrypted_message[2:18]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message[18:]) + decryptor.finalize()
    return decrypted_message.decode()
'''
def on_receive(packet, interface):
    global received_messages
    try:
        encrypted_payload = packet['decoded']['payload']

        # המרה של ה-payload לגרסת בינארית במידה והיא מיוצגת כמחרוזת הקסה
        if isinstance(encrypted_payload, str):
            encrypted_payload = bytes.fromhex(encrypted_payload)

        key_table = load_key_table()
        decrypted_message = decrypt_message(encrypted_payload, key_table)
        logging.debug(f"Received and decrypted message: {decrypted_message}")
        received_messages.append(decrypted_message.decode('utf-8', errors='ignore'))  # ננסה לפענח ל-UTF-8 אך נתעלם משגיאות
    except Exception as e:
        logging.error(f"Error handling received message: {e}")





# הרשמה לאירוע שמאזין להודעות שמגיעות מהרדיו
def setup_meshtastic_listener():
    global interface
    try:
        interface = SerialInterface(devPath="COM26")  # לשנות לפי השם של החיבור הטורי המקומי...
        # interface.gotResponse = on_receive  # הוספת האירוע של קבלת הודעה
        # interface.start()  # התחלת קריאה לממשק
        pub.subscribe(on_receive, "meshtastic.receive")
        logging.debug("Meshtastic interface setup successfully")
    except Exception as e:
        logging.error(f"Error setting up Meshtastic interface: {e}")

# קריאה לפונקציה להתחלת הממשק
setup_meshtastic_listener()

@app.route('/connect', methods=['POST'])
def connect():
    global interface
    try:
        if not interface:
            setup_meshtastic_listener()  # אם אין חיבור קיים, התחל מחדש את הממשק
        logging.debug("Connected to mesh network")
        return jsonify({"status": "connected"}), 200
    except Exception as e:
        logging.error(f"Error connecting to mesh network: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/disconnect', methods=['POST'])
def disconnect():
    global interface
    if interface:
        interface.close()
        interface = None
        logging.debug("Disconnected from mesh network")
        return jsonify({"status": "disconnected"}), 200
    else:
        logging.error("No active connection to disconnect")
        return jsonify({"status": "error", "message": "No active connection"}), 400

@app.route('/send_message', methods=['POST'])
def send_message():
    global interface
    if not interface:
        logging.error("Not connected to mesh network")
        return jsonify({"status": "error", "message": "Not connected"}), 400

    data = request.get_json()
    logging.debug(f"Received POST request to /send_message with data: {data}")

    message = data.get("message")
    if not message:
        logging.error("No message provided in request")
        return jsonify({"status": "error", "message": "No message provided"}), 400

    try:
        key_table = load_key_table()  # לוודא שטבלת המפתחות נטענת
        encrypted_message = encrypt_message(message, key_table)
        logging.debug(f"Encrypted message: {encrypted_message}")

        interface.sendText(encrypted_message.hex())  # המרה למחרוזת הקסה
        logging.debug("Message sent to mesh network")
        return jsonify({"status": "message sent"}), 200
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/get_messages', methods=['GET'])
def get_messages():
    global received_messages
    return jsonify({"messages": received_messages}), 200

@app.route('/get_locations', methods=['GET'])
def get_locations():
    global interface
    if not interface:
        logging.error("Not connected to mesh network")
        return jsonify({"status": "error", "message": "Not connected"}), 400

    try:
        nodes = interface.nodes
        locations = [{"id": node.id, "latitude": node.latitude, "longitude": node.longitude} for node in nodes.values()]
        logging.debug(f"Retrieved node locations: {locations}")
        return jsonify({"locations": locations}), 200
    except Exception as e:
        logging.error(f"Error getting locations: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
