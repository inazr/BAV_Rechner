'''
v.0.0.2
Allgemeine Informationen:
Bei Fragen: Stephan@BI

Alle Angaben ohne Gewähr!
Bitte Änderungen ausschließlich in Personendaten.py durchführen.
'''

import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import math
import time
import Personendaten
import warnings

warnings.filterwarnings('ignore')
pd.set_option("display.max_columns", 12)
pd.set_option("display.expand_frame_repr", False)


Geburtsdatum = datetime.strptime(Personendaten.Geburtsdatum, '%d.%m.%Y')
Renteneintritt = datetime.strptime(Personendaten.Renteneintritt, '%d.%m.%Y') + timedelta(days=-1)
Bruttoeinkommen = Personendaten.Bruttoeinkommen // 12
Bruttoeinkommen_Wachstum = Personendaten.Bruttoeinkommen_Wachstum_e
BAV_Vertragsbeginn = datetime.strptime(Personendaten.BAV_Vertragsbeginn, '%d.%m.%Y')
BAV_Bruttobeitrag = Personendaten.BAV_Bruttobeitrag_mtl * 12
BAV_Bruttoeinkommen = Bruttoeinkommen - BAV_Bruttobeitrag
BAV_Zuschuss = 0.15
Freistellungsauftrag = Personendaten.Freistellungsauftrag
Kapitalmarktzins_e = Personendaten.Kapitalmarktzins_e
ETF_TER = Personendaten.ETF_TER
ETF_Entnahme = Personendaten.Entnahme_mtl
RV_angesammelte_RP = Personendaten.RV_angesammelte_RP
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
Abgeltungssteuer = 0.25


def zins_pro_jahr_in_zins_pro_monat(zins):
    # In der Finanzmathematik hat ein Monat genau 30 Tage!
    zins = ((1 + zins) ** (1 / 12)) - 1
    
    return zins


def zins_pro_jahr_in_zins_pro_tag(zins):
    # In der Finanzmathematik hat ein Jahr genau 360 Tage!
    zins = ((1 + zins) ** (1 / 360)) - 1
    
    return zins


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
        Lohnsteuer = (0.42 * zvE) - 8963.74

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


def calc_rentenpunkte(Einkommen):
    Rentenpunkte_pro_Monat = min(Einkommen, RV_Beitragsbemessungsgrenze / 12) / (RV_Durchschnittsentgelt / 12) / 12

    return Rentenpunkte_pro_Monat


def calc_ETF_verlauf(df_ETF):
    df_ETF['Nettoaufwand'].fillna(0, inplace=True)

    df_ETF['Bruttoentnahme'] = ETF_Entnahme * (1 - df_ETF['Arbeit_vs_Rente'])
    df_ETF['Jahresbruttoentnahme'] = df_ETF['Bruttoentnahme'].resample('Y').sum()
    
    for i in range(1, len(df_ETF)):
       
        '''
        Berechnet den Bruttofondswert
        '''
        df_ETF['Fondswert'].iloc[i] = (df_ETF['Nettoaufwand'].iloc[i] + df_ETF['Fondswert'].iloc[i-1] - df_ETF['Bruttoentnahme'].iloc[i-1]) * (1 + zins_pro_jahr_in_zins_pro_monat(Kapitalmarktzins_e))
        
        '''
        Berechnet die TER
        '''
        df_ETF['TER'].iloc[i] = df_ETF['Fondswert'].iloc[i] * zins_pro_jahr_in_zins_pro_monat(ETF_TER)

       # Berechnung der Steuer auf den Aktien Fond
        if i % 12 == 11: # == 11 -> Dezember
            # Basisertrag (min 0) = Wert am Jahresanfang * Basiszins 2020 * 0,7
            df_ETF['Basisertrag'].iloc[i] = df_ETF['Fondswert'].iloc[i-11] * 0.0007 * 0.7
            
            # Vorabpauschale = max(min(Basisertrag, Gesamtergebnis) - Bruttoentnahme, 0)
            df_ETF['Vorabpauschale'].iloc[i] = max(df_ETF['Basisertrag'].iloc[i] - df_ETF['Jahresbruttoentnahme'].iloc[i], 0)
            
            # Steuer der Vorabpauschale
            df_ETF['Steuerlast_Vorabpauschale'].iloc[i] = df_ETF['Vorabpauschale'].iloc[i] * 0.7 * ((1 + Solidaritaetszuschlag) * Abgeltungssteuer)

            # Steuer der Entnahme  Bruttoentnahme
            df_ETF['Steuerlast_Bruttoentnahme'].iloc[i] = df_ETF['Jahresbruttoentnahme'].iloc[i] * 0.7 * ((1 + Solidaritaetszuschlag) * Abgeltungssteuer)
            
            # Berechnung der Gesamtsteuer inkl. Freistellungsauftrag
            df_ETF['Steuerlast_Gesamt'].iloc[i] = max(df_ETF['Steuerlast_Vorabpauschale'].iloc[i] + df_ETF['Steuerlast_Bruttoentnahme'].iloc[i] - Freistellungsauftrag, 0)
          
            # Berechnet die Nettoentnahme nach Abzug der Abgeltungssteuer
            df_ETF['Jahresnetto'].iloc[i] = df_ETF['Jahresbruttoentnahme'].iloc[i] - df_ETF['Steuerlast_Gesamt'].iloc[i]

        '''
        Berechnet den Nettofondswert
        '''
        df_ETF['Fondswert'].iloc[i] = df_ETF['Fondswert'].iloc[i] - df_ETF['TER'].iloc[i]
        
    '''
    Berechnet die monatliche Nettoentnahme
    '''
    df_ETF['Jahresnetto'].fillna(method='bfill', inplace=True)
    df_ETF['Nettoentnahme'] = df_ETF['Jahresnetto'] / 12
    
    return df_ETF


