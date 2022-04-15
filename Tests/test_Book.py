import pandas as pd
from Class.Data import Data
from Class.Book import Book


# DATA IMPORT
path_data = "Data/First_book_data.csv"
data = Data(path=path_data).imported_data

# BOOK SPECIFICATION
opt = dict()
#Options(Type, Position, Nominal, Strike, Maturity)
opt[1] = {'Type': 'C', 'Position': 'Long', 'Payoff': 1000, 'Strike': 40000, 'Maturity': 1}
opt[2] = {'Type': 'C', 'Position': 'Long', 'Payoff': 1000, 'Strike': 40000, 'Maturity': 1}


# BOOK INITIATION
book = Book(data=data,
            opt=opt,
            initial_cash=20000,
            pricing_method='BS',
            smile_active=False,
            delta_max=1,
            annual_basis=365,
            inception_date="12/03/2022")

pd.set_option('display.max_columns', None)
print("###### Test Record\n")
print("\n###### Option 1\n")
print(book.book_objets[1].record)
print("\n###### Option 2\n")
print(book.book_objets[2].record)

# BACKETESTIN & RECORDING
book.backtest()

print("\n###### Option 1\n")
print(book.book_objets[1].record)
print("\n###### Option 2\n")
print(book.book_objets[2].record)

print("\n\n\n\n###### Test book_position\n")
print(book.book_positions['12/03/2022'])
print(f"\n\n\n\n\n Global Position with initial cash = {book.initial_cash}")
print(book.book_delta_hedge)

