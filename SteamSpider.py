from scrapy.crawler import CrawlerProcess
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

    wishListsURL = []
    for url in url_account:
        splitting = url.split('/')
        user = splitting[-1]
        user_type = splitting[-2]
        wishListsURL.append(f'https://store.steampowered.com/wishlist/{user_type}/{user}/wishlistdata/?p=0')

    return wishListsURL


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
        df.to_parquet(f'parquets/{filename}.parquet')


process = CrawlerProcess()
process.crawl(SteamSpider, users=communityUsers)
process.start()
