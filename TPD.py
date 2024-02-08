import sys
from PyQt5.QtWidgets import QWidget,QApplication,QLabel,QVBoxLayout,QHBoxLayout,QPushButton,QTextEdit,QAction
from PyQt5.QtWidgets import QScrollArea,QToolButton,QWidgetAction,QMenu,QMainWindow,QDialog
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QSize,Qt
from time import sleep as uyu
from random import random,randint
import requests
import urllib.parse
from bs4 import BeautifulSoup
import win32gui, win32con

hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)

def klasik_dosya_oku(dosya_ismi):
    dosya = open(dosya_ismi, "a+", encoding="utf-8")
    dosya.close()
    dosya = open(dosya_ismi, "r", encoding="utf-8")
    satirlar = dosya.read()
    satirlar = satirlar.splitlines()
    dosya.close()
    return satirlar

def hatali_kelime_ekle(kelime,hatali_kelimeler_dosyasi_konumu):

    dosya=open(hatali_kelimeler_dosyasi_konumu,"a+",encoding="utf-8")
    dosya.close()
    dosya=open(hatali_kelimeler_dosyasi_konumu,"r",encoding="utf-8")
    kelimeler=dosya.read()
    kelimeler=kelimeler.splitlines()
    dosya.close()

    if kelime not in kelimeler:
        dosya = open(hatali_kelimeler_dosyasi_konumu, "a+", encoding="utf-8")
        dosya.write(kelime)
        dosya.write("\n")
        dosya.close()
        print("Hatalı kelime '{}' eklendi".format(kelime))
    else:
        print("Hatalı kelime '{}' zaten bulunuyor".format(kelime))

def dosyaya_kaydet(yazilacak_dosya_konumu,hatali_kelime_dosyasi,Tureng_icin_sayi,*args):
    dosya=open(yazilacak_dosya_konumu,"a+",encoding="utf-8")
    dosya.close()
    dosya=open(yazilacak_dosya_konumu,"r",encoding="utf-8")
    onceden_aranmislar = []
    satirlar = dosya.read()
    satirlar = satirlar.splitlines()
    dosya.close()
    for i in satirlar:
        i = i.split("***")
        onceden_aranmislar.append(str(i[0]).strip())

    def varmi(deger):
        deger=str(deger).strip().lower()
        if deger in onceden_aranmislar:
            return True
        else:
            return False

    dosya=open(yazilacak_dosya_konumu,"a+",encoding="utf-8")
    for i in args:
        if (type(i)==type(list())):
            for k in i:
                k=str(k).lower()
                if not varmi(k):
                    Tureng_verisi=Tureng_ciktisi(k, Tureng_icin_sayi)
                    if Tureng_verisi:
                        dosya.write(k.rstrip(" ") + "***")
                        for listeler in Tureng_verisi:
                            for anlamlarvs in listeler:
                                dosya.write(anlamlarvs)
                                dosya.write("+++")
                            dosya.write("---")
                        print("Kaydedilen kelime", k)
                        dosya.write("\n")

                    else:
                        hatali_kelime_ekle(k, hatali_kelime_dosyasi)

                    uyu(randint(0, 1) + round(random(), 2))
        else:
            i=str(i).lower()
            if not varmi(i):
                Tureng_verisi = Tureng_ciktisi(i, Tureng_icin_sayi)
                if Tureng_verisi:
                    dosya.write(i.rstrip(" ") + "***")
                    for listeler in Tureng_verisi:
                        for anlamlarvs in listeler:
                            dosya.write(anlamlarvs)
                            dosya.write("+++")
                        dosya.write("---")
                    print("Kaydedilen kelime", i)
                    dosya.write("\n")
                else:
                    hatali_kelime_ekle(i, hatali_kelime_dosyasi)

                uyu(randint(0, 1) + round(random(), 2))
    dosya.close()

def modifiyeli_dosyayi_oku(okunacak_dosya_konumu):
    tum_satirlar=[]
    for i in klasik_dosya_oku(okunacak_dosya_konumu):
        satir = []
        i = i.split("***")
        satir.append(str(i[0]))
        tum_listeler_string=i[1].split("---")
        tum_listeler_string.pop()
        for liste in tum_listeler_string:
            liste=liste.split("+++")
            liste.pop()
            satir.append(liste)
        tum_satirlar.append(satir)
    return tum_satirlar[::-1]

