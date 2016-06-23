'''
Script to tweet the status of docks

'''


import requests
import collections
import datetime

import psycopg2
from pgconnect import pgconnect

from twython import Twython, TwythonError
from keys import keys

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
    url = 'https://api-core.niceridemn.org/gbfs/en/station_status.json'
    stations = requests.get(url)
    city_dict = collections.defaultdict(int)
    city_dict['execution_time'] = datetime.datetime.fromtimestamp(float(stations.json()['last_updated']))
    for station in stations.json()['data']['stations']:
        if station['is_installed'] == 1 and station['is_renting'] == 1 and station['is_returning'] == 1:
            city_dict[id_city_dict[station['station_id']]] += int(station['num_bikes_available'])
    # return city_dict

    ###### publish tweet
    tweet_status(city_dict)


def write_to_table(city_vals):
    con = psycopg2.connect(database=db, user=user, host=host, port=5432)
    cur = con.cursor()
    sql = "INSERT INTO niceride_mn.nr_city_stats (execution_time, minneapolis, st_paul, falcon_heights, golden_valley, fort_snelling) VALUES (%s,%s,%s,%s,%s,%s)"
    cur.execute(sql, tuple(city_vals))
    con.commit()
    con.close()
    return


def tweet_status(city_dict):
    #insert values into table
    write_to_table([city_dict['execution_time'], city_dict['Minneapolis'], city_dict['Saint Paul'], city_dict['Falcon Heights'], city_dict['Golden Valley'], city_dict['Fort Snelling']])

    #prep for tweet
    other = city_dict['Falcon Heights'] + city_dict['Golden Valley'] + city_dict['Fort Snelling']
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_TOKEN_SECRET = keys['access_token_secret']
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    status_text = ''

    now = int(datetime.datetime.now().strftime('%M')[0])
    if now % 2 == 0:
        status_text = "%s #NiceRideMN bikes are avail in #Minneapolis, %s in #StPaul, and %s in #GoldenValley, #FalconHeights, & #FortSnelling" % ("{:,.0f}".format(city_dict['Minneapolis']), "{:,.0f}".format(city_dict['Saint Paul']), "{:,.0f}".format(other))
    else:
        status_text = "There are %s #NiceRideMN bikes avail in #Minneapolis, %s in #StPaul, and %s in #GoldenValley, #FalconHeights, & #FortSnelling." % ("{:,.0f}".format(city_dict['Minneapolis']), "{:,.0f}".format(city_dict['Saint Paul']), "{:,.0f}".format(other))

    try:
        twitter.update_status(status=status_text)
    except TwythonError as e:
        print "failed to tweet"
        print e
        pass


def main():
    # id_city_dict = collections.defaultdict(str)
    icd = get_id_city()
    get_nr_dock(icd)

if __name__ == "__main__":
    main()
