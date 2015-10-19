A Twitter bot tweeting a summary of available [Nice Ride](https://www.niceridemn.org/) bikes in the Twin Cities. See the result [here](https://twitter.com/NiceRideDocks).

[`code/niceridestatus.py`](https://github.com/datapolitan/niceridestatus/blob/master/code/niceridestatus.py) runs in a cron job firing every 10 minutes to parse the [dock status](https://secure.niceridemn.org/data2/bikeStations.xml) and update the Twitter feed. 

[`code/niceride_analysis.py`](https://github.com/datapolitan/niceridestatus/blob/master/code/niceride_analysis.py) runs in a cron job firing 1 minute after midnight to provide a rollup of the previous 24 hours and update the Twitter feed.

[`code/update_station_loc.py`](https://github.com/datapolitan/niceridestatus/blob/master/code/update_station_loc.py) runs in a cron job firing once a week to update the station locations to pick up any new stations and their location around the Twin Cities.