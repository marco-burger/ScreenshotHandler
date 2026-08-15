#!/usr/bin/env python3
"""Erzeugt eine minimale PNG-Testdatei mit frei waehlbarem Aenderungsdatum.

Damit laesst sich das Archivieren und Loeschen des ScreenshotHandlers in einem
Wegwerf-Verzeichnis durchspielen, ohne echte Screenshots zu riskieren.

Beispiele:
    python3 createTestFile.py /tmp/shots/alt.png --days-ago 400
    python3 createTestFile.py /tmp/shots/fix.png --date 2024-02-20
"""

import argparse
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Minimal gueltiges 1x1-PNG
PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
    b"\x00\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01\xe2!\xbc3"
    b"\x00\x00\x00\x00IEND\xaeB`\x82"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Zieldatei, z. B. /tmp/shots/alt.png")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--days-ago", type=int, help="Aenderungsdatum auf so viele Tage vor heute setzen"
    )
    group.add_argument("--date", help="Aenderungsdatum als YYYY-MM-DD")
    args = parser.parse_args()

    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print(f"Ungueltiges Datum: {args.date} (erwartet YYYY-MM-DD)", file=sys.stderr)
            return 1
    elif args.days_ago is not None:
        target_date = datetime.now() - timedelta(days=args.days_ago)
    else:
        target_date = datetime.now()

    args.path.parent.mkdir(parents=True, exist_ok=True)
    args.path.write_bytes(PNG_BYTES)

    timestamp = time.mktime(target_date.timetuple())
    os.utime(args.path, (timestamp, timestamp))

    print(f"PNG erstellt: {args.path}")
    print(f"Datum gesetzt auf: {target_date:%Y-%m-%d %H:%M:%S}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
