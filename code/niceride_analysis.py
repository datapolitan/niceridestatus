'''
Read results from database and create 24 hour graph of activity
'''

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime
import twython
import numpy as np
import os

import psycopg2
from pgconnect import pgconnect

from keys import keys

prefix = '/home/ec2-user/niceridestatus/code/'

def tweet_status(day):
    '''
    a function to tweet the input values
    '''
    #####authenticate the Twitter account
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_TOKEN_SECRET = keys['access_token_secret']
    twitter = twython.Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    #######

    ####Should add some length checking to tweet jik
    photo = open(prefix + day + '.png', 'rb')
    response = twitter.upload_media(media=photo)
    twitter.update_status(status='The past 24 hours of available #NiceRideMN bikes', media_ids=[response['media_id']])
    return

def main():
    db = pgconnect['db']
    user = pgconnect['user']
    host = pgconnect['host']

    con = psycopg2.connect(database=db, user=user, host=host, port=5432)
    cur = con.cursor()

    df = pd.read_sql_query(open(prefix + "summary_stats.sql").read(),con,index_col='hour_ex')
    df.columns = ['Minneapolis','Saint Paul','Golden Valley/Falcon Heights/Fort Snelling']

    ax = df.plot(figsize=(10,5),title="Available NiceRide Bikes for Past 24 hours")
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel("Number of Available NiceRide Bikes")
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start, end, 4))
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1))
    ax.grid('on')
    day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    plt.savefig(prefix + day + '.png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    tweet_status(day)

    #remove file after tweeted
    os.remove(prefix + day + '.png')

if __name__ == "__main__":
    main()