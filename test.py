import pandas as pd

a = pd.DataFrame(columns=['Spot', 'Volatility', 'Delta', 'Gamma'])

a.loc[a.shape[0]] = [0,1,2,3]
a.loc[a.shape[0]] = [0,1,2,3]

print(a)