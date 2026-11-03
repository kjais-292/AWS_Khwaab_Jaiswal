from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Submissions are kept in memory (enough to show the backend processing data)
submissions = []


@app.route("/")
def health():
    return jsonify({"status": "ok", "service": "flask-backend"})


@app.route("/submit", methods=["POST"])
def submit():
    # Accept JSON (from the Express server) or a normal HTML form post
    data = request.get_json(silent=True) or request.form

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    # Validation, same as the Flask assignment
    if not name or not email:
        return jsonify({"success": False, "error": "Name and Email are required."}), 400
    if "@" not in email:
        return jsonify({"success": False, "error": "Please enter a valid email."}), 400

    entry = {
        "id": len(submissions) + 1,
        "name": name.title(),
        "email": email.lower(),
        "message": message,
        "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    submissions.append(entry)
    print(f"Received submission: {entry}", flush=True)

    return jsonify({"success": True, "message": f"Thanks {entry['name']}, your data was received!", "data": entry}), 201


@app.route("/api/submissions")
def list_submissions():
    return jsonify(submissions)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
