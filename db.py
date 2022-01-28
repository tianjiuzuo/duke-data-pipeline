import sqlite3
import json
import random
import requests
import json

# Get county population data
request_str = "https://api.census.gov/data/2019/pep/charagegroups?get=NAME,POP&for=county&in=state:37"
r = requests.get(request_str)
county_pop_lst = [(x[0].split(" County")[0], int(x[1])) for x in r.json()[1:]]
county_pop_lst.sort(key=lambda x:x[0])


with open('app/static/js/counties.geojson') as f:
    data = json.load(f)

conn= sqlite3.connect('app.db')
c = conn.cursor()

def total_victims_county():
   with sqlite3.connect("app.db") as conn:
       c = conn.cursor()
       c.execute("SELECT county, SUM(number_of_victims) FROM updates, users WHERE updates.user_id=users.id GROUP BY county")
       
       return c.fetchall()

victims_county = [[x[0], x[1]] for x in total_victims_county()]

# Compute density per county = total_num_victims / county_population
for i in victims_county:
    for j in county_pop_lst:
        if i[0] == j[0]:
            i[1] = "{:.4f}".format(i[1] / j[1])

for item in victims_county:
    for county in data['features']:
        if item[0] == county['properties']['name']:
            county['properties']['density'] = item[1]

with open('app/static/js/counties.geojson', 'w') as f:
    json.dump(data, f)
