from scrapy.crawler import CrawlerProcess
from datetime import date
import json
import pandas as pd
import scrapy

communityUsers = ['https://steamcommunity.com/id/hnrqandreata',
                  'https://steamcommunity.com/profiles/76561198113335827']


def pricingRight(price):
    price = str(price)
    start = price[0:-2]
    end = price[-2:]
    return float(start + '.' + end)


def SplitAccount(url_account):
    """
    Simple function to convert url (perfil) to url (wishlist).

    Parameters
    ----------
    url_account : list
        List containing users url to profile on steam.

    Returns
    -------
    url_wishlist : list
        List containing wishlist url.
    """
    return \
        [
            f'https://store.steampowered.com/wishlist/{url.split("/")[-2]}/{url.split("/")[-1]}/wishlistdata/?p=0'
            for url in url_account
        ]


class SteamSpider(scrapy.Spider):

    name = 'spiderSteam'

    def __init__(self, users: list, **kwargs):
        super().__init__(**kwargs)
        self.users_url = SplitAccount(users)

    def start_requests(self):
        urls = self.users_url

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        wishDict = json.loads(response.body)
        tempList = []

        filename = str(response).split('/')[-3]

        for keys_id in wishDict.keys():
            # General Dict
            game = wishDict[keys_id]

            # Specific Dict
            name = game['name']
            reviews_total = int(game['reviews_total'].replace(',',''))
            reviews_percent = game['reviews_percent']
            release_string = game['release_string']

            id = 0
            discount_pct = 0
            price = .0

            # Subs Dict
            if game['subs']:
                subs = game['subs'][0]
                id = subs['id']
                discount_pct = subs['discount_pct']
                price = pricingRight(subs['price'])

            tempList.append([name, reviews_total, reviews_percent, release_string, id, discount_pct, price])

        columns = ['name', 'reviews_total', 'reviews_percent', 'release_string', 'id', 'discount_pct', 'price']
        df = pd.DataFrame(tempList, columns=columns)
        df.to_parquet(f'parquets/{filename}_{date.today()}.parquet')


process = CrawlerProcess()
process.crawl(SteamSpider, users=communityUsers)
process.start()
