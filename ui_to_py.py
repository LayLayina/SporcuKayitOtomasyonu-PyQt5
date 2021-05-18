from PyQt5 import uic

with open('hakkındaUİ.py','w',encoding="utf-8") as fout:
    uic.compileUi('hakkında.ui',fout)