@echo off
REM Pfade an die eigene Umgebung anpassen.
REM %USERPROFILE% zeigt auf das Benutzerverzeichnis, z. B. C:\Users\name

set SCRIPT=%USERPROFILE%\CronTabs\ScreenshotHandler\screenshothandler.py
set LOG=%USERPROFILE%\CronTabs\ScreenshotHandler\logs\run.log

if not exist "%USERPROFILE%\CronTabs\ScreenshotHandler\logs" mkdir "%USERPROFILE%\CronTabs\ScreenshotHandler\logs"

py -3 "%SCRIPT%" >> "%LOG%" 2>&1
