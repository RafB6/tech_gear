from flask import Flask, render_template, request, redirect, jsonify, g
import json
import sqlite3

app = Flask(__name__)
app.config["DATABASE"] = "users.db"

with open("item_data.json", "r") as data_file:
    gear_data = json.load(data_file) 

def database_connection():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception = None):
    db = g.pop("db", None)
    if db is not None:
        db.close()



@app.route("/")
def main():
    return render_template("display/main_page.html")

@app.route("/users")
def get_users():
    db = database_connection()
    cursor = db.execute("SELECT * FROM users")
    users = cursor.fetchall()
    close_db()
    return {"users": [dict(row) for row in users]}

@app.route("/gear")
def gear():
    return render_template("display/get_gear.html", gear_data = gear_data)

@app.route("/get_gear")
def get_gear():
    #return JSON to browser
    return jsonify(gear_data)

@app.route("/login")
def login():
    return render_template("display/login.html")

if __name__ == '__main__':
    app.run(debug=True)
