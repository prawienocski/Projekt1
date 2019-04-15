#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:31:47 2019

@author: prawienocski
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QColorDialog
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt #odpowiedzialny za rysowanie wykresu
#klasa ponizej reprezentuje aplikacje
class AppWindow(QWidget):  
    def __init__(self):
        super().__init__()
        self.title = 'Wyznaczanie przecięcia dwóch punktów'
        self.initInterface() #klasa odpowiedzialna za tworzenie interfejsu
        self.initWidgets()
        self.setWindowIcon(QIcon('Kalkulator.png')) #dodanie ikonki kalkulatora do aplikacji
        
    def initInterface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100,100,500,350) #geometria okna
        self.show() #metoda aby okno się pokazalo
        
    def initWidgets(self):
        btn = QPushButton('rysuj',self) #guzik
        btnCol = QPushButton('Zmień Kolor',self)
        btnSave = QPushButton('Zapisz',self)
        #definiowanie labeli oraz line editow
        XAlabel=QLabel('X A',self) 
        YAlabel=QLabel('Y A',self) 
        XBlabel=QLabel('X B',self)
        YBlabel=QLabel('Y B',self)
        XClabel=QLabel('X C',self)
        YClabel=QLabel('Y C',self)
        XDlabel=QLabel('X D',self)
        YDlabel=QLabel('Y D',self)
        pollabel=QLabel('polozenie prostych',self)
        
        btn.setToolTip('Kliknij aby narysowac wykres')
        btnCol.setToolTip('wybierz kolor wykresu')
        btnSave.setToolTip('zapisz współrzędne punktu P do pliku')

        self.XAEdit=QLineEdit()
        self.YAEdit=QLineEdit()
        self.XBEdit=QLineEdit()
        self.YBEdit=QLineEdit()
        self.XCEdit=QLineEdit()
        self.YCEdit=QLineEdit()
        self.XDEdit=QLineEdit()
        self.YDEdit=QLineEdit()
        self.pollabel=QLineEdit()
        #ponizej linie wyswietlaja informacje (podpowiedzi) do okien edycji
        self.XAEdit.setToolTip('wpisz wsp X punktu A')
        self.YAEdit.setToolTip('wpisz wsp Y punktu A')
        self.XBEdit.setToolTip('wpisz wsp X punktu B')
        self.YBEdit.setToolTip('wpisz wsp Y punktu B')
        self.XCEdit.setToolTip('wpisz wsp X punktu C')
        self.YCEdit.setToolTip('wpisz wsp Y punktu C')
        self.XDEdit.setToolTip('wpisz wsp X punktu D')
        self.YDEdit.setToolTip('wpisz wsp Y punktu D')
        
        self.resultLabel = QLabel('',self)
        
        #wykres
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        #umieszczenie przyciskow w main window wraz z oknami edycji 
        #Umieszczenie pokolei X i Y dla A B C D 
        grid = QGridLayout()#tworzenie siatki
        grid.addWidget(XAlabel, 1, 0)
        grid.addWidget(self.XAEdit, 1, 1) 
        grid.addWidget(YAlabel, 1, 3)
        grid.addWidget(self.YAEdit, 1, 4)
        grid.addWidget(XBlabel, 2, 0)
        grid.addWidget(self.XBEdit, 2, 1)    
        grid.addWidget(YBlabel, 2, 3)
        grid.addWidget(self.YBEdit, 2, 4)
        grid.addWidget(XClabel, 3, 0)
        grid.addWidget(self.XCEdit, 3, 1)   
        grid.addWidget(YClabel, 3, 3)
        grid.addWidget(self.YCEdit, 3, 4)
        grid.addWidget(XDlabel, 4, 0)
        grid.addWidget(self.XDEdit, 4, 1)    
        grid.addWidget(YDlabel, 4, 3)
        grid.addWidget(self.YDEdit, 4, 4)
        
        #Umiejscowienie wszystkich przyciskow (przelicz, zmiany kolory, zapisu)
        grid.addWidget(btn, 5, 0 ,1, 2)   
        grid.addWidget(btnCol, 5, 0,3,4) 
        grid.addWidget(self.resultLabel,6,0)
        grid.addWidget(self.canvas, 1 ,7, -1, -1) #wykres
        
        grid.addWidget(pollabel,6,0) #label polozenia
        grid.addWidget(self.pollabel,6,1,1,4)
        
        grid.addWidget(btnSave,8,0,1,2) 
        
        self.setLayout(grid)
        #Umozliwienie uruchomienia funkcji przy kliknieciu guzika 
        btn.clicked.connect(self.oblicz)
        btnCol.clicked.connect(self.zmienkolor)
        btn.clicked.connect(self.zapisz)
        
    def zmienkolor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            print(color.name())
            self.Rysuj(col=color.name())
        
        
    def oblicz(self):
        self.Rysuj()
        
  
    def Rysuj(self,col='green'):      
        XA=self.rysuj(self.XAEdit)
        YA=self.rysuj(self.YAEdit)
        XB=self.rysuj(self.XBEdit)
        YB=self.rysuj(self.YBEdit)
        XC=self.rysuj(self.XCEdit)
        YC=self.rysuj(self.YCEdit)
        XD=self.rysuj(self.XDEdit)
        YD=self.rysuj(self.YDEdit)
        
        if XA is not None and (YA is not None) and (XB is not None) and (XB is not None) and (XC is not None) and (YC is not None) and (XD is not None) and (YD is not None):
               
            if (((XB-XA)*(YD-YC))-((YB-YA)*(XD-XC)))==0:
                self.pollabel.setText('proste są równoległe')
            else:
                t1=(((XC-XA)*(YD-YC))-((YC-YA)*(XD-XC)))/(((XB-XA)*(YD-YC))-((YB-YA)*(XD-XC)))
                t2=(((XC-XA)*(YB-YA))-((YC-YA)*(XB-XA)))/(((XB-XA)*(YD-YC))-((YB-YA)*(XD-XC)))    
                self.XP=round(XA+t1*(XB-XA),3)
                self.YP=round(YA+t1*(YB-YA),3)
   
                if 0<=t1<=1 and 0<=t2<=1:
                    self.pollabel.setText("Punkt przecięcia leży wewnątrz obu odcinków")
                elif 0<=t1<=1 and t2<0 or t2>1:
                    self.pollabel.setText("punkt leży wewnątrz odcinka AB i na przedłużeniu odcinka CD")
                elif 0<=t2<=1 and t1<0 or t1>1:
                    self.pollabel.setText("punkt przecięcia leży wewnątrz odcinka CD i na przedłużeniu odcinka AB")
             
            x1=['A', 'B', 'C', 'D', 'P']
            X2=[XA, XB, XC, XD, self.XP]
            Y2=[YA, YB, YC, YD, self.YP]
                      
            self.figure.clear()
            ax=self.figure.add_subplot(111) #wymiary siatki (jeden na jeden na jeden)
            ax.scatter(X2,Y2)
            ax.plot([XA,XB],[YA,YB] ,color=col,marker='o')
            ax.plot([XC,XD],[YC,YD] ,color=col,marker='o')  #rysowanie wykresu
            ax.plot([XA,self.XP],[YA,self.YP] ,linestyle='-.', color='red')
            ax.plot([XD,self.XP],[YD,self.YP] ,linestyle='-.', color='green')
            for (x,y,l) in zip(X2,Y2,enumerate(x1)):
                ax.annotate("{}({};{})".format(l[1],x,y), xy=(x,y)) #dodanie etykiet
           
            self.canvas.draw() #odswiezenie
        
    def rysuj(self,element):
        if element.text().lstrip('-').replace('.','',1).isdigit():
            return float(element.text())
        else:
            element.setFocus() #linijka pokazuje
            return None #None oznacza zwrót niczego 

  #Funkcja umozliwiajaca zapisanie wartosci do nowo utworzonego pliku tekstowego 
    def zapisz(self):
        plik1=open('Wsp_pkt_P.txt','w+')
        plik1.write(80*'-')
        plik1.write('\n|{:^10}|\n'.format('współrzędne'))#format
        plik1.write('\n|{:^10}|{:^10}|\n'.format('XP', 'YP'))
        plik1.write('\n|{:^10}|{:^10}|\n'.format(self.XP,self.YP))

        plik1.close()

#inny sposob otwarcia pliku ponizej
def main():
    app = QApplication(sys.argv)
    window = AppWindow()
    app.exec_()
    
if __name__ == '__main__':
    main()
#if __name__ == '__main__':
    
  #  app =  QApplication(sys.argv)
  #  okno = AppWindow()
  #  sys.exit(app.exec_())