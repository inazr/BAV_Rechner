'''
v.0.0.1
Allgemeine Informationen:
Bei Fragen: Stephan@BI

Alle Angaben ohne Gewähr!
Bitte Änderungen ausschließlich in Personendaten.py durchführen.
Annahmen: Wohnhaft in NRW, Sozialversicherungspflichtig in D
'''

import pandas as pd
from datetime import datetime
import math
import Personendaten

pd.set_option("display.max_columns", 16)
pd.set_option("display.expand_frame_repr", False)

Geburtsdatum = datetime.strptime(Personendaten.Geburtsdatum, '%d.%m.%Y')
Renteneintritt = datetime.strptime(Personendaten.Renteneintritt, '%d.%m.%Y')
Bruttoeinkommen = Personendaten.Bruttoeinkommen
Bruttoeinkommen_Wachstum = Personendaten.Bruttoeinkommen_Wachstum_e
BAV_Vertragsbeginn = datetime.strptime(Personendaten.BAV_Vertragsbeginn, '%d.%m.%Y')
BAV_Bruttobeitrag = Personendaten.BAV_Bruttobeitrag_mtl * 12
BAV_Bruttoeinkommen = Bruttoeinkommen - BAV_Bruttobeitrag
BAV_Zuschuss = 0.15
Freistellungsauftrag = Personendaten.Freistellungsauftrag
Kapitalmarktzins_e = Personendaten.Kapitalmarktzins_e
ETF_TER = Personendaten.ETF_TER
GKV = Personendaten.GKV
GKV_Zusatzbeitrag = Personendaten.GKV_Zusatzbeitrag
PKV = Personendaten.PKV
PKV_Beitrag = Personendaten.PKV_Beitrag_mtl
Kinder = Personendaten.Kinder
Kirche = Personendaten.Kirche


# Beitragssätze 2020:
GKV_Beitragssatz = 0.14600
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
BAV_Sozialabgabenfrei = RV_Beitragsbemessungsgrenze * 0.04
BAV_Steuerfrei = RV_Beitragsbemessungsgrenze * 0.08

# Entwicklung durchschnittsentgelt
RV_Durchschnittsentgelt = 40551
RV_Durchschnittsentgelt_wachstum = 0.0185
RV_Abzug_proMonat = 0.003
RV_RP_Wert = 33.05


def calc_steuern(zvE):

    if zvE <= 9408:
        Lohnsteuer = 0

    elif zvE <= 14532:
        y = (zvE - 9408) / 10000
        Lohnsteuer = (972.87 * y + 1400) * y

    elif zvE <= 57051:
        z = (zvE - 14532) / 10000
        Lohnsteuer = (((212.02 * z) + 2397) * z) + 972.79

    elif zvE <= 270500:
        Lohnsteuer = (0.42 * zvE) - 8963.74 # 85289,66

    elif zvE > 270500:
        Lohnsteuer = 0.45 * zvE - 17078.74

    else:
        print("Fehler bei der Steuerberechnung.")

    Soli = Lohnsteuer * Solidaritaetszuschlag

    if Kirche:
        Kirchensteuer = Lohnsteuer * Kirchensteuer
    else:
        Kirchensteuer = 0

    return Lohnsteuer, Soli, Kirchensteuer


