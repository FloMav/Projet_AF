from BinaryOption import BinaryOption
import pandas as pd

# Test digital call
digital_call_repC = BinaryOption(100, 100, 0.05, 0.01, 30, delta_max=1, volatility=0.25, payoff=1,  typ='C', rep='C')
print("### Test digital call")
print(f'Payoff = {digital_call_repC.payoff}')
print(f'Delta_max = {digital_call_repC.delta_max}')
print(f'Price_digital_call = {digital_call_repC.price_digital}')
print(f'delta_digital_call = {digital_call_repC.delta_digital}')
print(f'Price_bull_spread_call = {digital_call_repC.price_spread}')
print(f'delta_spread_call = {digital_call_repC.delta_spread}')
print(f'gamma_spread_call = {digital_call_repC.gamma_spread}')
print(f'vega_spread_call = {digital_call_repC.vega_spread}')
print(f'theta_spread_call = {digital_call_repC.theta_spread}')
print(f'rho_spread_call = {digital_call_repC.rho_spread}')

# Test digital put
digital_call_repP = BinaryOption(100, 100, 0.05, 0.01, 30, delta_max=1, volatility=0.25, payoff=1, typ='C', rep='P')
print("\n### Test digital put")
print(f'Payoff = {digital_call_repP.payoff}')
print(f'Delta_max = {digital_call_repP.delta_max}')
print(f'Price_digital_call = {digital_call_repP.price_digital}')
print(f'Price_bull_spread_put = {digital_call_repP.price_spread}')

# pd.set_option('display.max_columns', None) #print all columns
# Alicia = BinaryOption(100, 100, 0.05, 0.01, 30, delta_max=1, volatility=0.25, payoff=1, typ='C', rep='P')
# print("\n### Test recorder")
# print(Alicia.record)
# print("")
# print("Back_test")
# #spot = [101, 102]
# for a, b, c, d, e in zip([101, 102], [0.1, 0.15], [0.05, 0.1], [35, 40], [0.16, 0.17]):
#     Alicia.setter((a, b, c, d, e))
#     #print(Alicia.record)
#     print("")
#
# print("")
# print("")
# print("")
# print(Alicia.record)

Alicia = BinaryOption(100, 100, 0.05, 0.01, 30, delta_max=1, volatility=0.25, payoff=1, typ='C', rep='C')
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
