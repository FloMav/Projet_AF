import pandas as pd
from Data import Data
from Book import Book

############## BEFORE STARTING ###############
#Set up the inception date in the recorder (Vanilla/Binary)
#Set up smile data provenance

#Choose the pricing method (BS,...)
#Set up annual basis, default=365)
#Choose smile or not in BOOK
##############################################

data = Data().imported_data



###########ATTENTION theta_digital à verfier dans B&S


opt = dict()
#Options(Type, Position, Nominal, Strike, Maturity(minuts))
opt[1] = {'Type': 'C', 'Position': 'Long', 'Payoff': 10000, 'Strike': 30000, 'Maturity': 3}
opt[2] = {'Type': 'C', 'Position': 'Long', 'Payoff': 5000, 'Strike': 40944.839844, 'Maturity': 3}

book = Book(data, opt)
pd.set_option('display.max_columns', None)
print("###### Record\n")
print("\n###### Option 1\n")
print(book.book_objets[1].record)
print("\n###### Option 2\n")
print(book.book_objets[2].record)
book.backtest()
print("\n###### Option 1\n")
print(book.book_objets[1].record)
print("\n###### Option 2\n")
print(book.book_objets[2].record)



