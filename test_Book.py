import pandas as pd
from Data import Data
from Book import Book

#Data
data = Data().imported_data

#Options(Type, Position, Nominal, Strike, Maturity(minuts))
opt = dict()
opt[1] = {'Type': 'C', 'Position': 'Long', 'Payoff': 10000, 'Strike': 30000, 'Maturity': 50}
book = Book(data, opt)
pd.set_option('display.max_columns', None)
print(book.book[1].record)
print("")
print("Back_test")
book.backtest()
print("")
print("")
print("")
print(book.book[1].record)