def agac_seklinde_bastir(kaydedilen_sonuclarin_konumu="kaydedilen_sonuclar.txt"):
    for satir in modifiyeli_dosyayi_oku(kaydedilen_sonuclarin_konumu):
        print(" " + satir[0].capitalize())
        kelime_uzunlugu = len(satir[0])
        for index, liste in enumerate(satir):
            if index != 0:
                print("-" + "_" * kelime_uzunlugu + liste[2])
        print()

    input("")

def Tureng_ciktisi(kelime,sayi=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }
    # Sonuçların başındaki sayıları ayıklamak için olan kısım
    def intmi(a):
        try:
            return int(a)
        except ValueError:
            return False

    url = "https://tureng.com/tr/turkce-ingilizce/" + urllib.parse.quote(kelime)
    response = requests.get(url,headers=headers)
    icerik = response.content
    soup = BeautifulSoup(icerik, "html.parser")

    if ("Sanırız yanlış oldu, doğrusu şunlar olabilir mi?" in soup.text) or ("Aradığınız terimin karşılığı bulunamadı" in soup.text):
        return False
    current_index = -1
    son5 = []
    sayi_basladi=False



    for i in soup.find_all("tr", {"class": "", "style": ""}):
        for k in str(i.text).splitlines():
            if (current_index > sayi-1):
                break
            # filtreleme kısmı
            if (k != "") and (not intmi(k) and sayi_basladi == True):
                k = k.rstrip(" ")
                # if (k.endswith("i.")):
                #     k = k.replace("i.", "")
                # elif (k.endswith("f.")):
                #     k = k.replace("f.", "")
                # elif (k.endswith("ünl.")):
                #     k = k.replace("ünl.", "")
                # elif (k.endswith("expr.")):
                #     k = k.replace("expr.", "")
                # elif k.endswith(".s"):
                #     k = k.replace(".s", "")
                son5[current_index].append(k)


            # baştaki sayıyı filtreleme kısmı
            elif (intmi(k)):
                sayi_basladi=True
                son5.append([])
                current_index += 1
    if son5[-1]==[]:
        son5.pop()

    for i in son5:
        if "Kategori" in i:
            i.pop(3)
            i.pop(3)
            i.pop(3)
    return son5

def kelimekaydet(yazilacak_dosya_konumu,hatali_kelime_dosyasi,Tureng_icin_sayi,*args):
    dosya=open(yazilacak_dosya_konumu,"a+",encoding="utf-8")
    dosya.close()
    dosya=open(yazilacak_dosya_konumu,"r",encoding="utf-8")
    onceden_aranmislar = []
    satirlar = dosya.read()
    satirlar = satirlar.splitlines()
    dosya.close()
    for i in satirlar:
        i = i.split("***")
        onceden_aranmislar.append(str(i[0]).strip())

    hatali_kelimeler=[]

    def varmi(deger):
        deger=str(deger).strip().lower()
        if deger in onceden_aranmislar:
            return True
        else:
            return False

    dosya=open(yazilacak_dosya_konumu,"a+",encoding="utf-8")
    for i in args:
        if (type(i)==type(list())):
            for k in i:
                k=str(k).lower()
                if not varmi(k):
                    Tureng_verisi=Tureng_ciktisi(k, Tureng_icin_sayi)
                    if Tureng_verisi:
                        dosya.write(k.rstrip(" ") + "***")
                        for listeler in Tureng_verisi:
                            for anlamlarvs in listeler:
                                dosya.write(anlamlarvs)
                                dosya.write("+++")
                            dosya.write("---")
                        print("Kaydedilen kelime", k)
                        dosya.write("\n")

                    else:
                        hatali_kelimeler.append(k)

                    uyu(randint(0, 1) + round(random(), 2))
        else:
            i=str(i).lower()
            if not varmi(i):
                Tureng_verisi = Tureng_ciktisi(i, Tureng_icin_sayi)
                if Tureng_verisi:
                    dosya.write(i.rstrip(" ") + "***")
                    for listeler in Tureng_verisi:
                        for anlamlarvs in listeler:
                            dosya.write(anlamlarvs)
                            dosya.write("+++")
                        dosya.write("---")
                    print("Kaydedilen kelime", i)
                    dosya.write("\n")
                else:
                    hatali_kelimeler.append(i)

                uyu(randint(0, 1) + round(random(), 2))
    dosya.close()
    if len(hatali_kelimeler)>0:
        print(hatali_kelimeler)
        return hatali_kelimeler
    else:
        return False