def calc_steuern_sozialabgaben(Bruttoeinkommen, Monatsbrutto, Arbeit_vs_Rente= 1, GKV=GKV, GKV_Zusatzbeitrag=GKV_Zusatzbeitrag, PKV=PKV, PKV_Beitrag=PKV_Beitrag, Kinder=Kinder, Kirche=Kirche):

    if GKV:
        KV_Beitragssatz = (GKV_Beitragssatz + GKV_Zusatzbeitrag) * 0.5
        KV_Bemessungssatz = min(Bruttoeinkommen, GKV_Beitragsbemessungsgrenze)
        KV = KV_Beitragssatz * KV_Bemessungssatz


        if Kinder:
            PV = KV_Bemessungssatz * PV_Beitragssatz * 0.5

        else:
            PV = KV_Bemessungssatz * (PV_Beitragssatz * 0.5 + Kinderlosenmalus)


    elif PKV:
        KV = PKV_Beitrag / 2
        PV = 0

    AV_Bemessungssatz = min(Bruttoeinkommen, AV_Beitragsbemessungsgrenze)
    AV = AV_Bemessungssatz * AV_Beitragssatz * 0.5


    if Arbeit_vs_Rente == 0:
        RV = 0

    else:
        RV_Bemessungssatz = min(Bruttoeinkommen, AV_Beitragsbemessungsgrenze)
        RV = RV_Bemessungssatz * RV_Beitragssatz * 0.5


    Vorsorgeaufwendungen = RV + KV + PV

    zvE = math.floor(Bruttoeinkommen - Vorsorgeaufwendungen)

    Lohnsteuer, Soli, Kirchensteuer = calc_steuern(zvE)

    Lohnsteuer = round(Lohnsteuer, 2)
    Soli = round(Soli, 2)
    Kirchensteuer = round(Kirchensteuer, 2)

    Nettoeinkommen = Bruttoeinkommen - KV - AV - PV - RV - Lohnsteuer - Soli - Kirchensteuer


    '''
    (Monatsbrutto / Bruttoeinkommen) sollte in der Regel 1 / 12 sein. Außer im Jahr des Renteneinstiegs...
    '''

    KV = round(KV * (Monatsbrutto / Bruttoeinkommen), 2)
    AV = round(AV * (Monatsbrutto / Bruttoeinkommen), 2)
    PV = round(PV * (Monatsbrutto / Bruttoeinkommen), 2)
    RV = round(RV * (Monatsbrutto / Bruttoeinkommen), 2)
    zvE = round(zvE * (Monatsbrutto / Bruttoeinkommen), 2)
    Lohnsteuer = round(Lohnsteuer * (Monatsbrutto / Bruttoeinkommen), 2)
    Soli = round(Soli * (Monatsbrutto / Bruttoeinkommen), 2)
    Kirchensteuer = round(Kirchensteuer * (Monatsbrutto / Bruttoeinkommen), 2)
    Nettoeinkommen = round(Nettoeinkommen * (Monatsbrutto / Bruttoeinkommen), 2)

    return KV, AV, PV, RV, zvE, Lohnsteuer, Soli, Kirchensteuer, Nettoeinkommen


