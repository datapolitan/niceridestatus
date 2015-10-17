'''
Retrieve station locations from the xml and update the database table.
To be run daily in a cron job when the other script isn't running.
'''

import xmltodict # have to load
import requests

url = "https://secure.niceridemn.org/data2/bikeStations.xml"