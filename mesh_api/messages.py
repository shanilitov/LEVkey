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
    # בחירת אינדקס מפתח אקראי
    index = os.urandom(1)[0] % len(key_table)
    key = key_table[index]
    iv = os.urandom(16)  # וקטור אתחול (IV) אקראי
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return f"{index:04d}".encode() + iv + ciphertext

# פונקצית פענוח
def decrypt_message(encrypted_message, key_table):
    index = int(encrypted_message[:4].decode())
    key = key_table[index]
    iv = encrypted_message[4:20]
    ciphertext = encrypted_message[20:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()
