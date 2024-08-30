from icalendar import Calendar
from datetime import timedelta


def check_for_keywords(time_spent, keywords, event, summary):
    # Überprüfe für jedes Schlüsselwort, ob es im Termin-Titel enthalten ist
    for keyword in keywords:
        if keyword.lower() in summary.lower():
            start = event.get("DTSTART").dt
            end = event.get("DTEND").dt
            time_spent[keyword.lower()] += end - start
    return time_spent

def get_overview(filename, categories):
    overview = dict()
    for key, value in categories.items():
        keywords = value.get('keywords')
        # Initialisiere ein Dictionary, um die Zeit für jedes Schlüsselwort zu speichern
        time_spent = {keyword.lower(): timedelta() for keyword in keywords}

        # Öffne die .ics-Datei und lese sie ein
        with open(filename, "r") as file:
            cal = Calendar.from_ical(file.read())

        # Iteriere durch alle Ereignisse im Kalender
        for event in cal.walk("VEVENT"):
            summary = event.get("SUMMARY")
            if not summary:
                return "no key events from calendar loaded, aborting.."
            time_spent = check_for_keywords(time_spent, keywords, event, summary)

        hours_spent = 0
        for _, time in time_spent.items():
            hours_spent += time.total_seconds() / 3600
        hours_spent = round(hours_spent, 2)
        cp_ratio = round(value.get('cp')/hours_spent, 5)
        overview[key] = {'hours_spent': hours_spent, 'cp_ratio': cp_ratio}
    return overview


# Beispiel: Ersetze 'calendar.ics' durch den Pfad zu deiner .ics-Datei und gib eine Liste von Schlüsselwörtern an.
categories = {
    "Systemtheorie": {
        "keywords": ["SigSys", "Signale und Systeme", "Regelungstechnik"],
        "cp": 9,
    },
    "GETII": {
        "keywords": ["Elektrotechnik", "GET"],
        "cp": 4
    },
    "Technologie- und Innovationsmanagement": {
        "keywords": ["TIM", "Technologie- und Innovationsmanagement",],
        "cp": 7.5,
    },
    "Data Literacy": {
        "keywords": ["Data Literacy"],
        "cp": 4
    },
    "Bierpong": {
        "keywords": ["Bierpong"],
        "cp": 100},
}
overview = get_overview(
    "Calendar-Studium@group.calendar.google.com.ics", categories
)

for keyword, elements in overview.items():
    print(f"'{keyword}': {elements}")
