#!/usr/bin/env python3
"""Screenshots aufraeumen: alte ins Archiv verschieben, sehr alte loeschen.

ACHTUNG: Dieses Skript LOESCHT Dateien im Archiv-Verzeichnis unwiderruflich.
Vor dem ersten echten Lauf immer erst mit --dry-run pruefen.
"""

import argparse
import logging
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# -------------------------------------------------------------
# Konfiguration -- hier anpassen oder per Umgebungsvariable setzen
# -------------------------------------------------------------

# Verzeichnis, in dem macOS die Bildschirmfotos ablegt
SCREENSHOT_DIR = Path(
    os.environ.get("SCREENSHOT_DIR", Path.home() / "Desktop" / "Bildschirmfotos")
)

# Archiv-Verzeichnis (Standard: Unterordner "Archiv")
ARCHIVE_DIR = Path(os.environ.get("ARCHIVE_DIR", SCREENSHOT_DIR / "Archiv"))

# Verzeichnis fuer die Logdateien
LOG_DIR = Path(os.environ.get("LOG_DIR", Path.home() / "CronTabs" / "ScreenshotHandler"))

# Nach so vielen Tagen wird eine Datei ins Archiv verschoben
ARCHIVE_AFTER_DAYS = int(os.environ.get("ARCHIVE_AFTER_DAYS", "10"))

# Nach so vielen Tagen wird eine Datei im Archiv geloescht
DELETE_AFTER_DAYS = int(os.environ.get("DELETE_AFTER_DAYS", "360"))

# -------------------------------------------------------------
# Logging-Setup
# -------------------------------------------------------------

script_name = Path(__file__).stem
this_month = datetime.now().strftime("%Y-%m")
log_path = LOG_DIR / f"{script_name}_{this_month}.log"
log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

# -------------------------------------------------------------
# Start des eigentlichen Programmes
# -------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Nur anzeigen, was passieren wuerde -- nichts verschieben oder loeschen",
    )
    args = parser.parse_args()

    if not SCREENSHOT_DIR.is_dir():
        logging.error("Screenshot-Verzeichnis nicht gefunden: %s", SCREENSHOT_DIR)
        return 1

    if not args.dry_run:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    archive_before = date.today() - timedelta(days=ARCHIVE_AFTER_DAYS)
    delete_before = date.today() - timedelta(days=DELETE_AFTER_DAYS)

    actuall = 0
    toArchive = 0
    inArchive = 0
    deleted = 0

    # Aktuelle Screenshots durchgehen und alte ins Archiv verschieben
    for file in SCREENSHOT_DIR.iterdir():
        if not file.is_file() or file.suffix.lower() != ".png":
            continue
        mdate = date.fromtimestamp(file.stat().st_mtime)
        if mdate <= archive_before:
            toArchive += 1
            if args.dry_run:
                logging.info("[dry-run] wuerde archivieren: %s", file.name)
            else:
                file.replace(ARCHIVE_DIR / file.name)
        else:
            actuall += 1

    # Archiv durchgehen und sehr alte Dateien loeschen
    if ARCHIVE_DIR.is_dir():
        for file in ARCHIVE_DIR.iterdir():
            if not file.is_file() or file.suffix.lower() != ".png":
                continue
            mdate = date.fromtimestamp(file.stat().st_mtime)
            if mdate <= delete_before:
                deleted += 1
                if args.dry_run:
                    logging.info("[dry-run] wuerde loeschen: %s", file.name)
                else:
                    file.unlink()
            else:
                inArchive += 1

    logging.info(
        "%sAktuelle Daten: %d, Verschobene Daten: %d, Archivierte Daten: %d, "
        "Geloeschte Daten: %d",
        "[dry-run] " if args.dry_run else "",
        actuall,
        toArchive,
        inArchive,
        deleted,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
