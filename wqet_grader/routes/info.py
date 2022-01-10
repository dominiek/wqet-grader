
from flask import Blueprint, g, jsonify, redirect, request

app = Blueprint("info", __name__)

@app.route("/", methods=["GET"])
def info():
    return jsonify({"service": "wqet-grader"})
