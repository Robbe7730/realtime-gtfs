import gtfs

gtfs.connect("mysql://delaymap:password@localhost:3306/DelayMap")
gtfs.from_url("https://sncb-opendata.hafas.de/gtfs/static/c21ac6758dd25af84cca5b707f3cb3de")