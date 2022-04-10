import pandas as pd
from Data import Data
from Book import Book

data = Data().imported_data

opt = dict()
#Options(Type, Position, Nominal, Strike, Maturity(minuts))
opt[1] = {'Type': 'C', 'Position': 'Long', 'Payoff': 1000, 'Strike': 40000, 'Maturity': 1}
opt[2] = {'Type': 'C', 'Position': 'Long', 'Payoff': 1000, 'Strike': 40000, 'Maturity': 1}

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
print(book.book_positions['18/03/2022'])
print(f"\n Global Position with initial cash = {book.initial_cash}")
print(book.book_delta_hedge)

# book.book_objets[1].record.to_csv("Report/opt1.csv")
# book.book_objets[2].record.to_csv("Report/opt2.csv")
# for date in book.book_positions:
#     book.book_positions[date].to_csv(f"Report/positions_{date[:1]}.csv")
# book.book_delta_hedge.to_csv("Report/delta_hedge.csv")
