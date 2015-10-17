import xmltodict
import requests
import collections

import psycopg2
from pgconnect import pgconnect

import twython
from keys import keys

db = pgconnect['db']
user = pgconnect['user']
host = pgconnect['host']

#select the ids and city
def get_id_city():
    '''
    Get the city for each dock id and populate the id_city_dict
    '''
    icd = collections.defaultdict(str)
    con = psycopg2.connect(database=db, user=user, host=host, port=5432)
    cur = con.cursor()
    cur.execute(open("select_id_city.sql").read())
    q = cur.fetchall()
    for row in q:
        icd[str(row[0])] = row[1]
    con.close()
    return icd

def get_nr_dock(id_city_dict):
    url = "https://secure.niceridemn.org/data2/bikeStations.xml"
    r = requests.get(url)
    stations = xmltodict.parse(r.content)
    ####### process the stations json file
    totalDocks_sum = 0
    avail_bikes_sum = 0
    in_service_station_sum = 0
    #re-initialize the boro_dict to reset values
    city_dict = collections.defaultdict(int)
    for station in stations['stations']['station']:
        if station['installed'] == 'true' and station['locked'] == 'false' and station['public'] == 'true':
            totalDocks_sum += int(station['nbBikes']) + int(station['nbEmptyDocks'])
            avail_bikes_sum += int(station['nbBikes'])
            in_service_station_sum += 1
            city_dict[id_city_dict[station['id']]] += int(station['nbBikes'])
#    return city_dict

    ###### publish tweet
    tweet_status(city_dict)

def tweet_status(city_dict):
    other = city_dict['Falcon Heights'] + city_dict['Golden Valley'] + city_dict['Fort Snelling']
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_TOKEN_SECRET = keys['access_token_secret']
    twitter = twython.Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    
    status_text = "There are %s #NiceRideMN bikes avail in #Minneapolis, %s in #StPaul, and %s in #GoldenValley, #FalconHeights, & #FortSnelling"
    print status_text % ("{:,.0f}".format(city_dict['Minneapolis']),"{:,.0f}".format(city_dict['Saint Paul']),"{:,.0f}".format(other))

def main():
    # id_city_dict = collections.defaultdict(str)
    icd = get_id_city()
    get_nr_dock(icd)

if __name__ == "__main__":
    main()
