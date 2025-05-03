from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

LICENSES = {
    "LynixOnline": {
        "expires": "2025-06-01 13:00",
        "status": "active"
    },
    "MyOtherServer": {
        "expires": "2025-12-31 23:59",
        "status": "revoked"
    }
}

@app.route("/verify", methods=["POST"])
def verify():
    data = request.json
    server = data.get("server")
    now = datetime.datetime.now()

    if server not in LICENSES:
        return jsonify({"status": "invalid"}), 403

    lic = LICENSES[server]

    if lic["status"] != "active":
        return jsonify({"status": "revoked"}), 403

    expires = datetime.datetime.strptime(lic["expires"], "%Y-%m-%d %H:%M")
    if now > expires:
        return jsonify({"status": "expired"}), 403

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
