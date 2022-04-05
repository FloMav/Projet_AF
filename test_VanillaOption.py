from VanillaOption import VanillaOption
import pandas as pd


call = VanillaOption(100, 100, 0.05, 0.01, 30, volatility=0.25)
print("### Test Call")
print(f'Price = {call.price}')
print(f'Delta = {call.delta}')
print(f'Gamma = {call.gamma}')
print(f'Theta = {call.theta}')
print(f'Vega = {call.vega}')
print(f'Vega = {call.rho}')

put = VanillaOption(100, 100, 0.05, 0.01, 30, typ='P', volatility=0.25)
print("\n### Test Put")
print(f'Price = {put.price}')
print(f'Delta = {put.delta}')
print(f'Gamma = {put.gamma}')
print(f'Theta = {put.theta}')
print(f'Vega = {put.vega}')
print(f'Vega = {put.rho}')

put.volatility = 0.16
print("\n### Test Put new vol")
print(f'Volatility = {put.volatility}')
print(f'Price = {put.price}')
print(f'Delta = {put.delta}')
print(f'Gamma = {put.gamma}')
print(f'Theta = {put.theta}')
print(f'Vega = {put.vega}')
print(f'Vega = {put.rho}')


Alicia = VanillaOption(100, 100, 0.05, 0.00, 30, volatility=0.25, typ='P')
pd.set_option('display.max_columns', None) #print all columns
print("\n### Test Backtest option")
print("\n### Option at inception\n")
print(Alicia.record)
print("")

spot = [101, 102]
rate = [0.1, 0.15]
dividend = [0.05, 0.1]
maturity = [35, 40]
volatility = [0.16, 0.17]
for s, r, d, m, v in zip(spot, rate, dividend, maturity, volatility):
    Alicia.setter((s, r, d, m, v))

print("\n### Option's life\n")
print(Alicia.record)
