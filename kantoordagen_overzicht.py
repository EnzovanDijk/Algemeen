#!/usr/bin/env python3
"""
Overzicht kantoordagen en afwezigheid
Startdatum: 14 mei 2025

Gebruik:
  1. Voeg afwezigheidsdagen toe aan afwezigheid.csv
  2. Voer uit: python3 kantoordagen_overzicht.py
"""

import csv
import os
from datetime import date, timedelta
from collections import defaultdict

# Pad naar dit script (voor relatieve paden)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AFWEZIGHEID_CSV = os.path.join(SCRIPT_DIR, "afwezigheid.csv")

# Nederlandse feestdagen 2025-2026
FEESTDAGEN = {
    # 2025
    date(2025, 1, 1): "Nieuwjaarsdag",
    date(2025, 4, 18): "Goede Vrijdag",
    date(2025, 4, 20): "Eerste Paasdag",
    date(2025, 4, 21): "Tweede Paasdag",
    date(2025, 4, 27): "Koningsdag",
    date(2025, 5, 5): "Bevrijdingsdag",
    date(2025, 5, 29): "Hemelvaartsdag",
    date(2025, 6, 8): "Eerste Pinksterdag",
    date(2025, 6, 9): "Tweede Pinksterdag",
    date(2025, 12, 25): "Eerste Kerstdag",
    date(2025, 12, 26): "Tweede Kerstdag",
    # 2026
    date(2026, 1, 1): "Nieuwjaarsdag",
    date(2026, 4, 3): "Goede Vrijdag",
    date(2026, 4, 5): "Eerste Paasdag",
    date(2026, 4, 6): "Tweede Paasdag",
    date(2026, 4, 27): "Koningsdag",
    date(2026, 5, 5): "Bevrijdingsdag",
    date(2026, 5, 14): "Hemelvaartsdag",
    date(2026, 5, 24): "Eerste Pinksterdag",
    date(2026, 5, 25): "Tweede Pinksterdag",
    date(2026, 12, 25): "Eerste Kerstdag",
    date(2026, 12, 26): "Tweede Kerstdag",
}

def laad_afwezigheid():
    """Laad afwezigheidsdagen uit CSV bestand"""
    afwezigheid = {}

    if not os.path.exists(AFWEZIGHEID_CSV):
        print(f"Let op: {AFWEZIGHEID_CSV} niet gevonden. Maak dit bestand aan.")
        return afwezigheid

    with open(AFWEZIGHEID_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(
            (row for row in f if not row.startswith('#')),
            fieldnames=['datum', 'reden', 'opmerking']
        )

        for row in reader:
            if row['datum'] == 'datum':  # Skip header
                continue

            try:
                dag, maand, jaar = row['datum'].split('-')
                d = date(int(jaar), int(maand), int(dag))

                reden = row['reden'].strip().lower()
                opmerking = row['opmerking'].strip() if row['opmerking'] else ""

                if reden == 'verlof':
                    label = f"Verlof ({opmerking})" if opmerking else "Verlof"
                elif reden == 'ziek':
                    label = f"Ziek ({opmerking})" if opmerking else "Ziek"
                else:
                    label = f"{reden.capitalize()} ({opmerking})" if opmerking else reden.capitalize()

                afwezigheid[d] = label

            except (ValueError, AttributeError) as e:
                print(f"Waarschuwing: ongeldige regel overgeslagen: {row}")

    return afwezigheid

def get_weekday_name(d):
    """Geef Nederlandse dagnaam"""
    dagen = ["ma", "di", "wo", "do", "vr", "za", "zo"]
    return dagen[d.weekday()]

def bereken_overzicht():
    start_datum = date(2025, 5, 14)  # Eerste werkdag

    # Einddatum: laatste dag van huidige maand
    vandaag = date.today()
    if vandaag.month == 12:
        eind_datum = date(vandaag.year + 1, 1, 1) - timedelta(days=1)
    else:
        eind_datum = date(vandaag.year, vandaag.month + 1, 1) - timedelta(days=1)

    maand_namen = {
        1: "januari", 2: "februari", 3: "maart", 4: "april",
        5: "mei", 6: "juni", 7: "juli", 8: "augustus",
        9: "september", 10: "oktober", 11: "november", 12: "december"
    }

    # Laad afwezigheid uit CSV
    afwezigheid = laad_afwezigheid()

    resultaten = defaultdict(lambda: {
        "werkdagen_totaal": 0,
        "kantoordagen": 0,
        "afwezigheid": [],
        "feestdagen": []
    })

    huidige_datum = start_datum
    while huidige_datum <= eind_datum:
        maand_key = f"{huidige_datum.year}-{huidige_datum.month:02d}"

        if huidige_datum.weekday() < 5:  # Ma-vr
            if huidige_datum in FEESTDAGEN:
                resultaten[maand_key]["feestdagen"].append(
                    f"  {huidige_datum.day:2d}-{huidige_datum.month:02d} ({get_weekday_name(huidige_datum)}): {FEESTDAGEN[huidige_datum]}"
                )
            else:
                resultaten[maand_key]["werkdagen_totaal"] += 1

                if huidige_datum in afwezigheid:
                    resultaten[maand_key]["afwezigheid"].append(
                        f"  {huidige_datum.day:2d}-{huidige_datum.month:02d} ({get_weekday_name(huidige_datum)}): {afwezigheid[huidige_datum]}"
                    )
                else:
                    resultaten[maand_key]["kantoordagen"] += 1

        huidige_datum += timedelta(days=1)

    # Print overzicht
    print("=" * 70)
    print("OVERZICHT KANTOORDAGEN EN AFWEZIGHEID")
    print(f"Periode: {maand_namen[start_datum.month]} {start_datum.year} - {maand_namen[eind_datum.month]} {eind_datum.year}")
    print("=" * 70)
    print()

    totaal_werkdagen = 0
    totaal_kantoordagen = 0
    totaal_verlof = 0
    totaal_ziek = 0

    for maand_key in sorted(resultaten.keys()):
        jaar, maand = maand_key.split("-")
        maand_naam = maand_namen[int(maand)]
        data = resultaten[maand_key]

        print(f"📅 {maand_naam.upper()} {jaar}")
        print("-" * 40)
        print(f"  Werkdagen in maand:    {data['werkdagen_totaal']:3d}")
        print(f"  Kantoordagen:          {data['kantoordagen']:3d}")

        afwezig_count = len(data['afwezigheid'])
        if afwezig_count > 0:
            print(f"  Afwezig:               {afwezig_count:3d}")
            for item in data['afwezigheid']:
                print(item)
                if "Verlof" in item:
                    totaal_verlof += 1
                elif "Ziek" in item:
                    totaal_ziek += 1

        if data['feestdagen']:
            print(f"  Feestdagen:")
            for item in data['feestdagen']:
                print(item)

        totaal_werkdagen += data['werkdagen_totaal']
        totaal_kantoordagen += data['kantoordagen']

        print()

    print("=" * 70)
    print("SAMENVATTING")
    print("=" * 70)
    print(f"  Totaal werkdagen:      {totaal_werkdagen:3d}")
    print(f"  Totaal kantoordagen:   {totaal_kantoordagen:3d}")
    print(f"  Totaal verlof:         {totaal_verlof:3d} dagen")
    print(f"  Totaal ziek:           {totaal_ziek:3d} dagen")
    print()
    print("💡 Voor reiskostendeclaratie: gebruik het aantal KANTOORDAGEN per maand")
    print(f"📝 Afwezigheid bijwerken: bewerk {AFWEZIGHEID_CSV}")
    print()

if __name__ == "__main__":
    bereken_overzicht()
