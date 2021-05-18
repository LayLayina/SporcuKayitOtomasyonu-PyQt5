#--------------------------------KÜTÜPHANE--------------------------------#
#-------------------------------------------------------------------------#
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from AnaSayfaUİ import *
from hakkındaUİ import *
from PyQt5.QtWidgets import QDialog
#--------------------------------UYGULAMA OLUŞTUR--------------------------------#
#--------------------------------------------------------------------------------#
Uygulama= QApplication(sys.argv)
penAna= QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()

penhakkında=QDialog()
ui2=Ui_Dialog()
ui2.setupUi(penhakkında)

#--------------------------------VERİTABANI OLUŞTUR--------------------------------#
#----------------------------------------------------------------------------------#
import sqlite3
global curs
global conn
conn=sqlite3.connect('veritabanı.db')
curs=conn.cursor()
sorguCreTblSpor=("CREATE TABLE IF NOT EXISTS spor(                 \
                 Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    \
                 TCNo TEXT NOT NULL UNIQUE,                        \
                 SporcuAdi TEXT NOT NULL,                          \
                 SporcuSoyadi TEXT NOT NULL,                       \
                 KulupAdi TEXT NOT NULL,                           \
                 Brans TEXT NOT NULL,                              \
                 Cinsiyet TEXT NOT NULL,                           \
                 DTarihi TEXT NOT NULL,                            \
                 MHal TEXT NOT NULL,                               \
                 Kilo TEXT NOT NULL)")
curs.execute(sorguCreTblSpor)
conn.commit()


#--------------------------------KAYDET-----------------------------------#
#-------------------------------------------------------------------------#
def EKLE():
    _lneTCK=ui.lneTCK.text()
    _lneSporcuAdi=ui.lneSporcuAdi.text()
    _lneSporcuSoyadi=ui.lneSporcuSoyadi.text()
    _cmbSporKulubu=ui.cmbSporKulb.currentText()
    _lwBrans=ui.lwBrans.currentItem().text()
    _cmbCinsiyet=ui.cmbCinsiyet.currentText()
    _cwDTarihi=ui.cwDTarihi.selectedDate().toString(QtCore.Qt.ISODate)
    if ui.chkMedeniHal.isChecked():
        _medeniHal="Evli"
    else:
        _medeniHal="Bekar"
    _spnKilo=ui.spnKilo.value()

    curs.execute("INSERT INTO spor \
                      (TCNo,SporcuAdi,SporcuSoyadi,KulupAdi,Brans,Cinsiyet,DTarihi,MHal,Kilo)\
                       VALUES (?,?,?,?,?,?,?,?,?)",\
                       (_lneTCK,_lneSporcuAdi,_lneSporcuSoyadi,_cmbSporKulubu,_lwBrans,_cmbCinsiyet,_cwDTarihi,_medeniHal,_spnKilo))
    conn.commit()
    LISTELE()

#--------------------------------LİSTELE---------------------------------------#
#------------------------------------------------------------------------------#
def LISTELE():
    ui.tblwBilgiler.clear()
    ui.tblwBilgiler.setHorizontalHeaderLabels(('No','TC Kimlik No','Sporcu Adı','Sporcu Soyadı',
                                               'Kulüp Adı','Branş','Cinsiyet','Doğum Tarihi',
                                               'Medeni Hal','Sporcu Kilosu'))

    ui.tblwBilgiler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    curs.execute("SELECT * FROM spor")
    for satirIndeks,satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate(satirVeri):
            ui.tblwBilgiler.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    ui.lneTCK.clear()
    ui.lneSporcuAdi.clear()
    ui.lneSporcuSoyadi.clear()
    ui.cmbSporKulb.setCurrentIndex(-1)
    ui.spnKilo.setValue(50)


    curs.execute("SELECT COUNT (*) FROM spor ")
    kayitSayisi=curs.fetchone()
    ui.lblkayitsayisi.setText(str(kayitSayisi[0]))

    curs.execute("SELECT AVG(Kilo) FROM spor")
    ortKilo=curs.fetchone()
    ui.lblOrtKilo.setText(str(ortKilo[0]))



LISTELE()


#----------------------------------ÇIKIŞ---------------------------------------#
#------------------------------------------------------------------------------#

def CIKIS():
    cevap = QMessageBox.question(penAna,"ÇIKIŞ","Programdan çıkmak istediğinize emin misiniz?",
                         QMessageBox.Yes | QMessageBox.No)
    if cevap == QMessageBox.Yes:
        conn.close()
        sys.exit(Uygulama.exec_())
    else:
        penAna.show()

#----------------------------------SİL-----------------------------------------#
#------------------------------------------------------------------------------#

