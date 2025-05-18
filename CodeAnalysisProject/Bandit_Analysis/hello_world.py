import os
import hashlib
import ast
import subprocess
from flask import Flask

# 1. Hardcoded Password - Güvenli Hali
def connect_to_database():
    # Password'ü hardcode etmek yerine çevresel değişkenlerden alalım
    password = os.getenv("DB_PASSWORD", "default_password")
    print(f"Connecting to the database with password: {password}")

# 2. Eval Kullanımı - Güvenli Hali
def execute_user_input(user_input):
    # eval yerine ast.literal_eval kullanarak güvenliği artırdık
    try:
        result = ast.literal_eval(user_input)
        print(f"User input executed: {result}")
    except (ValueError, SyntaxError) as e:
        print(f"Invalid input: {e}")

# 3. MD5 Hash Kullanımı - Güvenli Hali
def generate_hash(password):
    # SHA-256 daha güvenli bir seçenek
    return hashlib.sha256(password.encode()).hexdigest()

# 4. Komut Çalıştırma - En Güvenli Hali
def run_command(command_list):
    # Komutları sadece liste olarak al, shell=False
    if isinstance(command_list, list) and all(isinstance(arg, str) for arg in command_list):
        try:
            result = subprocess.run(command_list, check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
    else:
        print("Invalid command input. Must be a list of strings.")

# 5. Flask Debug Modu - Güvenli Hali
app = Flask(__name__)

@app.route("/")
def home():
    return "Flask Güvenli Modda Çalışıyor!"

if __name__ == "__main__":
    # debug=True kaldırıldı
    app.run()