class sutunlaricinwidget(QWidget):
    def __init__(self,kelime):
        super(sutunlaricinwidget, self).__init__()
        self.ui(kelime)
    def ui(self,kelime):
        self.layout=QHBoxLayout(self)
        self.label=QLabel(kelime)
        self.layout.addWidget(self.label)

class kullanimsutunu(QWidget):
    def __init__(self,kelimeler):
        super().__init__()
        self.ui(kelimeler)
    def ui(self,kelimeler):
        self.satirlar=[]
        for kelime in kelimeler:
            self.satirlar.append(sutunlaricinwidget(kelime))
        self.layout = QVBoxLayout(self)
        for i in self.satirlar:
            self.layout.addWidget(i)

class kelimesutunu(QWidget):
    def __init__(self,kelimeler):
        super().__init__()
        self.ui(kelimeler)
    def ui(self,kelimeler):
        self.satirlar=[]
        for kelime in kelimeler:
            self.satirlar.append(sutunlaricinwidget(kelime))
        self.layout = QVBoxLayout(self)
        for i in self.satirlar:
            self.layout.addWidget(i)

class anlamsutunu(QWidget):
    def __init__(self,kelimeler):
        super().__init__()
        self.ui(kelimeler)
    def ui(self,kelimeler):
        self.satirlar=[]
        for kelime in kelimeler:
            self.satirlar.append(sutunlaricinwidget(kelime))
        self.layout = QVBoxLayout(self)
        for i in self.satirlar:
            self.layout.addWidget(i)

class horizontalmenu(QWidget):
    def __init__(self,kullanimlistesi,kelimelistesi,anlamlarlistesi):
        super(horizontalmenu, self).__init__()
        self.ui(kullanimlistesi,kelimelistesi,anlamlarlistesi)
    def ui(self,kullanimlistesi,kelimelistesi,anlamlarlistesi):
        self.hbox=QHBoxLayout(self)
        self.sutunlar=[]
        self.sutunlar.append(kullanimsutunu(kullanimlistesi))
        self.sutunlar.append(kelimesutunu(kelimelistesi))
        self.sutunlar.append(anlamsutunu(anlamlarlistesi))
        for i in self.sutunlar:
            self.hbox.addWidget(i)

class satirsagkisim(QWidget):
    def __init__(self,satir):
        super().__init__()
        satir=list(satir)
        satir.pop(0)
        self.kelimelerlistesi=[]
        self.anlamlarlistesi=[]
        self.kullanimlistesi=[]
        for i in satir:
            self.kullanimlistesi.append(i[0])
            self.kelimelerlistesi.append(i[1])
            self.anlamlarlistesi.append(i[2])

        self.layout = QHBoxLayout(self)
        self.toolbutton = QToolButton()
        self.toolbutton.setPopupMode(QToolButton.InstantPopup)
        try:
            self.toolbutton.setIcon(QIcon("ok.ico"))
        except:
            pass
        self.toolbutton.setIconSize(QSize(22,22))

        ###############################


        self.horizontalmenu=horizontalmenu(self.kullanimlistesi,self.kelimelerlistesi,self.anlamlarlistesi)







        self.widgetAction = QWidgetAction(self.toolbutton)
        self.widgetAction.setDefaultWidget(self.horizontalmenu)

        self.widgetMenu = QMenu(self.toolbutton)
        self.widgetMenu.addAction(self.widgetAction)
        self.toolbutton.setMenu(self.widgetMenu)
        self.layout.addWidget(self.toolbutton)

class satirsolkisim(QWidget):
    def __init__(self,kelime):
        super(satirsolkisim, self).__init__()
        self.ui(kelime)
    def ui(self,kelime):

        kelime=str(kelime).capitalize()
        self.layout=QHBoxLayout()
        self.label = QLabel(kelime)
        self.label.setFont(QFont("Calibri",15))
        self.layout.addWidget(self.label)
        self.label.setStyleSheet("color : black;")
        self.setLayout(self.layout)

