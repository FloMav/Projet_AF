from VanillaOption import VanillaOption

call = VanillaOption(100, 100, 0.05, 0.01, 30, volatility=0.25)
print("### Test Call")
print(f'Price = {call.price}')
print(f'Delta = {call.delta}')
print(f'Gamma = {call.gamma}')
print(f'Theta = {call.theta}')
print(f'Vega = {call.vega}')

put = VanillaOption(100, 100, 0.05, 0.01, 30, typ='P', volatility=0.25)
print("\n### Test Put")
print(f'Price = {put.price}')
print(f'Delta = {put.delta}')
print(f'Gamma = {put.gamma}')
print(f'Theta = {put.theta}')
print(f'Vega = {put.vega}')

put.volatility = 0.16
print("\n### Test Put new vol")
print(f'Volatility = {put.volatility}')
print(f'Price = {put.price}')
print(f'Delta = {put.delta}')
print(f'Gamma = {put.gamma}')
print(f'Theta = {put.theta}')
print(f'Vega = {put.vega}')

print("")
Alicia = VanillaOption(100, 100, 0.05, 0.01, 30, volatility=0.25)
print(Alicia.record)
print("")
for a, b in zip([101, 102], [0.16, 0.17]):
    Alicia.setter((a, b))
    print(Alicia.record)
    print("")

