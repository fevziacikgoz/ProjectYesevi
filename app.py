from flask import Flask, jsonify, request

app = Flask(__name__)

users = {
    "admin": "1234"
}


@app.route("/", methods=["GET"])
def home():
    return "<h1>Login API Çalışıyor!</h1><p>Kullanabileceğiniz endpoint: /api/login (POST)</p>"


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify({"message": "Kullanıcı adı boş olamaz!"}), 400

    if not password:
        return jsonify({"message": "Parola boş olamaz!"}), 400

    if username in users and users[username] == password:
        return jsonify({"message": "Giriş Başarılı!"}), 200
    else:
        return jsonify({"message": "Hatalı kullanıcı adı veya parola!"}), 401


if __name__ == "__main__":
    app.run(port=5000, debug=True)