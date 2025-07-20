# tech_gear
Hello!
This is a simple project that mimics a search-by-query feature like those found in popular e-commerce sites.

Features:
Search items by brand or model (user input)
Sort results by type, price, rating, or ID
Toggle between ascending and descending order
Client-side validation
Dark/Light Motive, remembered across the domain with cookies
Asynchronus duplicate-checking system (fetch, await) with minimizing the use of client's resources
Finished rating system that's using other table in db to storing scores, displaying data efficiently thanks to using LEFT JOIN
REST API technology
Add/Delete products

soon: Admin users


Tech Stack:
Flask, JavaScript, SQLITE3(used to be JSON, but sqlite is more efficient in this use-case), HTML/CSS, AJAX

How to run:
Install flask ("pip install flask")
Run app.py
Open http://localhost:5000