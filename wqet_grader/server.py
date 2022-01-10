import logging
import os

from flask import Flask, g, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from .routes.grade import app as grade_routes
from .routes.info import app as info_routes

app = Flask(__name__)
CORS(app)

@app.errorhandler(Exception)
def handle_exception(error):
    logging.warn("Uncought error during API call: {}".format(str(error)))
    if isinstance(error, HTTPException):
        return (
            jsonify(
                {
                    "error": {
                        "code": error.code,
                        "name": error.name,
                        "message": error.description,
                    }
                }
            ),
            error.code,
        )
    else:
        return jsonify({"error": {"code": 500, "message": str(error)}})


app.register_blueprint(info_routes, url_prefix="/")
app.register_blueprint(grade_routes, url_prefix="/1")

if __name__ == "__main__":
    app.run(host="localhost", port=2400, debug=False, threaded=False)
