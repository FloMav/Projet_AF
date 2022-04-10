import pandas as pd
from Data import Data
from Book import Book

data = Data().imported_data

opt = dict()
#Options(Type, Position, Nominal, Strike, Maturity(minuts))
opt[1] = {'Type': 'C', 'Position': 'Long', 'Payoff': 1000, 'Strike': 45000, 'Maturity': 4}
opt[2] = {'Type': 'C', 'Position': 'Long', 'Payoff': 1000, 'Strike': 44000, 'Maturity': 4}

book = Book(data, opt)
pd.set_option('display.max_columns', None)
print("###### Test Record\n")
print("\n###### Option 1\n")
print(book.book_objets[1].record)
print("\n###### Option 2\n")
print(book.book_objets[2].record)

book.backtest()
print("\n###### Option 1\n")
print(book.book_objets[1].record)
print("\n###### Option 2\n")
print(book.book_objets[2].record)


print("\n\n###### Test book_position\n")
#print(book.book_objets[1].record.loc['18/03/2022'].values)
#print(book.book_positions.keys())
print(book.book_positions['18/03/2022'])
print("\n Global Position")
print(book.book_track)

