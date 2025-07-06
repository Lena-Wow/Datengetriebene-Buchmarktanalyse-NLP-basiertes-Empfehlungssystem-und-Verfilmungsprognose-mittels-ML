import pandas as pd

df1 = pd.read_csv("bestseller.csv")
df2 = pd.read_csv("nicht_bestseller_buecher_syntetisch.csv")
df3 = pd.read_csv("nicht_bestseller_goodreads_realistisch.csv")

df_gesamt = pd.concat([df1, df2, df3], ignore_index=True)

df_gesamt.to_csv("zusammengefuegt.csv", index=False)
print(df_gesamt.head(10))    

