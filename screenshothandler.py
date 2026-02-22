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
# Logging-Setup
# -------------------------------------------------------------

# Name der aktuellen Python-Datei ohne .py
script_name = Path(__file__).stem

# Aktueller Monat formatieren (YYYY-MM)
this_month = datetime.now().strftime("%Y-%m")

# Logfile-Name erzeugen
log_filename = f"{script_name}_{this_month}.log"
log_path = Path("/Users/marcoburger/CronTabs/ScreenshotHandler") / log_filename
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

cwd = os.getcwd()

#print("Current working directory: ", cwd)

cwd = os.chdir("/Users/marcoburger/Desktop/Bildschirmfotos")
cwd = os.getcwd()

#print("Current working directory: ", cwd)

today = date.today()
today = time.localtime()
today = time.strftime("%Y-%m-%d", today)

yesterday = date.today() - timedelta(10)

yesterday2 = date.today() - timedelta(360)

#print(today)
#print(yesterday)

actuall = 0
older = 0
toOld = 0

archiveDIR = "/Users/marcoburger/Desktop/Bildschirmfotos/Archiv/"

for x in os.listdir():
    if x.endswith(".png"):
        # Prints only text file present in My Folder
        #print(x)
        fts = os.path.getmtime(x)
        fts_ctz = date.fromtimestamp(fts)
        #fts_ctz_date = time.strftime("%Y-%m-%d", fts_ctz)
        #print(fts_ctz)
        if fts_ctz <= yesterday:
            older += 1
            src_path = os.path.join(cwd, x)
            dst_path = os.path.join(archiveDIR, x)
            os.rename(src_path, dst_path)
        else:
            actuall += 1


cwd = os.chdir("/Users/marcoburger/Desktop/Bildschirmfotos/Archiv")
cwd = os.getcwd()

#print("Current working directory: ", cwd)
for x in os.listdir():
    fts = os.path.getmtime(x)
    fts_ctz = date.fromtimestamp(fts)
    if fts_ctz <= yesterday2:
        toOld += 1
        os.remove(x)
    else:
        older += 1

logging.info("Aktuelle Daten: %d, Veralterte Daten: %d, Gelöschte Daten: %d", actuall, older, toOld)


