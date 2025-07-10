from objects_functions import get_id
from flask import Flask, render_template, request, redirect, jsonify, redirect, url_for
import json

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("display/main_page.html")

with open("item_data.json", "r") as data_file:
    gear_data = json.load(data_file)

@app.route("/add_gear", methods=["GET", "POST"])
def add_gear():
    #Get users values from form
    if request.method == "POST":
        gearId = len(gear_data) + 1 #get incremented id number
        gearType = request.form.get("type")
        model = request.form.get("model")
        try:
            price = float(request.form.get("price"))
        except (TypeError, ValueError):
            return "Error: Price must be a number", 400
        newProduct = {
            "id": gearId,
            "type": gearType,
            "model": model,
            "price": price,
            "rating": 0
        }
        gear_data.append(newProduct)
        with open("item_data.json", "w") as data_file:
            json.dump(gear_data, data_file, indent=4)

        return redirect(url_for("gear"))
    else:
        return render_template("display/add_gear.html")

@app.route("/gear")
def gear():
    return render_template("display/get_gear.html", gear_data = gear_data)

@app.route("/get_gear", methods=["GET"])
def get_gear():
    #get arguments from user
    sort_by = request.args.get('sort_by', 'id')
    reverse = request.args.get('reverse', 'normal')
    query = request.args.get('query', 'default')
    #check for reverse, its value is crucial determine if implementation of sorting algorithm is necessary
    if reverse == "normal":
        rev = False
    else:
        rev = True

    query_gear = []
    if query != "default" and len(query) > 0 and query is not None:
        for elem in gear_data:
            if elem in query_gear:
                continue

            if query.lower() in str(elem["brand"]).lower() or query.lower() in str(elem["model"]).lower():
                query_gear.append(elem)
    else:
        query_gear = gear_data
    
    #print values
    if sort_by == "price":
        sorted_gear = sorted(query_gear,key = lambda x: float(x[sort_by]),reverse=rev)
    else:
        sorted_gear = sorted(query_gear, key = lambda x: x[sort_by], reverse=rev)

    #return JSON to browser
    return jsonify(sorted_gear)


if __name__ == '__main__':
    app.run(debug=True)
