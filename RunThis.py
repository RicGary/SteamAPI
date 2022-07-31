import pandas as pd

from main import UserID, WishlistPage, WishPrices, WishlistSum, OutputData
from time import sleep

print('Exemple:')
print('https://steamcommunity.com/profiles/76561198113335827/')

urlTest = input('Paste your steam URL here: ')
try:
    ID = UserID(urlTest)
    WishURL = WishlistPage(ID)
    Prices = WishPrices(WishURL)
    SumPrices = WishlistSum(Prices)
    OutputData(Prices, SumPrices, ID[1])

    print()
    print('Check Output dir for more info')
    print(pd.DataFrame(Prices))
    print()
    print('Total: ', SumPrices)

    sleep(10)

except:
    print()
    print('Your steam wishlist is private.')
    sleep(5)