import pandas as pd

df = pd.DataFrame({"Sales QTY": [10, 20, 30, 40],
                   "Sales Person": ['Jack', 'Adam', 'Ken', 'Jack'],
                   "Product": ["Apple", "Orange", "Apple", "Cherry"]
                   })
rows = []
rows.append(list(df.columns))
for row in df.itertuples(index=False):
    tmp = list(row)
    rows.append(tmp)

# The accepted answer consists of two lines
L = df.to_numpy().tolist()
L.insert(0,df.columns.tolist())

