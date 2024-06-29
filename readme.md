pip install pillow pandas

pyinstaller --onefile --noconsole --add-data "henchies.xlsx;." --add-data "헨치사진;헨치사진" --hidden-import openpyxl Mixmaster_S9.py
