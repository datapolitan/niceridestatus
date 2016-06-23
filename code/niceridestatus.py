'''
Script to tweet the status of docks

'''

import requests
import collections
import datetime

import psycopg2
from pgconnect import pgconnect

db = pgconnect['db']
user = pgconnect['user']
host = pgconnect['host']


def get_id_city():
    '''
    Get the city for each dock status_id and populate the id_city_dict
    '''
    icd = collections.defaultdict(str)
    con = psycopg2.connect(database=db, user=user, host=host, port=5432)
    cur = con.cursor()
    cur.execute(open("/home/ec2-user/niceridestatus/code/select_id_city.sql").read())
    q = cur.fetchall()
    for row in q:
        icd[str(row[0])] = row[1]
    con.close()
    return icd


def get_nr_dock(id_city_dict):
    '''
    Get the station status and parse into a dictionary counting available bikes by city
    '''
    url = 'https://api-core.niceridemn.org/gbfs/en/station_status.json'
    stations = requests.get(url)
    city_dict = collections.defaultdict(int)
    city_dict['execution_time'] = datetime.datetime.fromtimestamp(float(stations.json()['last_updated']))
    for station in stations.json()['data']['stations']:
        if station['is_installed'] == 1 and station['is_renting'] == 1 and station['is_returning'] == 1:
            city_dict[id_city_dict[station['station_id']]] += int(station['num_bikes_available'])
    return city_dict


def write_to_table(city_dict):
    '''
    Write number of available bikes by city to the database table
    '''
    city_vals = [city_dict['execution_time'], city_dict['Minneapolis'], city_dict['Saint Paul'], city_dict['Falcon Heights'], city_dict['Golden Valley'], city_dict['Fort Snelling']]

    con = psycopg2.connect(database=db, user=user, host=host, port=5432)
    cur = con.cursor()
    sql = "INSERT INTO niceride_mn.nr_city_stats (execution_time, minneapolis, st_paul, falcon_heights, golden_valley, fort_snelling) VALUES (%s,%s,%s,%s,%s,%s)"
    cur.execute(sql, tuple(city_vals))
    con.commit()
    con.close()
    return


def main():
    icd = get_id_city()
    city_dict = get_nr_dock(icd)
    write_to_table(city_dict)

if __name__ == "__main__":
    main()
