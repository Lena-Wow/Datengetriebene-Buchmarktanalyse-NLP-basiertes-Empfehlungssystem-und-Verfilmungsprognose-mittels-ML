import pandas as pd
'''Datenquelle:GitHub Gist von „apietrick24“ , ursprung  das Kaggle‑Dataset '''
# Datei laden (ersetze den Dateinamen durch den tatsächlichen Pfad zu deiner Datei)
pfad = "D:\\awrDATEN\\lena\\DATA SCIENCE INSTITUTE\\abschlussprojekt_Buchmarkt\\Analyse_vorhersage_Bestseller_LW\\Option_03\\bookPublishingData.csv"
df = pd.read_csv(pfad)
# Ersten Blick auf die Daten werfen
print(df.head(50))  # zeigt die ersten 50 Zeilen

# (optional) Infos zum DataFrame anzeigen
print(df.columns)
 