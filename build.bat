@echo off
cd C:\Users\jdy26\Documents\GitHub\Mizmaster-S9
pyinstaller --onefile --noconsole --add-data "C:\Users\jdy26\Documents\GitHub\Mizmaster-S9\henchies.xlsx;." --add-data "C:\Users\jdy26\Documents\GitHub\Mizmaster-S9\헨치사진;헨치사진" --hidden-import openpyxl Mixmaster_S9.py
pause