class Pencere(QMainWindow):
    def __init__(self,satirlar):
        super(Pencere, self).__init__()
        self.setWindowTitle("Tureng")
        try:
            self.setWindowIcon(QIcon("tureng.ico"))
        except:
            pass
        self.ui(satirlar)


        # setting the minimum size
        self.setMinimumSize(240, 300)

    def ui(self,satirlar):
        self.scrollArea = QScrollArea()
        self.sagwidget=QWidget()
        self.saglayout=QVBoxLayout()
        self.liste=[]
        self.solwidget=QWidget()
        self.sollayout=QVBoxLayout()

        menubar=self.menuBar()
        button_action = QAction("Kelime Ekle", self)
        menubar.addAction(button_action)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.toolbartiklamasi)
        button_action.setCheckable(True)


        self.addtoview(satirlar)

        self.sagwidget.setLayout(self.saglayout)




        self.mainwidget=QWidget()
        self.mainlayout=QHBoxLayout(self.mainwidget)

        anawidget=QWidget()
        h_layout=QHBoxLayout(anawidget)
        h_layout.addWidget(self.scrollArea)

        self.mainlayout.addWidget(self.solwidget)
        self.mainlayout.setSpacing(2)
        self.mainlayout.addWidget(self.sagwidget)

        self.scrollArea.setStyleSheet("background : darkgrey;")
        self.scrollArea.setWidget(self.mainwidget)
        self.setCentralWidget(anawidget)

    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def addtoview(self,satirlar):
        for i in satirlar:
            self.liste.append(satirsolkisim(i[0]))

        for i in self.liste:
            self.sollayout.addWidget(i)

        self.solwidget.setLayout(self.sollayout)

        self.liste.clear()

        for i in satirlar:
            self.liste.append(satirsagkisim(i))

        for i in self.liste:
            self.saglayout.addWidget(i)

        self.liste.clear()

    def updateview(self):
        self.clearLayout(self.sollayout)
        self.clearLayout(self.saglayout)
        self.addtoview(modifiyeli_dosyayi_oku("kaydedilen_sonuclar.txt"))


    def toolbartiklamasi(self):
        self.dialogpenceresi=kelimeekle()

class kelimeeklewidgeti(QWidget):
    def __init__(self):
        super(kelimeeklewidgeti, self).__init__()
        self.vlayout=QVBoxLayout(self)
        self.text=QLabel("Eklenecek kelime / kelimeler:")
        self.text.setFont(QFont("Calibri",12))
        self.vlayout.addWidget(self.text)
        self.yazialani=QTextEdit()
        self.vlayout.addWidget(self.yazialani)
        self.altyazi=QLabel()
        self.vlayout.addWidget(self.altyazi)
        self.bt=QPushButton("Kaydet")
        self.bt.clicked.connect(self.tikla)
        self.vlayout.addWidget(self.bt)


    def tikla(self):
        yazi=self.yazialani.toPlainText()
        self.yazialani.setText("İşlem yapılıyor...")
        islemyapildi=False
        yazi=yazi.splitlines()
        for s,i in enumerate(yazi):
            yazi[s]=i.strip().lower()
        self.sonuc=kelimekaydet("kaydedilen_sonuclar.txt","hatali_kelimeler.txt", 7,yazi)
        if self.sonuc:
            self.yazialani.clear()
            self.hatalilar=""
            for i in self.sonuc:
                self.hatalilar+="{} kelimesi hatalıdır.\n".format(i)
                yazi.remove(i)
            #kelimeler dosyasına ekleme yapma kısmı

            self.yazialani.setText(self.hatalilar)
        if len(yazi)>0:
            dosya = open("kelimeler.txt", "a+",encoding="utf-8")
            for i in yazi:
                dosya.write(i+"\n")
            dosya.close()
            islemyapildi = True

        if islemyapildi == True:
            self.yazialani.setText(self.yazialani.toPlainText() + "\nİşlem tamamlandı.")
            win.updateview()

class kelimeekle(QDialog):
    def __init__(self):
        super(kelimeekle, self).__init__()
        self.hlayout=QHBoxLayout(self)
        self.widget=kelimeeklewidgeti()
        self.setWindowTitle("Kelime ekle")
        try:
            self.setWindowIcon(QIcon("plus.ico"))
        except:
            pass
        self.hlayout.addWidget(self.widget)
        self.setFixedHeight(self.hlayout.sizeHint().height())
        self.setFixedWidth(self.hlayout.sizeHint().width())
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.show()


app = QApplication(sys.argv)
win = Pencere(modifiyeli_dosyayi_oku("kaydedilen_sonuclar.txt"))
win.show()
sys.exit(app.exec_())
