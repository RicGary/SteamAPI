from graph import plotly_graph
from scrapy.crawler import CrawlerProcess
from dash import Dash, html, dcc
import json
import pandas as pd
import scrapy

app = Dash(__name__)
fig = []


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

    def __init__(self, users: list, account, **kwargs):
        super().__init__(**kwargs)
        self.accountTitle = account
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

            # Not used by the time
            reviews_total = int(game['reviews_total'].replace(',', ''))
            reviews_percent = game['reviews_percent']
            release_string = game['release_string']

            # Constants
            game_id = 0
            discount_pct = 0
            price = .0

            # Subs Dict
            if game['subs']:
                subs = game['subs'][0]
                discount_pct = subs['discount_pct']
                price = pricingRight(subs['price'])

                # Not used by the time
                game_id = subs['id']

                full_price = price / (1 - (discount_pct / 100))

                tempList.append(
                    [name, reviews_total, reviews_percent, release_string, game_id, discount_pct, price, full_price])

        columns = ['name',
                   'reviews_total',
                   'reviews_percent',
                   'release_string',
                   'id',
                   'discount_pct',
                   'price',
                   'full_price']
        df = pd.DataFrame(tempList, columns=columns)

        df_noSQL = df[['name', 'price', 'full_price']].sort_values('full_price')
        df_noSQL = df_noSQL[df_noSQL.full_price != 0].reset_index()

        fig.append(plotly_graph(self.accountTitle, df_noSQL))


# Process Start
def startProcess(account: str, user: str):
    users = [user]

    process = CrawlerProcess()
    process.crawl(
        SteamSpider,
        users=users,
        account=account
    )
    process.start()


if __name__ == '__main__':
    startProcess('crios', 'https://steamcommunity.com/profiles/76561198113335827')

    # print(fig)
    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),
        html.Div(children="""
                    Dash: A web application framework for your data."""),
        dcc.Graph(
            id='testing-graph',
            figure=fig[-1]
        )
    ])

    app.run_server(debug=True)
