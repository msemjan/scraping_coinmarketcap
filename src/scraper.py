import datetime
import json
import requests
import pandas as pd
from math import nan
from bs4 import BeautifulSoup

# start and end date in format YYYYMMDD
now = datetime.datetime.now()

# The script scrapes values for last 365 days
start_date = (now - datetime.timedelta(days=-365)).strftime("%Y%m%d")
end_date   = now.strftime("%Y%m%d")

# path to savefile
savefile = './crypto.csv'

# Fetching data from the site
url = f"https://coinmarketcap.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content , 'html.parser')


coins = {}

data = soup.find("script", id="__NEXT_DATA__", type="application/json")
coin_data = json.loads(data.contents[0])
listings = coin_data["props"]["initialState"]["cryptocurrency"]["listingLatest"]["data"]

# Getting a dict of coin IDs and slugs
for listing in listings:
    coins[str(listing['id'])] = listing['slug']


# Saving things that I am interested in
mc = []
symbol = []
p = []
p1h = []
p24h = []
p7d = []
p30d = []
p90d = []
v = []
ts = []
t = []
vol24hpc = []
mc24hpc = []
fmc24hpc = []


# Fetching historical data
for i in coins:
    page = requests.get(f"https://coinmarketcap.com/currencies/{coins[i]}/historical-data/?start={start_date}&end={end_date}")
    soup = BeautifulSoup(page.content, "html.parser")
    data = soup.find("script", id="__NEXT_DATA__", type="application/json")
    if data is None:
        continue 
    historical_data = json.loads(data.contents[0])

    quotes = historical_data["props"]["initialState"]["cryptocurrency"]["quotes"]
    if quotes is None:
        continue

    # Saving things that I am interested in
    for quote in quotes:
        mc.append(quotes[quote]['mc'] if 'mc' in quotes[quote] else nan)
        symbol.append(quotes[quote]['symbol'] if 'symbol' in quotes[quote] else nan)
        p.append(quotes[quote]['p'] if 'p' in quotes[quote] else nan)
        p1h.append(quotes[quote]['p1h'] if 'p1h' in quotes[quote] else nan)
        p24h.append(quotes[quote]['p24h'] if 'p24h' in quotes[quote] else nan)
        p7d.append(quotes[quote]['p7d'] if 'p7d' in quotes[quote] else nan)
        p30d.append(quotes[quote]['p30d'] if 'p30d' in quotes[quote] else nan)
        p90d.append(quotes[quote]['p90d'] if 'p90d' in quotes[quote] else nan)
        v.append(quotes[quote]['v'] if 'v' in quotes[quote] else nan)
        t.append(quotes[quote]['t'] if 't' in quotes[quote] else nan)
        ts.append(quotes[quote]['ts'] if 'ts' in quotes[quote] else nan)
        vol24hpc.append(quotes[quote]['vol24hpc'] if 'vol24hpc' in quotes[quote] else nan)
        mc24hpc.append(quotes[quote]['mc24hpc'] if 'mc24hpc' in quotes[quote] else nan)
        fmc24hpc.append(quotes[quote]['fmc24hpc'] if 'fmc24hpc' in quotes[quote] else nan)

# Store data
df = pd.DataFrame(
        {
            "mc":           mc,
            "symbol":       symbol,
            "p":            p,
            "p1h":          p1h,                                      
            "p24h":         p24h,                     
            "p7d":          p7d,                     
            "p30d":         p30d,                     
            "p90d":         p90d,                     
            "v":            v,                     
            "ts":           ts,                     
            "t":            t,                     
            "vol24hpc":     vol24hpc,                     
            "mc24hpc":      mc24hpc,                     
            "fmc24hpc":     fmc24hpc                     
        })
df.to_csv(savefile, index=False)
