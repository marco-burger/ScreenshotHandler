@echo off
set SCRIPT=C:\Users\<USER>\CronTabs\ScreenshotHandler\screenshothandler.py
set LOG=C:\Users\<USER>\CronTabs\ScreenshotHandler\logs\run.log

py -3.14 "%SCRIPT%" >> "%LOG%" 2>&1