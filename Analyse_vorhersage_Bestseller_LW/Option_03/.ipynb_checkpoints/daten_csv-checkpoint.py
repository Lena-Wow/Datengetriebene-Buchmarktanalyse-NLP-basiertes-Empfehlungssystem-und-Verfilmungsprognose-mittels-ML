import pandas as pd

# Datei laden (ersetze den Dateinamen durch den tatsächlichen Pfad zu deiner Datei)
pfad = "D:\\awrDATEN\\lena\\DATA SCIENCE INSTITUTE\\abschlussprojekt_Buchmarkt\\Analyse_vorhersage_Bestseller_LW\\Option_03\\bookPublishingData.csv"
df = pd.read_csv(pfad)
# Ersten Blick auf die Daten werfen
print(df.head(50))  # zeigt die ersten 5 Zeilen

# (optional) Infos zum DataFrame anzeigen
print(df.info())
