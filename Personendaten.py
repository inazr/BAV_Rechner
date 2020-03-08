# Alle Angaben p.a.

Geburtsdatum = '14.11.1986'
Renteneintritt = '01.12.2053' # IdR: 01. des Monats nach dem 67. Geburtstag. Mit Abzug: frühestens nach dem 62. Geburstag. Der Abzug wird nicht berechnet!

Bruttoeinkommen = 54321
Bruttoeinkommen_Wachstum_e = 0.02 # Erwarteter Wert über der Inflation.

# Rentenversicherung
RV_angesammelte_RP = 10 # Bisher erworbene Rentenpunkte. Vereinfacht -> Summe über eigener Bruttoverdienst / Deutschlandweiter durchschnittlicher Bruttoverdienst p.a. ( im Jahr 2020 ca. 40551 €) Schätzwert: Anzahl Arbeitsjahre.

# Krankenversicherung
GKV = True
GKV_Zusatzbeitrag = 0.007

# Funktioniert noch nicht
PKV = False
PKV_Beitrag_mtl = 0

# Sonstige Angaben
Kinder = False
Kirche = False

# BAV Vertrag
BAV_Vertragsbeginn = '01.04.2020'
BAV_Bruttobeitrag_mtl = 200
BAV_Zuschuss = 0.25

# Finanzmarktdaten
Freistellungsauftrag= 801   # Verheiratet: max 1.602 €, Alleinstehend: max. 801 €
Kapitalmarktzins_e = 0.05
ETF_TER = 0.01
Entnahme_mtl = BAV_Bruttobeitrag_mtl * 2 # Schätzwert der Bruttoentnahme für alle Personen um die 30, um den Fond im 30. Jahr nach Renteneintritt aufgebraucht zu haben. Wer glaubt, dass er älter als 97 wird, bzw. bereits älter als ~32 ist, sollte diesen Wert GGf. anpassen um kein negatives Fondsguthaben zu erzeugen!