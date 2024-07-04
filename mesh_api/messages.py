import os
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# יצירת טבלת האש עם 1000 מפתחות
def generate_key_table(num_keys=1000, key_size=32):
    return [os.urandom(key_size) for _ in range(num_keys)]

# שמירת טבלת המפתחות בקובץ
def save_key_table(key_table, filename="key_table.json"):
    with open(filename, 'w') as f:
        json.dump([key.hex() for key in key_table], f)

# טעינת טבלת המפתחות מקובץ
def load_key_table(filename="key_table.json"):
    with open(filename, 'r') as f:
        keys_hex = json.load(f)
    return [bytes.fromhex(key) for key in keys_hex]

# פונקצית הצפנה
def encrypt_message(message, key_table):
    key_index = os.urandom(1)[0] % len(key_table)
    key = key_table[key_index]
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = iv + encryptor.update(message.encode()) + encryptor.finalize()
    return key_index.to_bytes(2, byteorder='big') + encrypted_message


# פונקצית פענוח
def decrypt_message(encrypted_message, key_table):
    key_index = int.from_bytes(encrypted_message[:2], byteorder='big')
    key = key_table[key_index]
    iv = encrypted_message[2:18]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message[18:]) + decryptor.finalize()
    return decrypted_message  # נשאיר את ההודעה כמחרוזת בינרית