def calc_steuern_sozialabgaben(Bruttoeinkommen, GKV=GKV, GKV_Zusatzbeitrag=GKV_Zusatzbeitrag, PKV=PKV, PKV_Beitrag=PKV_Beitrag, Kinder=Kinder, Kirche=Kirche):

    if GKV:
        KV_Beitragssatz = (GKV_Beitragssatz + GKV_Zusatzbeitrag) * 0.5
        KV_Bemessungssatz = min(Bruttoeinkommen, GKV_Beitragsbemessungsgrenze)
        KV = KV_Beitragssatz * KV_Bemessungssatz
        AG_KV = KV_Beitragssatz * KV_Bemessungssatz

        if Kinder:
            PV = KV_Bemessungssatz * PV_Beitragssatz * 0.5

        else:
            PV = KV_Bemessungssatz * (PV_Beitragssatz * 0.5 + Kinderlosenmalus)

        AG_PV = = KV_Bemessungssatz * PV_Beitragssatz * 0.5

    elif PKV:
        KV = PKV_Beitrag
        AG_KV = PKV_Beitrag
        PV = 0

    AV_Bemessungssatz = min(Bruttoeinkommen, AV_Beitragsbemessungsgrenze)
    AV = AV_Bemessungssatz * AV_Beitragssatz * 0.5
    AG_AV = AV_Bemessungssatz * AV_Beitragssatz * 0.5

    RV_Bemessungssatz = min(Bruttoeinkommen, AV_Beitragsbemessungsgrenze)
    RV = RV_Bemessungssatz * RV_Beitragssatz * 0.5
    AG_RV = RV_Bemessungssatz * RV_Beitragssatz * 0.5

    KV = round(KV, 2)
    PV = round(PV, 2)
    RV = round(RV, 2)
    AV = round(AV, 2)


    #    11.781


    zvE = math.floor(Bruttoeinkommen - 1000 - 36 - min(25046 * 0.9 * 0.5, ((0.90 * 2 * RV) - RV) + ((0.90 * 2 * AV) - AV) + (0.90 * (KV_Bemessungssatz * PV_Beitragssatz * 0.5 + PV) - PV) + (0.96 * KV )))
    #zvE = math.floor(Bruttoeinkommen - 1000 - 36 - ((0.90 * 2 * RV) - RV) - ((0.90 * 2 * AV) - AV) - (0.90 * (KV_Bemessungssatz * PV_Beitragssatz * 0.5 + PV) - PV) - (0.96 * KV ))

    if

    zvE = math.floor(Bruttoeinkommen - 1000 - 36 min())

    Lohnsteuer, Soli, Kirchensteuer = calc_steuern(zvE)

    Lohnsteuer = math.floor(Lohnsteuer)
    Soli = round(Soli, 2)
    Kirchensteuer = round(Kirchensteuer, 2)

    Nettoeinkommen = Bruttoeinkommen - KV - AV - PV - RV - Lohnsteuer - Soli - Kirchensteuer

    return KV, AV, PV, RV, zvE, Lohnsteuer, Soli, Kirchensteuer, Nettoeinkommen


def calc_Altersrente():
    RegelRenteneintritt = datetime(Geburtsdatum.year + 67, Geburtsdatum.month + 1, 1)

    if (abs(Renteneintritt.year - RegelRenteneintritt.year) * 12 - (Renteneintritt.month - RegelRenteneintritt.month)) > 48:
        print("Rentenbeginn zu früh gewählt!")
        exit()

    Rentenabzug = RV_Abzug_proMonat * (abs(Renteneintritt.year - RegelRenteneintritt.year) * 12 - (Renteneintritt.month - RegelRenteneintritt.month))
    Rentenabzug = round(Rentenabzug, 4)

    JahreBisZurRente = abs(BAV_Vertragsbeginn.year - Renteneintritt.year) + abs(BAV_Vertragsbeginn.month - Renteneintritt.month)/12
    # print(round(JahreBisZurRente, 2))

    Rentenpunkte = min(Bruttoeinkommen, RV_Beitragsbemessungsgrenze) / RV_Durchschnittsentgelt * JahreBisZurRente
    Rentenwert = round(Rentenpunkte * RV_RP_Wert * (1 - Rentenabzug), 2)

    print("\n")
    print("Rentenpunkte: " + str(round(Rentenpunkte, 2)))
    print("Rentenwert: " + str(Rentenwert) + " €")

    BAV_Rentenpunkte = min(BAV_Bruttoeinkommen, RV_Beitragsbemessungsgrenze) / RV_Durchschnittsentgelt * JahreBisZurRente
    BAV_Rentenwert = round(BAV_Rentenpunkte * RV_RP_Wert * (1 - Rentenabzug), 2)

    print("BAV_Rentenpunkte: " + str(round(BAV_Rentenpunkte, 2)))
    print("BAV_Rentenwert: " + str(BAV_Rentenwert) + " €")
    print("\n")
    print("Reduzierung der brutto Altersrente durch Abschluss einer BAV voraussichtlich um " + str(round(Rentenwert - BAV_Rentenwert, 2)) + " € pro Monat.")

    return RegelRenteneintritt, Rentenabzug, Rentenpunkte, BAV_Rentenpunkte


def calc_ETF_Sparplan():
    pass


