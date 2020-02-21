'''
v.0.0.1
Allgemeine Informationen:
Bei Fragen: Stephan@BI
Die Berechnungen funktionieren bei Ehegattensplitting (noch) nicht.
Alle Angaben ohne Gewähr!
'''

import pandas as pd
from datetime import datetime
from datetime import timedelta
import math

'''
In diesem Abschnitt bitte Änderungen vornehmen:
Alle Angaben p.a. !
'''
Geburtsdatum = datetime.strptime('14.11.1986', '%d.%m.%Y')
'''
    IdR: 01. des Monats nach dem 67. Geburtstag
    Mit Abzug: frühestens nach dem 63. Geburstag
    Mit GdB von >= 50: frühestens nach dem 62. Geburstag
'''
Renteneintritt = datetime.strptime('01.12.2053', '%d.%m.%Y')

BAV_Vertragsbeginn = datetime.strptime('01.04.2020', '%d.%m.%Y')

Bruttoeinkommen = 48000
Gehaltssteigerung_e = 0.02

BAV_Bruttobeitrag = 2400
BAV_ST_Zuschuss = 0.15

Freistellungsauftrag: 801   # Verheiratet: max 1.602 €, Alleinstehend: max. 801 €
Kapitalmarktzins_e = 0.05

# Krankenversicherung
GKV: True
GKV_Zusatzbeitrag = 0.07
PKV: False
PKV_Beitrag: 0

# Sonstige Angaben
Kinder: False
Kirche: False


'''
In diesem Abschnitt bitte nur Änderungen vornehmen, wenn du weißt was du tust:
'''
BAV_Bruttoeinkommen = Bruttoeinkommen - BAV_Bruttobeitrag

# Beitragssätze 2020:
GKV_Beitragssatz = 0.146
AV_Beitragssatz = 0.024
RV_Beitragssatz = 0.186
PV_Beitragssatz = 0.0305
Kinderlosenmalus = 0.0025
Solidaritaetszuschlag = 0.055
Kirchensteuer = 0.09

# Beitragsbemessungsgrenzen 2020:
GKV_Beitragsbemessungsgrenze = 56250
PV_Beitragsbemessungsgrenze = 56250
RV_Beitragsbemessungsgrenze = 82800
AV_Beitragsbemessungsgrenze = 82800

# Entwicklung durchschnittsentgelt
durchschnittsentgelt_rentenversicherung_2020 = 40551
durchschnittsentgelt_rentenversicherung = 0.0185


'''
In diesem Abschnitt bitte - KEINE - Änderungen vornehmen:
'''

def calc_steuern_sozialabgaben(Bruttoeinkommen, GKV, GKV_Zusatzbeitrag, PKV, PKV_Beitrag, Kinder, Kirche):

    if GKV:
        KV_Beitragssatz = (GKV_Beitragssatz + GKV_Zusatzbeitrag) * 0.5
        KV_Bemessungssatz = min(Bruttoeinkommen, 56250)
        KV = KV_Beitragssatz * KV_Bemessungssatz


        if Kinder:
            PV = KV_Bemessungssatz * (PV_Beitragssatz) * 0.5

        else:
            PV = KV_Bemessungssatz * (PV_Beitragssatz * 0.5 + Kinderlosenmalus)

    elif PKV:
        KV = PKV_Beitrag
        PV = 0


    AV_Bemessungssatz = min(Bruttoeinkommen, 82800)
    AV = AV_Bemessungssatz * AV_Beitragssatz * 0.5

    RV_Bemessungssatz = min(Bruttoeinkommen, 82800)
    RV = RV_Bemessungssatz * RV_Beitragssatz * 0.5

    KV = round(KV, 2)
    PV = round(PV, 2)
    RV = round(RV, 2)
    AV = round(AV, 2)

    zvE = math.floor(Bruttoeinkommen - KV - (0.9 * (AV + RV + PV)))

    if zvE <= 9408:
        Lohnsteuer = 0

    elif zvE <= 14532:
        y = (zvE - 9408) / 10000
        Lohnsteuer = (972.87 * y + 1400) * y

    elif zvE <= 57051:
        z = (zvE - 14532) / 10000
        Lohnsteuer = (212.02 * z + 2397) * z + 972.79

    elif zvE <= 270500:
        Lohnsteuer = 0.42 * zvE - 8963.74

    elif zvE > 270500:
        Lohnsteuer = 0.45 * zvE - 17078.74

    else:
        print("Fehler bei der Steuerberechnung.")

    Soli = Lohnsteuer * 0.055

    if Kirche:
        Kirchensteuer = Lohnsteuer * 0.09
    else:
        Kirchensteuer = 0


    Lohnsteuer = math.floor(Lohnsteuer)
    Soli = round(Soli, 2)
    Kirchensteuer = round(Kirchensteuer, 2)

    Nettoeinkommen = Bruttoeinkommen - KV - AV - PV - RV - Lohnsteuer - Soli - Kirchensteuer

    print(str(KV) + " € Krankenversicherung")
    print(str(PV) + " € Pflegeversicherung")
    print(str(RV) + " € Rentenversicherung")
    print(str(AV) + " € Arbeitslosenversicherung")
    print(str(zvE) + " € zu versteuerndes Einkommen")
    print(str(Lohnsteuer) + " € Lohnsteuer")
    print(str(Soli) + " € Soli")
    print(str(Kirchensteuer) + " € Kirchensteuer")
    print(str(Nettoeinkommen) + " € Nettoeinkommen")

    return KV, AV, PV, RV, zvE, Lohnsteuer, Soli, Kirchensteuer, Nettoeinkommen




def calc_Verlust_Rentenpunkte(Bruttoeinkommen):


if __name__ == "__main__":
    print("YOUR MILEAGE MY VARY!")

    KV, AV, PV, RV, zvE, Lohnsteuer, Soli, Kirchensteuer, Nettoeinkommen = calc_steuern_sozialabgaben(
        Bruttoeinkommen, person['GKV'], person['GKV Zusatzbeitrag'], person['PKV'], person['PKV Beitrag'],
        person['Kinder'], person['Kirchensteuer'])


    _, _, _, _, _, _, _, _, Nettoeinkommen_BAV = calc_steuern_sozialabgaben(
        Bruttoeinkommen_BAV, person['GKV'], person['GKV Zusatzbeitrag'], person['PKV'], person['PKV Beitrag'],
        person['Kinder'], person['Kirchensteuer'])

    BAV_Monatsbeitrag_Netto  = round((Nettoeinkommen - Nettoeinkommen_BAV )/ 12, 2)
    print(BAV_Monatsbeitrag_Netto)