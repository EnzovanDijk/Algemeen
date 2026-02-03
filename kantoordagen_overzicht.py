#!/usr/bin/env python3
"""
Overzicht kantoordagen en afwezigheid
Startdatum: mei 2025
"""

from datetime import date, timedelta
from collections import defaultdict

# Nederlandse feestdagen 2025-2026
FEESTDAGEN = {
    date(2025, 5, 1): "Dag van de Arbeid",  # Niet altijd vrij in NL
    date(2025, 5, 5): "Bevrijdingsdag",
    date(2025, 5, 29): "Hemelvaartsdag",
    date(2025, 6, 8): "Eerste Pinksterdag",
    date(2025, 6, 9): "Tweede Pinksterdag",
    date(2025, 12, 25): "Eerste Kerstdag",
    date(2025, 12, 26): "Tweede Kerstdag",
    date(2026, 1, 1): "Nieuwjaarsdag",
}

# Afwezigheidsdagen
AFWEZIGHEID = {
    date(2025, 8, 18): "Verlof (vakantie)",
    date(2025, 8, 19): "Verlof (vakantie)",
    date(2025, 8, 20): "Verlof (vakantie)",
    date(2025, 8, 21): "Verlof (vakantie)",
    date(2025, 8, 22): "Verlof (vakantie)",
    date(2025, 9, 2): "Ziek",
    date(2025, 9, 3): "Ziek",
    date(2025, 9, 4): "Ziek",
    date(2025, 10, 9): "Ziek",
    date(2025, 10, 10): "Ziek",
    date(2025, 11, 24): "Ziek",
    date(2025, 11, 25): "Ziek",
    date(2025, 11, 26): "Ziek",
    date(2025, 12, 18): "Verlof (vakantie)",
    date(2025, 12, 19): "Verlof (vakantie)",
    date(2025, 12, 22): "Verlof (vakantie)",
    date(2025, 12, 23): "Verlof (vakantie)",
    date(2025, 12, 31): "Verlof (vakantie, halve dag 13:00-16:00)",
    date(2026, 1, 21): "Ziek",
    date(2026, 1, 22): "Ziek",
    date(2026, 1, 23): "Ziek",
}

def is_werkdag(d):
    """Check of een datum een werkdag is (ma-vr, geen feestdag)"""
    return d.weekday() < 5 and d not in FEESTDAGEN

def get_weekday_name(d):
    """Geef Nederlandse dagnaam"""
    dagen = ["ma", "di", "wo", "do", "vr", "za", "zo"]
    return dagen[d.weekday()]

def bereken_overzicht():
    start_datum = date(2025, 5, 14)  # Eerste werkdag
    eind_datum = date(2026, 1, 31)

    maand_namen = {
        1: "januari", 2: "februari", 3: "maart", 4: "april",
        5: "mei", 6: "juni", 7: "juli", 8: "augustus",
        9: "september", 10: "oktober", 11: "november", 12: "december"
    }

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

                if huidige_datum in AFWEZIGHEID:
                    resultaten[maand_key]["afwezigheid"].append(
                        f"  {huidige_datum.day:2d}-{huidige_datum.month:02d} ({get_weekday_name(huidige_datum)}): {AFWEZIGHEID[huidige_datum]}"
                    )
                else:
                    resultaten[maand_key]["kantoordagen"] += 1

        huidige_datum += timedelta(days=1)

    # Print overzicht
    print("=" * 70)
    print("OVERZICHT KANTOORDAGEN EN AFWEZIGHEID")
    print("Periode: mei 2025 - januari 2026")
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
    print()

if __name__ == "__main__":
    bereken_overzicht()
