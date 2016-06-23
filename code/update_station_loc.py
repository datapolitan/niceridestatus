'''
Retrieve station locations from the xml and update the database table.
To be run daily in a cron job when the other script isn't running.
Updated to process the new JSON file
'''

import requests

import datetime

import psycopg2
from pgconnect import pgconnect

url = "https://api-core.niceridemn.org/gbfs/en/station_information.json"
stations = requests.get(url)


db = pgconnect['db']
user = pgconnect['user']
host = pgconnect['host']

con = psycopg2.connect(database=db, user=user, host=host, port=5432)
cur = con.cursor()

#drop table and recreate
cur.execute(open("/home/ec2-user/niceridestatus/code/create_id_loc.sql").read())
con.commit()

sql = "INSERT INTO niceride_mn.id_loc(station_id,geom,created_at) VALUES (%s,ST_SetSRID(ST_MakePoint(%s,%s),4326),%s)"
for station in stations.json()['data']['stations']:
    now = datetime.datetime.now()
    cur.execute(sql, (station['station_id'], station['lon'], station['lat'], now))
con.commit()

con.close()
