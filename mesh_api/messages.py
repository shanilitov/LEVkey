import os
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import logging


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
    encrypted_payload = key_index.to_bytes(1, byteorder='big') + encrypted_message
    logging.debug(f"Encrypted payload: {encrypted_payload.hex()}")
    return encrypted_payload


# פונקצית פענוח
def decrypt_message(encrypted_message, key_table):
    print(type(encrypted_message))
    key_index = encrypted_message[0]
    print(key_index)
    key = key_table[key_index]

    encrypted_message = encrypted_message[1:]
    iv = encrypted_message[:16]
    ciphertext = encrypted_message[16:]

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    a=decryptor.update(ciphertext)
    b=decryptor.finalize()
    decrypted_message= a+b
    # decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_message.decode('utf-8', errors='ignore')


a = encrypt_message("Hello", load_key_table())
b = decrypt_message(a, load_key_table())
print(b)
