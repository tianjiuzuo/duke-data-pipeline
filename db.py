import sqlite3
import json
import random

with open('app/static/js/counties.geojson') as f:
    data = json.load(f)

conn= sqlite3.connect('app.db')
c = conn.cursor()

def fetchData():
   with sqlite3.connect("app.db") as conn:
       c = conn.cursor()
       c.execute("SELECT county, SUM(number_of_victims) FROM updates, users WHERE updates.user_id=users.id GROUP BY county")
       return c.fetchall()

new_data = fetchData()

for item in new_data:
    for county in data['features']:
        if item[0] == county['properties']['name']:
            county['properties']['density'] = item[1]

with open('app/static/js/counties.geojson', 'w') as f:
    json.dump(data, f)
