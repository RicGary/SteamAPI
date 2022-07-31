def UserID(url):
    """
    Transforms your steam community url into ID code.

    Parameters
    ----------
    url : str
        Steam profile community url

    Returns
    -------
    ID : str
        ID code
    """
    ID = url.split('/')
    return ID[-3], ID[-2]


def WishlistPage(id):
    """
    Take your ID and put on wishlist page.

    Parameters
    ----------
    id : str
        ID code

    Returns
    -------
    link : str
        wish list Url
    """
    return f'https://store.steampowered.com/wishlist/{id[0]}/{id[1]}/#sort=price'


def WishPrices(wishlistUrl):
    """
    Transforms something into a zipped list of (game, price)

    Parameters
    ----------
    wishlistUrl : str
        wish list Url

    Returns
    -------
    data : list
        zipped list
    """
    import requests
    import json
    import re

    # I have no clue of what's happening here
    wishlist_url = json.loads(re.findall(r'g_strWishlistBaseURL = (".*?");', requests.get(wishlistUrl).text)[0])
    objectsDict = requests.get(wishlist_url + 'wishlistdata/?p=0').json()

    try:
        def convertPrice(stringPrice):
            stringPrice = str(stringPrice)
            return stringPrice[0:-2] + '.' + stringPrice[-2:]

        data = [(value['name'], convertPrice(value['subs'][0]['price']))
                for _, value in objectsDict.items()
                if value['subs']]
        return data

    except TypeError as err:
        print("Error: ", err)
        print("Oops, we encounter an error. Check if your wishlist is private by going on "
              "private navigation and pasting this:")
        print(wishlistUrl)
        from time import sleep
        from sys import exit
        sleep(10)
        exit()


def WishlistSum(data):
    """ Converts into dataframe and sum the Price column """
    import pandas as pd

    df = pd.DataFrame(data)
    df.columns = ['Game_Name', 'Price']
    df = df.astype({'Price': 'float'})
    return round(df['Price'].sum(), 2)


def OutputData(data, wishSum, name):
    """
    Makes a beauty txt

    Parameters
    ----------
    data : list
        zipped list

    wishSum : float
        sum of Price column

    name : str
        name/ID of profile

    Returns
    -------
    output file : .txt
    """
    with open(f'Output/{name}.txt', 'w', encoding='utf8') as file:
        file.write(f'Profile: {name}\n')
        file.write('┌' + '─'*56 + '┬' + '─'*11 + '┐\n')
        file.write(f'{"│Game":56s} │ {"Price":10s}│\n')
        file.write('├' + '─'*56 + '┼' + '─'*11 + '┤\n')
        for line in data:
            file.write(f'│{line[0]:55s} │R$ {line[1]:8s}│\n')

        file.write('├' + '─'*56 + '┼' + '─'*11 + '┤\n')
        file.write(f'│{"Total":55s} │R$ {str(wishSum):8s}│\n')
        file.write('└' + '─'*56 + '┴' + '─'*11 + '┘\n')


if __name__ == '__main__':
    urlTest = 'https://steamcommunity.com/id/jvoli/'
    ID = UserID(urlTest)
    WishURL = WishlistPage(ID)
    Prices = WishPrices(WishURL)
    SumPrices = WishlistSum(Prices)
    OutputData(Prices, SumPrices, ID[1])
