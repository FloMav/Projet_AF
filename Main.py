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
opt[1] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 30000, 'Maturity': 3}
opt[2] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 50000, 'Maturity': 10}
opt[3] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 45000, 'Maturity': 15}
opt[4] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 44000, 'Maturity': 7}
opt[5] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 42000, 'Maturity': 3}
opt[6] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 53000, 'Maturity': 5}
opt[7] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 60000, 'Maturity': 4}
opt[8] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 70000, 'Maturity': 7}
opt[9] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 55000, 'Maturity': 14}
opt[10] = {'Type': 'C', 'Position': 'Short', 'Payoff': 10000, 'Strike': 70000, 'Maturity': 30}



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
print(book.book_positions['12/03/2022'])
print(f"\n Global Position with initial cash = {book.initial_cash}")
print(book.book_delta_hedge)



