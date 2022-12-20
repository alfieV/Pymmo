import pandas as pd

#Dataset
df = pd.read_csv('DATA/valeursfoncieres-2018.txt', sep='|', low_memory=False)
#print (type(df), '\n')

#print (df, '\n')
print (df.describe(), '\n')

#Les 7 premières valeurs sont confidentiels (identité de la personne etc...)
numDisposition = df['No disposition']
dateMutation = df['Date mutation']
natureMutation = df['Nature mutation']
valeurFonciere = df['Valeur fonciere']
numVoie = df['No voie']
indiceRepetition = df['B/T/Q']
typeVoie = df['Type de voie']
codeRivoli = df['Code voie']
nomVoie = df['Voie']
codepostal = df['Code postal']
nomCommune = df['Commune']
codeDepartement = df['Code departement']
codeCommune = df['Code commune']
print (valeurFonciere, '\n')