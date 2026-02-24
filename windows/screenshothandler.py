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

yesterday = date.today() - timedelta(10)

yesterday2 = date.today() - timedelta(90)

actuall = 0
older = 0
toOld = 0

for file in base_dir.iterdir():
    if file.suffix.lower() == ".png":
        fts = file.stat().st_mtime
        fts_ctz = date.fromtimestamp(fts)
        if fts_ctz <= yesterday:
            older += 1
            src_path = file
            dst_path = archive_dir / file.name
            file.replace(dst_path)
        else:
            actuall += 1

for file in archive_dir.iterdir():
    fts_ctz = date.fromtimestamp(file.stat().st_mtime)
    fts_ctz = date.fromtimestamp(fts)
    if fts_ctz <= yesterday2:
        toOld += 1
        file.unlink()
    else:
        older += 1

logging.info("Aktuelle Daten: %d, Veralterte Daten: %d, Gelöschte Daten: %d", actuall, older, toOld)


