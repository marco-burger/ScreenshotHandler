import os
import time
from datetime import date, timedelta

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

print("Aktuelle Daten: ", actuall , " Veralterte Daten: ", older, " Gelöschte Daten: ", toOld)