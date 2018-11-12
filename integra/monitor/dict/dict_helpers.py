import csv
from pathlib import Path
from integra.monitor.dict.slow import Event


def get_event_category(k):
    switcher = {
        'A': 'ALARM',
        'Z': 'ZAŁĄCZENIE CZUWANIA - wymagana interwencja obsługi stacji',
        'W': 'WYŁĄCZENIE CZUWANIA - nie wymaga interwencji, ster.wsk.czuwania',
        'F': 'AWARIA - wymagana interwencja, ster.wsk.awarii',
        'N': 'KONIEC AWARII - nie wymaga interwencji, ster.wsk.awarii',
        'T': 'TEST - interwencja przy braku kodu o określonym czasie',
        'U': 'UWAGA - sygnalizowane, ale nie wymaga interwencji',
        'P': 'POZOSTALE - nie wymaga interwencji',
    }
    return switcher.get(k, "")


def load_slow():
    f = open(str(Path(__file__).parent.absolute()) + "/CID.PL.txt", 'r')
    slow = dict()
    try:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0 and not row[0].startswith(';'):

                q = int(row[0])
                xyz = int(row[1])

                if xyz not in slow:
                    slow[xyz] = dict()
                slow[xyz][q] = Event(row[3], row[2], row[4])
    finally:
        f.close()

    return slow


def format_s_field(s_field, ccc, ss):
    switcher = {
        'i': 'Numer strefy: {0}, numer wejscia (czujki): {1}'.format(ss, ccc),
        'u': 'Numer strefy: {0}, numer użytkownika: {1}'.format(ss, ccc),
        's': 'Numer strefy: {0}'.format(ss),
        'v': 'Numer użytkownika: {0}'.format(ccc),
        'e': 'Numer strefy: {0}, numer expandera: {1}'.format(ss, ccc),
        'x': 'Zdarzenie systemowe',
    }

    return switcher.get(s_field, "")
