#from objects_functions import get_id
from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import json
import sqlite3
from datetime import datetime

app = Flask(__name__)

def connect_to_database():
    conn = sqlite3.connect('gear.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/add_rating", methods=["POST"])
def add_rating():
    try:
        rating = int(request.form.get("rating"))
        comment = request.form.get("comment")
        prod_id = int(request.form.get("id"))
        conn = connect_to_database()
        cursor = conn.execute("INSERT INTO ratings (score, product_id, comment) VALUES (?,?,?)", (rating, prod_id, comment))
        conn.commit()
        return jsonify({"issuccess": True})
    except Exception as e:
        return jsonify({"error": str(e)})        

#CHECK IF A PRODUCT EXISTS
@app.route("/check_product")
def check_product():
    gear_data = get_Data()
    model = request.args.get("model", None).strip()
    brand = request.args.get("brand", None).strip()

    existing_product = None
    #look for matching product
    for product in gear_data:
        if product["model"] == model and product["brand"] == brand:
            existing_product = product
            break
    #make recongnizable pass codes
    if existing_product:
        return jsonify(existing_product)
    else:
        return jsonify({"doesExist": "No"})


#SET THEME COOKIE
@app.route("/setTheme", methods=['POST'])
def set_theme():
    data = request.get_json()
    theme = data.get('theme', 'light')
    response = make_response(jsonify(success=True))
    response.set_cookie('theme', theme)
    #SEND COOKIE TO FRONT-END
    return response

#GET DATA
def get_Data():
    conn = connect_to_database()
    cursor = conn.execute("SELECT gear.id, gear.type, gear.brand, gear.model, gear.price, AVG(ratings.score) AS score FROM gear LEFT JOIN ratings ON gear.id = ratings.product_id GROUP BY gear.id")
    rows = cursor.fetchall()
    conn.close()
    gear_data = []
    for row in rows:
        row = dict(row)
        if row["score"] == None:
            row["score"] = 0
        gear_data.append(row)
    return gear_data

@app.route("/")
# MAIN PAGE
def main():
    return render_template("display/main_page.html", current_year=datetime.now().year)


# GEAR LIST
@app.route("/gear")
def gear():
    theme = request.cookies.get("theme", "light")
    gear_data = get_Data()
    return render_template("display/get_gear.html", gear_data = gear_data, theme = theme)



# ADD FORM
@app.route("/add_gear", methods=["GET", "POST"])
def add_gear():
    gear_data = get_Data()
    theme = request.cookies.get("theme", "light")

    # HANDLE REQUEST (POST by default)
    if request.method == "POST":    
        gearCount = len(gear_data)
        #Get users values from form
        gearType = request.form.get("type")
        model = request.form.get("model")
        brand = request.form.get("brand")
        price = float(request.form.get("price"))
        formType = request.form.get("formType")
        #Connect to database
        conn = connect_to_database()
        cursor = conn.cursor()

        # HANDLE POST REQUEST
        if formType == "Add":
            #Insert new product to database
            try:
                cursor.execute("INSERT INTO gear (type, brand, model, price) VALUES (?,?,?,?)", (gearType, brand, model, price))
                conn.commit()
                conn.close()
                return redirect(url_for("gear"))
            except Exception as e:
                return str(e) + "INSERTING INTO", 500
        # HANDLE DELETE REQUEST
        elif formType == "Delete":
            for i in range(gearCount):
                product = gear_data[i]
                # find product to delete
                if product["brand"] == brand and product["model"] == model:
                    try:
                        # DELETE PRODUCT FROM BOTH TABLES
                        cursor.execute("DELETE FROM gear WHERE id=?", (product["id"],))
                        cursor.execute("DELETE FROM ratings WHERE product_id=?", (product["id"],))
                        conn.commit()
                        conn.close()
                        # UPDATE GEAR DATA
                        gear_data = get_Data()
                        return redirect(url_for("gear"))
                    except Exception as e:
                        return e, 500
        else:
            return "Unknown form type", 500
    # HANDLE RENDERING THE SITE
    else:
        return render_template("display/add_gear.html", theme=theme)


# SEARCHING ROUTE
@app.route("/get_gear", methods=["GET"])
def get_gear():
    gear_data = get_Data()
    #get arguments from user
    sort_by = request.args.get('sort_by', 'brand')
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
    
    #sort values
    if sort_by == "price" or sort_by == "score":
        sorted_gear = sorted(query_gear,key = lambda x: float(x[sort_by]),reverse=rev)
    else:
        sorted_gear = sorted(query_gear, key = lambda x: x[sort_by], reverse=rev)

    #return JSON to browser
    return jsonify(sorted_gear)


if __name__ == '__main__':
    app.run(debug=True)



#TRANSFERING JSON DATA TO DATABASE
#conn = sqlite3.connect('gear.db')
#cursor = conn.cursor()
#for product in gear_data:
#    cursor.execute(f''' 
#    INSERT INTO gear (type, brand, model, price, rating) VALUES (?,?,?,?,?)
#    ''', (product["type"], product["brand"], product["model"], product["price"], product["rating"]))
#conn.commit()
#conn.close()
