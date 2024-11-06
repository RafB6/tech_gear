from flask import Flask, render_template, request, redirect, jsonify
import json

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("display/main_page.html")

with open("item_data.json", "r") as data_file:
    gear_data = json.load(data_file)

@app.route("/gear")
def gear():
    return render_template("display/get_gear.html", gear_data = gear_data)

@app.route("/get_gear", methods=["GET"])
def get_gear():
    #return JSON to browser
    return jsonify(gear_data)

if __name__ == '__main__':
    app.run(debug=True)
