import os
import time
from datetime import datetime

filename = "_testbilder/testbild_3.png"

# Minimal gültiges 1x1 PNG
png_bytes = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
    b"\x00\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01\xe2!\xbc3"
    b"\x00\x00\x00\x00IEND\xaeB`\x82"
)

# PNG schreiben
with open(filename, "wb") as f:
    f.write(png_bytes)

# gewünschtes Datum
target_date = datetime(2024, 2, 20, 10, 30, 0)
timestamp = time.mktime(target_date.timetuple())

# Access- und Modified-Date setzen
os.utime(filename, (timestamp, timestamp))

print("PNG erstellt:", filename)
print("Datum gesetzt auf:", target_date)