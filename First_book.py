import pandas as pd
from Class.Data import Data
from Class.Book import Book

# DATA IMPORT
path = 'Data/Data/First_book_data.csv'
data = Data(path=path).imported_data

# BOOK SPECIFICATION
opt = dict()
#Options(Type, Position, Nominal, Strike, Maturity)
opt[1] = {'Type': 'C', 'Position': 'Short', 'Payoff': 500, 'Strike': 30000, 'Maturity': 3}
opt[2] = {'Type': 'C', 'Position': 'Short', 'Payoff': 1000, 'Strike': 50000, 'Maturity': 4}
opt[3] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 45000, 'Maturity': 5}
opt[4] = {'Type': 'C', 'Position': 'Short', 'Payoff': 1000, 'Strike': 44000, 'Maturity': 7}
opt[5] = {'Type': 'C', 'Position': 'Short', 'Payoff': 5000, 'Strike': 50000, 'Maturity': 7}
opt[6] = {'Type': 'C', 'Position': 'Short', 'Payoff': 1000, 'Strike': 47000, 'Maturity': 15}
opt[7] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 60000, 'Maturity': 25}
opt[8] = {'Type': 'C', 'Position': 'Short', 'Payoff': 50000, 'Strike': 70000, 'Maturity': 28}
opt[9] = {'Type': 'C', 'Position': 'Short', 'Payoff': 1000, 'Strike': 55000, 'Maturity': 29}
opt[10] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 30000, 'Maturity': 30} #Last maturity 11/04/2022


# BOOK INITIATION
book = Book(data=data,
            opt=opt,
            initial_cash=20000,
            pricing_method='BS',
            smile_active=False,
            delta_max=1,  ####
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

# REPORTS
for op in opt:
    book.book_objets[op].record.to_csv(f"Reports/First_book/opt/opt{op}.csv", sep=';')
for date in book.book_positions:
    dt = str(date[3] + date[4] + '_' + date[0] + date[1] + '_' + date[6] + date[7] + date[8] + date[9])
    book.book_positions[date].to_csv(f"Reports/First_book/positions/positions_{dt}.csv", sep=';')
book.book_delta_hedge.to_csv("Reports/First_book/delta_hedge.csv", sep=';')
