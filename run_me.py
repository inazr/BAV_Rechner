import pandas as pd
from datetime import datetime
from datetime import timedelta
from personal_info import person
import math

GKV_Beitragssatz = 0.146
AV_Beitragssatz = 0.024
RV_Beitragssatz = 0.186
PV_Beitragssatz = 0.0305
Kinderlosenmalus = 0.0025

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


if __name__ == "__main__":
    print("YOUR MILEAGE MY VARY!")

    KV, AV, PV, RV, zvE, Lohnsteuer, Soli, Kirchensteuer, Nettoeinkommen = calc_steuern_sozialabgaben(person['Bruttoeinkommen'], person['GKV'], person['GKV Zusatzbeitrag'], person['PKV'], person['PKV Beitrag'], person['Kinder'], person['Kirchensteuer'])
