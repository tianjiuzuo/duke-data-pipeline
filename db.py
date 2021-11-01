import sqlite3
import json
import random

with open('app/static/js/counties.geojson') as f:
    data = json.load(f)

for county in data['features']:
    county['properties']['density'] += random.randint(-20,20)

with open('app/static/js/counties.geojson', 'w') as f:
    json.dump(data, f)

#conn= sqlite3.connect('app.db')
#c = conn.cursor()
#def fetchData():
#    with sqlite3.connect("app.db") as conn:
#        c = conn.cursor()
#        c.execute("SELECT number_of_victims FROM updates")
#        return c.fetchall()[0][0]
#fetchData()
