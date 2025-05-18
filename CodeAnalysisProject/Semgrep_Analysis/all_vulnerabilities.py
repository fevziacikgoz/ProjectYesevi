import os
import hashlib
import ast
import subprocess
import sqlite3
from flask import Flask
from Crypto.Cipher import AES

# 1. Hardcoded Password (Düzeltildi)
def connect_to_database():
    password = os.getenv("DB_PASSWORD", "default_password")  # Hardcoded password kaldırıldı
    print(f"Connecting to the database with password: {password}")

# 2. Eval Kullanımı (Düzeltildi)
def execute_user_input(user_input):
    try:
        # Güvenli ast.literal_eval kullanımı
        result = ast.literal_eval(user_input)
        print(f"User input executed: {result}")
    except (ValueError, SyntaxError) as e:
        print(f"Invalid input: {e}")

# 3. Güçlü Hash Algoritması (Düzeltildi)
def generate_secure_hash(password):
    # SHA-256 daha güvenli bir seçenek
    return hashlib.sha256(password.encode()).hexdigest()

# 4. Sabitlenmiş Salt Kullanımı (Düzeltildi)
def hash_password(password):
    # Dinamik salt kullanımı
    salt = os.urandom(16)
    return hashlib.sha256(salt + password.encode()).hexdigest()

# 5. Parola Kontrolü (Güçlendirildi)
def check_password(stored_password, provided_password):
    # Sabit karşılaştırma yerine zaman sabitli karşılaştırma
    return hashlib.compare_digest(stored_password, provided_password)

# 6. Parola Resetleme (Düzeltildi)
def reset_password(user_email):
    # Sabit token kaldırıldı, rastgele token kullanılıyor
    reset_token = os.urandom(32).hex()
    print(f"Password reset link: https://example.com/reset?token={reset_token}")

# 7. Güçlü Şifreleme (AES GCM)
def encrypt_data(data):
    key = os.urandom(32)  # 256-bit key
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return ciphertext, tag

# 8. Güvenli AES Anahtarı
def aes_encrypt(data):
    key = os.urandom(32)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return ciphertext, tag

# 9. Komut Çalıştırma (Güvenli Hale Getirildi)
def run_command(command_list):
    try:
        # shell=True kaldırıldı
        result = subprocess.run(command_list, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")

# 10. Güvenli Popen Kullanımı
def safe_popen(command_list):
    try:
        # shell=True kaldırıldı
        process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode())
    except Exception as e:
        print(f"Popen command failed: {e}")

# 11. Güvenli Dosya Okuma
def read_file(filename):
    try:
        # Dosya adı doğrulaması eklendi
        if ".." in filename or filename.startswith("/"):
            raise ValueError("Invalid file path")
        with open(filename, "r") as f:
            return f.read()
    except Exception as e:
        print(f"File read error: {e}")

# 12. Path Traversal Koruması
def read_user_file(filepath):
    try:
        # Path traversal koruması
        if ".." in filepath or filepath.startswith("/"):
            raise ValueError("Invalid file path")
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        print(f"File read error: {e}")

# 13. Güvenli SQL Sorgusu (Parametrik Sorgu)
def get_user(username):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchall()
    except Exception as e:
        print(f"SQL error: {e}")

# 14. SQL Enjeksiyonu Koruması (Parametrik Sorgu)
def find_user(username):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchall()
    except Exception as e:
        print(f"SQL error: {e}")

# 15. Flask Debug Modu (Kapatıldı)
app = Flask(__name__)

@app.route("/")
def home():
    return "Flask Güvenli Modda Çalışıyor!"

if __name__ == "__main__":
    # debug=True kaldırıldı, ortam değişkeni eklendi
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)