def create_Prognose_df(BAV_Bruttobeitrag=0):
    df_Prognose = pd.DataFrame()

    '''
    Erstellt einen Index von Beginn des Jahres in dem die BAV startet bis zum Zeitpunkt X
    '''
    df_Prognose['Zeitraum'] = pd.date_range(start=datetime(BAV_Vertragsbeginn.year, 1, 1, 0, 0), end=datetime(Renteneintritt.year + 30, 12, 31, 0, 0), freq='M')
    df_Prognose['Zeitraum'] = pd.to_datetime(df_Prognose['Zeitraum'])
    df_Prognose.set_index(keys='Zeitraum', inplace=True, drop=True)

    '''
    Generiert eine fortlaufende Nummer
    '''
    df_Prognose.insert(0, 'Laufzeit', range(0, len(df_Prognose)))
    
    '''
    Boolean 1 = Ansparphase, 0 = Rentenphase
    '''
    df_Prognose['Arbeit_vs_Rente'] = 0
    df_Prognose['Arbeit_vs_Rente'].loc[:Renteneintritt] = 1

    df_Prognose['Vertrag'] = 0
    df_Prognose['Vertrag'].loc[BAV_Vertragsbeginn:Renteneintritt] = 1

    '''
    Implementiert das Wachstum des Bruttoeinkommens jedes Jahr. 
    '''
    df_Prognose['Bruttoeinkommenswachstum'] = np.nan
    df_Prognose['Bruttoeinkommenswachstum'].iloc[::12] = (1 + Bruttoeinkommen_Wachstum) ** (df_Prognose['Laufzeit']//12)
    df_Prognose['Bruttoeinkommenswachstum'].fillna(method='ffill', inplace=True)
    df_Prognose['Bruttoeinkommen'] = df_Prognose['Bruttoeinkommenswachstum'] * (Bruttoeinkommen)
    
    
    '''
    Berechnet die Rentenpunkte 
    '''
    df_Prognose['Rentenpunkte'] = df_Prognose['Bruttoeinkommen'].map(calc_rentenpunkte)


    '''
    korrigiert das Bruttoeinkomme in der Rente
    Es fehlt: Die Rente aus dem ETF / der BAV
    '''
    df_Prognose['Bruttoeinkommen'].loc[Renteneintritt + timedelta(days=1):] = (df_Prognose['Rentenpunkte'].loc[:Renteneintritt].sum() + RV_angesammelte_RP) * RV_RP_Wert

    '''
    Generiert eine Spalte mit den Brutto BAV Zahlungen
    '''
    df_Prognose['BAV_Bruttobeitrag'] = 0
    df_Prognose['BAV_Bruttobeitrag'].loc[BAV_Vertragsbeginn: Renteneintritt] = BAV_Bruttobeitrag / 12

    '''
    Berechnet das BAV_Bruttoeinkommen
    '''
    df_Prognose['BAV_Bruttoeinkommen'] = df_Prognose['Bruttoeinkommen'] - df_Prognose['BAV_Bruttobeitrag']
 
    '''
    Berechnet die Rentenpunkte mit BAV
    '''
    df_Prognose['BAV_Rentenpunkte'] = df_Prognose['BAV_Bruttoeinkommen'].map(calc_rentenpunkte)

    '''
    korrigiert das Bruttoeinkomme in der Rente
    Es fehlt: Die Rente aus dem ETF / der BAV
    '''
    df_Prognose['BAV_Bruttoeinkommen'].loc[Renteneintritt + timedelta(days=1):] = (df_Prognose['BAV_Rentenpunkte'].loc[:Renteneintritt].sum() + RV_angesammelte_RP) * RV_RP_Wert

    '''
    korrigiert die Rentenpunkte in der Rente
    '''
    df_Prognose['Rentenpunkte'].loc[Renteneintritt + timedelta(days=1):] = 0
    df_Prognose['BAV_Rentenpunkte'].loc[Renteneintritt + timedelta(days=1):] = 0

    '''
    Berechnet das entgültige Jahresbrutto
    '''
    df_Prognose['Jahresbrutto'] = df_Prognose['Bruttoeinkommen'].resample('Y').sum()
    df_Prognose['Jahresbrutto'].fillna(method='bfill', inplace=True)
    df_Prognose['Jahresbrutto'] = df_Prognose['Jahresbrutto'] + (1 - df_Prognose['Arbeit_vs_Rente'])
    
    df_Prognose['BAV_Jahresbrutto'] = df_Prognose['BAV_Bruttoeinkommen'].resample('Y').sum()
    df_Prognose['BAV_Jahresbrutto'].fillna(method='bfill', inplace=True)
    
    '''
    Berechnet die Sozialabgaben und das Nettoeinkommen
    '''
    df_Prognose['KV'], df_Prognose['AV'], df_Prognose['PV'], df_Prognose['RV'], df_Prognose['zvE'], df_Prognose['Lohnsteuer'], df_Prognose['Soli'], df_Prognose['Kirchensteuer'], df_Prognose['Nettoeinkommen'] = zip(*df_Prognose.apply(lambda x: calc_steuern_sozialabgaben(x['Jahresbrutto'], x['Bruttoeinkommen'], x['Arbeit_vs_Rente']), axis=1))
    _, _, _, _, _, _, _, _, df_Prognose['BAV_Nettoeinkommen'] = zip(*df_Prognose.apply(lambda x: calc_steuern_sozialabgaben(x['BAV_Jahresbrutto'], x['BAV_Bruttoeinkommen'], x['Arbeit_vs_Rente']), axis=1))

    '''
    Berechnet den mtl. Nettoaufwand der BAV
    '''
    df_Prognose['Jahresnetto'] = df_Prognose['Nettoeinkommen'].resample('Y').sum()
    df_Prognose['BAV_Jahresnetto'] = df_Prognose['BAV_Nettoeinkommen'].resample('Y').sum()
    df_Prognose['Vertragsmonate'] = df_Prognose['Vertrag'].resample('Y').sum()

    df_Prognose['Jahresnetto'] = df_Prognose['Jahresnetto'].fillna(method='bfill') * df_Prognose['Vertrag']
    df_Prognose['BAV_Jahresnetto'] = df_Prognose['BAV_Jahresnetto'].fillna(method='bfill') * df_Prognose['Vertrag']
    df_Prognose['Vertragsmonate'] = df_Prognose['Vertragsmonate'].fillna(method='bfill')

    df_Prognose['Nettoaufwand'] = (df_Prognose['Jahresnetto'] - df_Prognose['BAV_Jahresnetto']) / df_Prognose['Vertragsmonate']

    '''
    In diesem Abschnitt wird die Entwicklung eines ETF inkl. Steuern berechnet
    '''
    df_ETF = df_Prognose[['Nettoaufwand', 'Arbeit_vs_Rente']]
    
    df_ETF['Fondswert'] = 0
    df_ETF['Basisertrag'] = 0
    df_ETF['Vorabpauschale'] = 0
    df_ETF['Bruttoentnahme'] = 0
    df_ETF['TER'] = 0
    df_ETF['Steuerlast_Vorabpauschale'] = 0
    df_ETF['Steuerlast_Bruttoentnahme'] = 0
    df_ETF['Steuerlast_Gesamt'] = 0
    df_ETF['Nettoentnahme'] = 0
    df_ETF['Jahresnetto'] = np.nan
    
    df_ETF = calc_ETF_verlauf(df_ETF)

    '''
    Korrigiert das Jahresnetto um den Ertrag aus dem ETF
    '''
    df_Prognose['Nettoeinkommen'] = df_Prognose['Nettoeinkommen'] + df_ETF['Nettoentnahme']

    df_Prognose = pd.concat([df_Prognose, df_ETF], axis=1)

    return(df_Prognose)


if __name__ == "__main__":
    print("\n")
    print("!!!              Alle Angaben ohne Gewähr             !!!")
    print("        Dieses Angebot stellt keine Beratung dar.        ")
    print(" Die Berechnung erfolgt nach bestem Wissen und Gewissen. ")
    print("\n")

    time.sleep(10)
    
    df_Prognose = create_Prognose_df(BAV_Bruttobeitrag)
    print(df_Prognose)
    
    df_Prognose.to_csv('Prognose.csv', sep=';')
    print('Der gesamte Verlauf wurde als csv Datei gespeichert.')
    print("\n")
 
    print('Das Nettoeinkommen im Rentenalter mit einer Anlage in einen ETF beträgt voraussichtlich: ' + round(df_Prognose['Nettoeinkommen'].iloc[-1], 2).astype(str) + ' € pro Monat.')
    print('Das Nettoeinkommen im Rentenalter mit einer Anlage in eine BAV beträgt voraussichtlich: ' +round(df_Prognose['BAV_Nettoeinkommen'].iloc[-1], 2).astype(str) + ' € pro Monat. PLUS! der Nettorente aus der BAV.')
