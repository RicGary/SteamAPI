import pandas as pd
from Wishlist import userID, wishlistPage, wishPrices, wishlistSum, outputData
from time import sleep

print('Exemple:')
print('https://steamcommunity.com/profiles/76561198113335827/')
print('or')
print('https://steamcommunity.com/id/yourNameHere/')

urlTest = input('Paste your steam URL here: ')

ID = userID(urlTest)
WishURL = wishlistPage(ID)
Prices = wishPrices(WishURL)
SumPrices = wishlistSum(Prices)
outputData(Prices, SumPrices, ID[1])

print()
print('Check Output dir for more info')
print(pd.DataFrame(Prices))
print()
print('Total: ', SumPrices)

sleep(10)
