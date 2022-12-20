import pandas as pd

#Dataset
df = pd.read_csv('DATA/valeursfoncieres-2018.txt', sep='|', low_memory=False)
#print (type(df), '\n')

print (df, '\n')