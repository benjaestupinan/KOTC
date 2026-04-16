import json
import os
import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

BIN_ID = "69e02a3236566621a8ba3b11"
API_KEY = "$2a$10$AhbCQtCSwmm/.5cmWoqs9O9LqiJlOq3ix4vK8s9AGnDPVv2B4xPNW"

BASE_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"


def load_data():
    headers = {"X-Master-Key": API_KEY}
    res = requests.get(BASE_URL, headers=headers)
    if res.status_code == 200:
        return res.json().get("record", {"names": [], "scores": {}})
    return {"names": [], "scores": {}}


def save_data(data):
    headers = {"X-Master-Key": API_KEY, "Content-Type": "application/json"}
    requests.put(BASE_URL, headers=headers, json=data)


@app.route("/api/data")
def get_data():
    return jsonify(load_data())


@app.route("/api/increment", methods=["POST"])
def increment():
    data = load_data()
    name = request.json.get("name")
    password = request.json.get("password")

    if password != "pepito123":
        return jsonify({"error": "Contraseña incorrecta"}), 401

    if name in data["scores"]:
        data["scores"][name] += 1
    else:
        data["scores"][name] = 1
        data["names"].append(name)

    save_data(data)
    return jsonify({"score": data["scores"][name]})


@app.route("/api/add", methods=["POST"])
def add_name():
    data = load_data()
    name = request.json.get("name")
    password = request.json.get("password")

    if password != "pepito123":
        return jsonify({"error": "Contraseña incorrecta"}), 401

    if not name:
        return jsonify({"error": "Nombre requerido"}), 400

    if name in data["names"]:
        return jsonify({"error": "Nombre ya existe"}), 400

    data["names"].append(name)
    data["scores"][name] = 0
    save_data(data)
    return jsonify({"success": True})


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)


# Vercel entrypoint
app = app
