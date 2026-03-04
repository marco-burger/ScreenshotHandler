import time

start = time.perf_counter()

from datetime import datetime

startingTimestamp = datetime.now()

import os
import time
from datetime import date, timedelta

import logging
import sys
from pathlib import Path

# -------------------------------------------------------------
# Pfad-Setup
# -------------------------------------------------------------

base_dir = Path(r"C:\Users\<USER>\Pictures\Screenshots")
archive_dir = base_dir / "Archiv"

archive_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# Logging-Setup
# -------------------------------------------------------------

# Name der aktuellen Python-Datei ohne .py
script_name = Path(__file__).stem

# Aktueller Monat formatieren (YYYY-MM)
this_month = datetime.now().strftime("%Y-%m")

# Logfile-Name erzeugen
log_filename = f"{script_name}_{this_month}.log"
log_path = Path(r"C:\Users\<USER>\CronTabs\ScreenshotHandler\logs") / log_filename
log_path.parent.mkdir(parents=True, exist_ok=True)  # Sicherstellen, dass der Ordner existiert 

# Logging konfigurieren
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)  # Ausgabe weiterhin in Konsole
    ]
)

# Beispiel-Ausgaben
# logging.info("Script gestartet")
# logging.debug("Debug-Information")
# logging.warning("Warnung!")
# logging.error("Fehler aufgetreten")

# -------------------------------------------------------------
# Start des eigentlichen Programmes
# ------------------------------------------------------------- 

today = date.today()
today = time.localtime()
today = time.strftime("%Y-%m-%d", today)

minus10days = date.today() - timedelta(10)

minus90days = date.today() - timedelta(90)

actuall = 0
toArchive = 0
inArchive = 0
deleted = 0

for file in base_dir.iterdir():
    if file.suffix.lower() == ".png":
        fts = file.stat().st_mtime
        fts_ctz = date.fromtimestamp(fts)
        if fts_ctz <= minus10days:
            toArchive += 1
            src_path = file
            dst_path = archive_dir / file.name
            file.replace(dst_path)
        else:
            actuall += 1

#Spezieller Fix für OneDrive: Alle Dateien im Archiv durchgehen und die alten Dateien löschen, da OneDrive sonst nicht mehr synchronisiert, wenn zu viele Dateien im Archiv liegen. Es werden nur die Dateien gelöscht, die älter als 90 Tage sind.
archive_files = [p for p in archive_dir.iterdir() if p.is_file() and p.suffix.lower() == ".png"]

for file_a in archive_files:
    mdate = date.fromtimestamp(file_a.stat().st_mtime)
    if mdate <= minus90days:
        deleted += 1
        file_a.unlink()
    else:
        inArchive += 1

logging.info("Aktuelle Daten: %d, Verschobene Daten: %d, Archivierte Daten: %d, Gelöschte Daten: %d", actuall, toArchive, inArchive, deleted)


