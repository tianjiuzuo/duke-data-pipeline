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
    
with open('app/static/js/bed-county-density.geojson') as g:
    data1 = json.load(g)
    
with open('app/static/js/victim-bed-density.geojson') as h:
    data2 = json.load(h)

conn= sqlite3.connect('app.db')
c = conn.cursor()

def total_victims_county():
   with sqlite3.connect("app.db") as conn:
       c = conn.cursor()
       c.execute("SELECT county, SUM(number_of_victims) FROM updates, users WHERE updates.user_id=users.id GROUP BY county")
    #    c.execute("SELECT county, SUM(number_of_victims) FROM updates)
       
       return c.fetchall()

victims_county = [[x[0], x[1]] for x in total_victims_county()]

def total_beds_county():
   with sqlite3.connect("app.db") as conn:
       c = conn.cursor()
       c.execute("SELECT county, SUM(capacity) FROM updates, users WHERE updates.user_id=users.id GROUP BY county")
       
       return c.fetchall()
   
beds_county = [[x[0], x[1]] for x in total_beds_county()]

# Compute density per county = total_num_victims / county_population
for i in victims_county:
    for j in county_pop_lst:
        if i[0] == j[0]:
            i[1] = "{:.4f}".format(i[1] / j[1])

for item in victims_county:
    for county in data['features']:
        if item[0] == county['properties']['name']:
            county['properties']['density'] = item[1]
            
# Compute beds (capacity) to county population = total_beds_co
for i in beds_county:
    for j in county_pop_lst:
        if i[0] == j[0]:
            i[1] = "{:.4f}".format(i[1] / j[1])

for item in beds_county:
    for county in data1['features']:
        if item[0] == county['properties']['name']:
            county['properties']['density'] = item[1]

# Compute number of victims to beds (county population)
victims_county = [[x[0], x[1]] for x in total_victims_county()]
beds_county = [[x[0], x[1]] for x in total_beds_county()]

for i in victims_county:
    for j in beds_county:
        if i[0] == j[0]:
            i[1] = "{:.4f}".format(i[1] / j[1])

for item in victims_county:
    for county in data2['features']:
        if item[0] == county['properties']['name']:
            county['properties']['density'] = item[1]

with open('app/static/js/counties.geojson', 'w') as f:
    json.dump(data, f)
    
with open('app/static/js/bed-county-density.geojson', 'w') as g:
    json.dump(data1, g)

with open('app/static/js/victim-bed-density.geojson', 'w') as h:
    json.dump(data2, h)