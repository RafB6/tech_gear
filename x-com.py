#from objects_functions import get_id
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import sqlite3

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("display/main_page.html")

def connect_to_database():
    conn = sqlite3.connect('gear.db')
    conn.row_factory = sqlite3.Row
    return conn

#GET DATA
def get_Data():
    conn = connect_to_database()
    cursor = conn.execute("SELECT * FROM gear")
    rows = cursor.fetchall()
    conn.close()
    gear_data = [dict(row) for row in rows]
    return gear_data
gear_data = get_Data()

#TRANSFERING JSON DATA TO DATABASE
#conn = sqlite3.connect('gear.db')
#cursor = conn.cursor()
#for product in gear_data:
#    cursor.execute(f''' 
#    INSERT INTO gear (type, brand, model, price, rating) VALUES (?,?,?,?,?)
#    ''', (product["type"], product["brand"], product["model"], product["price"], product["rating"]))
#conn.commit()
#conn.close()

@app.route("/add_gear", methods=["GET", "POST"])
def add_gear():
    #Get users values from form
    if request.method == "POST":
        gearType = request.form.get("type")
        model = request.form.get("model")
        brand = request.form.get("brand")
        price = float(request.form.get("price"))


        '''[OLD, SWITCHED TO CLIENT-SIDE VALIDATION]'''
        #Handle empty strings  
        #if len(model) == 0 or len(brand) == 0:
        #    return "Error: detected empty field(s)"
        #
        #try:
        #    price = float(request.form.get("price"))
        #except (TypeError, ValueError):
        #    return "Error: Price must be a number", 400
        '''-----------------------------------------'''
        
        
        conn = connect_to_database()
        cursor = conn.cursor()
        #Insert new product to database
        cursor.execute(f"INSERT INTO gear (type, brand, model, price, rating) VALUES (?,?,?,?,?)", (gearType, brand, model, price, 0))
        conn.commit()
        conn.close()
        #Update current 'gear_data'
        gear_data = get_Data()

        return redirect(url_for("gear"))
    else:
        return render_template("display/add_gear.html")

@app.route("/gear")
def gear():
    gear_data = get_Data()
    return render_template("display/get_gear.html", gear_data = gear_data)

@app.route("/get_gear", methods=["GET"])
def get_gear():
    #get arguments from user
    sort_by = request.args.get('sort_by', 'id')
    reverse = request.args.get('reverse', 'normal')
    query = request.args.get('query', 'default')
    #check for reverse, its value is crucial determine if implementation of sorting algorithm is necessary
    rev = (reverse == "reverse")

    query_gear = []
    #Look for items according to user's input
    if query != "default" and len(query) > 0 and query is not None:
        for elem in gear_data:
            if elem not in query_gear:
                #Check if any sort category contains user's query
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
