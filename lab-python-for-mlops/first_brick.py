import pandas as pd

URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
df = pd.read_csv(URL)

print(df.head(10))
print()
print("rows, columns:", df.shape)
print("missing values per column:")
print(df.isna().sum())
