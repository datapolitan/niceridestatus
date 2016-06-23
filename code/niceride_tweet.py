'''
A script to provide aggregate stats for the past hour
'''

import psycopg2
from pgconnect import pgconnect

from twython import Twython, TwythonError
from keys import keys

db = pgconnect['db']
user = pgconnect['user']
host = pgconnect['host']


def tweet_status():
    #prep for tweet
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_TOKEN_SECRET = keys['access_token_secret']
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    #query data for last hour
    con = psycopg2.connect(database=db, user=user, host=host, port=5432)
    cur = con.cursor()

    cur.execute(open("/home/ec2-user/niceridestatus/code/select_hour_stats.sql").read())
    q = cur.fetchall()
    r_list = []
    for el in q[0]:
        r_list.append(el)

    status_text = "In the past hour, there were an avg %s #NiceRideMN bikes avail in #Minneapolis, %s in #StPaul, and %s elsewhere" % ("{:,.0f}".format(r_list[0]), "{:,.0f}".format(r_list[1]), "{:,.0f}".format(r_list[2]))

    try:
        # print status_text
        twitter.update_status(status=status_text)
    except TwythonError as e:
        print "failed to tweet"
        print e
        pass


def main():
    tweet_status()

if __name__ == "__main__":
    main()
