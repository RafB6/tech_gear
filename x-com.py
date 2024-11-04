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
    #get arguments from user
    sort_by = request.args.get('sort_by', 'id')
    reverse = request.args.get('reverse', 'normal')
    query = request.args.get('query', 'default')
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
