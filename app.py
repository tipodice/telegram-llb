import base64
import json
import time

from db import Database
from config import DB_FILE
from flask import Flask, render_template


app = Flask(__name__)
db = Database(DB_FILE)


@app.route("/api/<string:token>")
def api(token):
    decoded_token = base64.b64decode(token).decode()
    data = db.database.get(decoded_token)
    if data:
        return data
    return "data not found"


if __name__ == "__main__":
    app.run()