def SIL():
    cevap = QMessageBox.question(penAna, "KAYIT SİL", "Kaıyıtı Silmek İstediğinize emin misiniz?",
                                 QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        secili=ui.tblwBilgiler.selectedItems()
        silinecek=secili[1].text()
        try:
            curs.execute("DELETE FROM spor WHERE TCNo='%s'"%(silinecek))
            conn.commit()
            LISTELE()
            ui.statusbar.showMessage("Kayıt Silme İşlemi Başarıyla Gerçekleşti...",5000)
        except Exception as Hata:
            ui.statusbar.showMessage("Şöyle Bir Hata İle Karşılaşıldı:"+str(Hata))
    else:
        ui.statusbar.showMessage("Kayıt Silme İşlemi İptal Edildi...", 5000)
        penAna.show()

#----------------------------------ARAMA-----------------------------------------#
#--------------------------------------------------------------------------------#

def ARA():
    aranan1=ui.lneTCK.text()
    aranan2=ui.lneSporcuAdi.text()
    aranan3=ui.lneSporcuSoyadi.text()
    curs.execute("SELECT * FROM spor WHERE TCNo=? OR SporcuAdi=? OR SporcuSoyadi=? OR (SporcuAdi=? AND SporcuSoyadi=?)",
                 (aranan1,aranan2,aranan3,aranan2,aranan3))
    conn.commit()
    ui.tblwBilgiler.clear()
    for satirIndeks,satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate(satirVeri):
            ui.tblwBilgiler.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))

#---------------------------------DOLDUR---------------------------------------#
#------------------------------------------------------------------------------#
def DOLDUR():
    secili=ui.tblwBilgiler.selectedItems()
    ui.lneTCK.setText(secili[1].text())
    ui.lneSporcuAdi.setText(secili[2].text())
    ui.lneSporcuSoyadi.setText(secili[3].text())
    ui.cmbSporKulb.setCurrentText(secili[4].text())
    if secili[5].text()=="Güreş":
        ui.lwBrans.item(0).setSelected(True)
        ui.lwBrans.setCurrentItem(ui.lwBrans.item(0))
    if secili[5].text()=="Box":
        ui.lwBrans.item(1).setSelected(True)
        ui.lwBrans.setCurrentItem(ui.lwBrans.item(1))
    if secili[5].text()=="Karate":
        ui.lwBrans.item(2).setSelected(True)
        ui.lwBrans.setCurrentItem(ui.lwBrans.item(2))
    if secili[5].text()=="Tekvando":
        ui.lwBrans.item(3).setSelected(True)
        ui.lwBrans.setCurrentItem(ui.lwBrans.item(3))
    if secili[5].text()=="Futbol":
        ui.lwBrans.item(4).setSelected(True)
        ui.lwBrans.setCurrentItem(ui.lwBrans.item(4))

    ui.cmbCinsiyet.setCurrentText(secili[6].text())

    yil=int(secili[7].text()[0:4])
    ay = int(secili[7].text()[5:7])
    gun = int(secili[7].text()[8:10])
    ui.cwDTarihi.setSelectedDate(QtCore.QDate(yil,ay,gun))

    if secili[8].text()=="Evli":
        ui.chkMedeniHal.setChecked(True)
    else:
        ui.chkMedeniHal.setChecked(False)

    ui.spnKilo.setValue(int(secili[9].text()))

#--------------------------------GÜNCELLE--------------------------------------#
#------------------------------------------------------------------------------#

def GUNCELLE():
    cevap = QMessageBox.question(penAna, "KAYIT GÜNCELLE", "Kaıyıtı Güncellemek İstediğinize emin misiniz?",
                                 QMessageBox.Yes | QMessageBox.No)
    if cevap == QMessageBox.Yes:
        try:
            secili = ui.tblwBilgiler.selectedItems()
            _Id = secili[0]
            _lneTCK = ui.lneTCK.text()
            _lneSporcuAdi = ui.lneSporcuAdi.text()
            _lneSporcuSoyadi = ui.lneSporcuSoyadi.text()
            _cmbSporKulubu = ui.cmbSporKulb.currentText()
            _lwBrans = ui.lwBrans.currentItem().text()
            _cmbCinsiyet = ui.cmbCinsiyet.currentText()
            _cwDTarihi = ui.cwDTarihi.selectedDate().toString(QtCore.Qt.ISODate)
            if ui.chkMedeniHal.isChecked():
                _medeniHal = "Evli"
            else:
                _medeniHal = "Bekar"
            _spnKilo = ui.spnKilo.value()

            curs.execute("UPDATE spor SET TCNo=?, SporcuAdi=?, SporcuSoyadi=?, Kilo=?, KulupAdi=?, Brans=?, Cinsiyet=?, DTarihi=?, MHal=? WHERE Id=?",
                         (_lneTCK,_lneSporcuAdi,_lneSporcuSoyadi,_spnKilo,_cmbSporKulubu,_lwBrans,_cmbCinsiyet,_cwDTarihi,_medeniHal,_Id))

            conn.commit()

            LISTELE()


        except Exception as Hata:
            ui.statusbar.showMessage("Söyle Bir Hata Meydana Geldi"+str(Hata),10000)
    else:
        ui.statusbar.showMessage("Güncelleme İptal Edildi",5000)

#--------------------------------HAKKINDA--------------------------------------#
#------------------------------------------------------------------------------#
def HAKKINDA():
    penhakkında.show()


#--------------------------------SİNYAL-SLOT-----------------------------------#
#------------------------------------------------------------------------------#
ui.btnEkle.clicked.connect(EKLE)
ui.btnListele.clicked.connect(LISTELE)
ui.btnCiks.clicked.connect(CIKIS)
ui.btnSil.clicked.connect(SIL)
ui.btnAra.clicked.connect(ARA)
ui.tblwBilgiler.itemSelectionChanged.connect(DOLDUR)
ui.btnGuncelle.clicked.connect(GUNCELLE)
ui.menhakinda.triggered.connect(HAKKINDA)

sys.exit(Uygulama.exec_())


