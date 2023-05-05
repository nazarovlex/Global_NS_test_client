import pymongo
from pymongo import errors
from flask import Flask, render_template
from flask import request
import requests
import re

# flask init
app = Flask(__name__, static_folder="static")


# mongo init
def mongo_init():
    db_client = pymongo.MongoClient("mongodb://mongo:mongo@mongo:27017/?authMechanism=DEFAULT")
    current_db = db_client["clients"]
    current_db.clients.create_index([('phone', 1)], unique=True)
    return current_db


# home page
@app.route('/')
@app.route("/home")
def home():
    return render_template("login.html", login_error=False)


# response page
@app.route('/response', methods=["POST"])
def result():
    # get params from form
    name = request.form.get("name")
    phone = request.form.get("phone")

    # check name & phone
    if name == "" or phone == "":
        return render_template("login.html", input_error=True)

    # phone number validation
    if not re.compile(r'^\+?\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}$').match(phone):
        return render_template("login.html", validation_error=True)

    # duplicates check
    current_db = mongo_init()
    web_collection = current_db["clients"]
    try:
        web_collection.insert_one({"name": name, "phone": phone})
    except errors.DuplicateKeyError:
        return render_template("login.html", login_error=True)

    # do request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer RLPUUOQAMIKSAB2PSGUECA'
    }
    data = {
        'stream_code': 'vv4uf',
        'client': {
            'phone': phone,
            'name': name,
        },
    }
    response = requests.post("https://order.drcash.sh/v1/order", headers=headers, json=data)

    # check status code
    if response.status_code != 200:
        return render_template("login.html", server_error=True)

    return render_template("response.html", response=response.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