def create_Ansparphase_df():
    df_ASP = pd.DataFrame()
    df_ASP['Jahr'] = pd.date_range(start=BAV_Vertragsbeginn,
                                           periods=(Renteneintritt.year - BAV_Vertragsbeginn.year + 1), freq='Y').year

    df_ASP.set_index(keys='Jahr', inplace=True, drop=True)

    df_ASP['Laufzeit'] = df_ASP.index - min(df_ASP.index)

    df_ASP['Bruttoeinkommen'] = Bruttoeinkommen * (1 + Bruttoeinkommen_Wachstum)**df_ASP['Laufzeit']
    df_ASP['KV'], df_ASP['AV'], df_ASP['PV'], df_ASP['RV'], df_ASP['zvE'], df_ASP['Lohnsteuer'], df_ASP['Soli'], df_ASP['Kirchensteuer'], df_ASP['Nettoeinkommen'] = zip(*df_ASP['Bruttoeinkommen'].map(calc_steuern_sozialabgaben))
    df_ASP['Sozialabgaben'] = df_ASP['KV'] + df_ASP['AV'] + df_ASP['PV'] + df_ASP['RV']

    #df_ASP['BAV_Bruttoeinkommen'] = BAV_Bruttoeinkommen * (1 + Bruttoeinkommen_Wachstum)**df_ASP['Laufzeit']
    #df_ASP['BAV_KV'], df_ASP['BAV_AV'], df_ASP['BAV_PV'], df_ASP['BAV_RV'], df_ASP['BAV_zvE'], df_ASP['BAV_Lohnsteuer'], df_ASP['BAV_Soli'], df_ASP['BAV_Kirchensteuer'], df_ASP['BAV_Nettoeinkommen'] = zip(*df_ASP['BAV_Bruttoeinkommen'].map(calc_steuern_sozialabgaben))

    #df_ASP['BAV_Nettobelastung'] = df_ASP['Nettoeinkommen'] - df_ASP['BAV_Nettoeinkommen']
    #df_ASP['BAV_Nettobelastung_mtl'] = df_ASP['BAV_Nettobelastung'] / 12

    print(df_ASP.loc[2031: 2032])


if __name__ == "__main__":
    print("\n")
    print("!!!             Alle Angaben ohne Gewähr            !!!")
    print("       Dieses Angebot stellt keine Beratung dar.       ")
    print("Die Berechnung erfolgt nach besten Wissen und Gewissem.")
    print("\n")


    print("Schritt 1: Berechnungen der Ansparphase")
    create_Ansparphase_df()
















'''
    print("Einkommen ohne BAV: ")
    KV, AV, PV, RV, zvE, Lohnsteuer, Soli, Kirchensteuer, Nettoeinkommen = calc_steuern_sozialabgaben(
        Bruttoeinkommen, GKV, GKV_Zusatzbeitrag, PKV, PKV_Beitrag, Kinder, Kirche)

    print("Krankenversicherung: " + str(KV) + " € | Pflegeversicherung: " + str(PV) + " € | Rentenversicherung: " + str(
        RV)
          + " € | Arbeitslosenversicherung: " + str(AV) + " € | Lohnsteuer: "
          + str(Lohnsteuer) + " € | Solidaritaetszuschlag: " + str(Soli) + " € | Kirchensteuer: " + str(Kirchensteuer))

    print("Nettoeinkommen: " + str(round(Nettoeinkommen, 2)) + " €")

    print("\n")
    print("Einkommen mit BAV: ")
    BAV_KV, BAV_AV, BAV_PV, BAV_RV, BAV_zvE, BAV_Lohnsteuer, BAV_Soli, BAV_Kirchensteuer, BAV_Nettoeinkommen = calc_steuern_sozialabgaben(
        BAV_Bruttoeinkommen, GKV, GKV_Zusatzbeitrag, PKV, PKV_Beitrag, Kinder, Kirche)

    print("Krankenversicherung: " + str(KV) + " € | Pflegeversicherung: " + str(PV) + " € | Rentenversicherung: " + str(
        RV)
          + " € | Arbeitslosenversicherung: " + str(AV) + " € | Lohnsteuer: "
          + str(Lohnsteuer) + " € | Solidaritaetszuschlag: " + str(Soli) + " € | Kirchensteuer: " + str(Kirchensteuer))

    print("Nettoeinkommen: " + str(round(Nettoeinkommen, 2)) + " €")

    print("\n")
    print("Nettobelastung durch Abschluss einer BAV: " + str(round(Nettoeinkommen - BAV_Nettoeinkommen, 2)) + " €.")

    RegelRenteneintritt, Rentenabzug, Rentenpunkte, BAV_Rentenpunkte = calc_Altersrente()
'''

