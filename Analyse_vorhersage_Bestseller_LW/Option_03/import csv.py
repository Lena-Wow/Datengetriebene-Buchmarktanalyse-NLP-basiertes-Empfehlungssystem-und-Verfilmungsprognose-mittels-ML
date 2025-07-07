import pandas as pd

# Eingabedatei
input_path = "row_BookPublishingDaten.csv"
output_path = "book_avg_fixed.csv"

# CSV laden (auch wenn sie schmutzig ist – ohne strikte Prüfung der Felderanzahl)
with open(input_path, encoding="utf-8") as f:
    lines = f.readlines()

# Die erste Zeile ist die Header-Zeile
header = lines[0]
data_lines = lines[1:]

# Neue Liste für bereinigte Zeilen
cleaned_lines = [header]

for line in data_lines:
    parts = line.strip().split(",")

    if len(parts) < 6:
        cleaned_lines.append(line)  # unvollständig, aber belassen
        continue

    # Spalte 6 = Book_Average_Rating
    try:
        rating_raw = parts[5].strip().replace('"', '').replace(',', '.')
        rating_float = float(rating_raw)
        parts[5] = f"{rating_float:.2f}"
    except Exception:
        # Falls Umwandlung fehlschlägt – nichts tun
        pass

    # Zeile wieder zusammensetzen
    cleaned_line = ",".join(parts)
    cleaned_lines.append(cleaned_line + "\n")

# Neue Datei speichern
with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(cleaned_lines)

print(f"✅ Fertig: Nur 'Book_Average_Rating' wurde korrigiert. Ergebnis in '{output_path}'.")

