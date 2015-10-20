'''
Retrieve station locations from the xml and update the database table.
To be run daily in a cron job when the other script isn't running.
'''

import xmltodict # have to install
import requests

import datetime

import psycopg2
from pgconnect import pgconnect

url = "https://secure.niceridemn.org/data2/bikeStations.xml"
r = requests.get(url)

stations = xmltodict.parse(r.content)

db = pgconnect['db']
user = pgconnect['user']
host = pgconnect['host']

con = psycopg2.connect(database=db, user=user, host=host, port=5432)
cur = con.cursor()

#drop table and recreate 
cur.execute(open("/home/ec2-user/niceridestatus/code/create_id_loc.sql").read())
con.commit()

sql = "INSERT INTO niceride_mn.id_loc(id,geom,created_at) VALUES (%s,ST_SetSRID(ST_MakePoint(%s,%s),4326),%s)"
for station in stations['stations']['station']:
    now = datetime.datetime.now()
    cur.execute(sql,(station['id'], station['long'],station['lat'],now))
con.commit()

con.close()
