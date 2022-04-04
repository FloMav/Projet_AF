import pandas as pd
from Data import Data
from Book import Book

data = Data().total_data

opt = dict()
#Options(Type, Position, Nominal, Strike, Maturity(minuts))
opt[1] = {'Type': 'C', 'Position': 'Short', 'Payoff': 1000, 'Strike': 35500, 'Maturity': '2022-01-24 08:47:00'}
opt[2] = {'Type': 'C', 'Position': 'Short', 'Payoff': 5000, 'Strike': 35600, 'Maturity': '2022-01-24 08:45:00'}


book = Book(data, opt)
book.report()

#for i in book.book:
    #print(i)
    #print(book.book[i])
