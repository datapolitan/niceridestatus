A Twitter bot tweeting a summary of available [Nice Ride](https://www.niceridemn.org/) bikes in the Twin Cities. See the result [here](https://twitter.com/NiceRideDocks).

[`code/niceridestatus.py`](https://github.com/datapolitan/niceridestatus/blob/master/code/niceridestatus.py) runs in a cron job firing every 10 minutes to parse the [dock status](https://api-core.niceridemn.org/gbfs/en/station_status.json) and update the database with the most recent count of available bikes by city.

[`code/niceride_tweet.py`](https://github.com/datapolitan/niceridestatus/blob/master/code/niceride_tweet.py) runs in a cron job firing every hour to calculate the average and [tweet](https://twitter.com/NiceRideDocks) it out to the world.

[`code/niceride_analysis.py`](https://github.com/datapolitan/niceridestatus/blob/master/code/niceride_analysis.py) runs in a cron job firing 1 minute after midnight to provide a rollup of the previous 24 hours and update the Twitter feed.

[`code/update_station_loc.py`](https://github.com/datapolitan/niceridestatus/blob/master/code/update_station_loc.py) runs in a cron job firing once a week to update the station locations to pick up any new stations and their location around the Twin Cities.

20160622 Update: The code has been updated to use the JSON version of the status rather than the old XML file.