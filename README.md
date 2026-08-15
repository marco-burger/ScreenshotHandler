# ScreenshotHandler

Kleines Aufräum-Skript für Screenshot-Ordner: Bildschirmfotos, die älter als
ein paar Tage sind, wandern automatisch in ein Archiv-Unterverzeichnis. Dateien,
die dort sehr lange liegen, werden gelöscht. Gedacht für den Betrieb per
cron (macOS) bzw. Aufgabenplanung (Windows).

Reines Python 3, keine Abhängigkeiten außer der Standardbibliothek.

## ⚠️ Warnung

**Das Skript löscht Dateien unwiderruflich** — es verschiebt sie nicht in den
Papierkorb. Betroffen sind `.png`-Dateien im konfigurierten Archiv-Verzeichnis,
die älter als `DELETE_AFTER_DAYS` sind.

Vor dem ersten scharfen Lauf **immer** erst prüfen, was passieren würde:

```bash
python3 macos/screenshothandler.py --dry-run
```

Die Standardpfade zeigen auf die Verzeichnisse des ursprünglichen Autors bzw.
auf plattformübliche Standardorte. Prüfe sie, bevor du das Skript startest.

## Funktionsweise

| Alter der Datei | Was passiert |
|---|---|
| jünger als `ARCHIVE_AFTER_DAYS` (10 Tage) | bleibt liegen |
| älter als `ARCHIVE_AFTER_DAYS` | wird nach `ARCHIVE_DIR` verschoben |
| im Archiv, älter als `DELETE_AFTER_DAYS` | wird gelöscht |

Berücksichtigt werden ausschließlich Dateien mit der Endung `.png`.
Unterverzeichnisse und andere Dateitypen werden nicht angefasst.

## Konfiguration

Entweder direkt im Konfig-Block am Kopf des Skripts anpassen oder per
Umgebungsvariable überschreiben:

| Variable | Standard macOS | Standard Windows |
|---|---|---|
| `SCREENSHOT_DIR` | `~/Desktop/Bildschirmfotos` | `~/Pictures/Screenshots` |
| `ARCHIVE_DIR` | `$SCREENSHOT_DIR/Archiv` | `$SCREENSHOT_DIR/Archiv` |
| `LOG_DIR` | `~/CronTabs/ScreenshotHandler` | `~/CronTabs/ScreenshotHandler/logs` |
| `ARCHIVE_AFTER_DAYS` | `10` | `10` |
| `DELETE_AFTER_DAYS` | `360` | `90` |

Unter Windows ist `DELETE_AFTER_DAYS` bewusst kürzer: Liegt das Archiv in
einem OneDrive-Ordner, bricht dessen Synchronisation ab, wenn sich dort zu
viele Dateien ansammeln.

Beispiel:

```bash
SCREENSHOT_DIR=~/Desktop/Screenshots ARCHIVE_AFTER_DAYS=30 python3 macos/screenshothandler.py --dry-run
```

## Einrichtung

### macOS (cron)

Siehe [macos/crontab-readme.info](macos/crontab-readme.info). Kurzfassung —
stündlich ausführen:

```bash
crontab -e
```

Eintrag:

```
0 * * * * /usr/bin/python3 "$HOME/CronTabs/ScreenshotHandler/screenshothandler.py"
```

Hinweis: cron braucht unter aktuellen macOS-Versionen die Berechtigung
„Festplattenvollzugriff", um auf `~/Desktop` zugreifen zu dürfen
(Systemeinstellungen → Datenschutz & Sicherheit).

### Windows (Aufgabenplanung)

[windows/screenshothandler.bat](windows/screenshothandler.bat) als Aufgabe
hinterlegen. Die Batch-Datei ruft das Python-Skript auf und hängt die Ausgabe
an ein Logfile an.

## Tests

[createTestFile.py](createTestFile.py) erzeugt minimale PNG-Dateien mit frei
wählbarem Änderungsdatum, um das Archivieren und Löschen gefahrlos in einem
Wegwerf-Verzeichnis durchzuspielen:

```bash
python3 createTestFile.py /tmp/shots/alt.png --days-ago 400
```

## Lizenz

[MIT](LICENSE)
