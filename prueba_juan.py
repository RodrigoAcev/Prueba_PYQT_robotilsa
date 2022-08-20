# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\prueba_juan.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import requests
import random
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(60, 60, 331, 491))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(460, 100, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(620, 90, 151, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(490, 300, 201, 111))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("click_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(50, 50))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Postulante para ROBOTILSA S.A"))
        self.label.setText(_translate("MainWindow", "-"))
        self.label_2.setText(_translate("MainWindow", "-"))
        self.pushButton.setText(_translate("MainWindow", "REQUEST"))




class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)



class PantallaPeque(QWidget):
    def __init__(self, dictionario):
        super().__init__()
        layout = QVBoxLayout()
        self.tableWidget = QTableWidget()

        self.tableWidget.setRowCount(len(dictionario.keys()))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Atributo', 'Valor'])

        for i, (k, v) in enumerate(dictionario.items()):
            self.tableWidget.setItem(i,0, QTableWidgetItem(k))
            self.tableWidget.setItem(i,1, QTableWidgetItem(v))
        self.tableWidget.move(0,0)


        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

class MiPantalla(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MiPantalla, self).__init__(parent)

        self.char_list = []
        self.name_list = []

        self.setupUi(self)

        self.threadpool = QThreadPool()
        self.pushButton.clicked.connect(self.Presiono)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.showTime)
        self.timer.start()

        self.listWidget.itemClicked.connect(self.detalle_personaje)

        self.listWidget.installEventFilter(self)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.listWidget):
            menu = QtWidgets.QMenu()
            menu.addAction('Información del personaje')
            if menu.exec_(event.globalPos()):
                #item = source.itemAt(event.pos())
                id_row = self.listWidget.currentRow()
                self.PantallaPeque = PantallaPeque(self.char_list[id_row])
                #self.dialogs.append(PantallaPeque)
                self.PantallaPeque.show()
                print(self.char_list[id_row])

            return True
        return super(MiPantalla, self).eventFilter(source, event)

    def Presiono(self):
        worker = Worker(self.GetResponse)
        # Execute
        self.threadpool.start(worker)

    def GetResponse(self):

        char_id_list = random.sample(range(1,84),10)
        ASPECTO_FISICO = ['height', 'mass', 'hair_color', 'skin_color', 'eye_color',
                            'birth_year', 'gender']
        self.char_list = []
        self.name_list = []
        self.listWidget.clear()
        for char_id in char_id_list:
            respuesta = requests.get(f'https://swapi.dev/api/people/{char_id}')
            try:
                aspectos = {key_i: respuesta.json()[key_i] for key_i in ASPECTO_FISICO}
                nombres = respuesta.json()['name']
            except:
                print('some wierd error :C')
                respuesta = requests.get(f'https://swapi.dev/api/people/{char_id+1}')
                aspectos = {key_i: respuesta.json()[key_i] for key_i in ASPECTO_FISICO if key_i in list( respuesta.json().keys())}
                nombres = respuesta.json()['name']
            self.char_list.append(aspectos)
            self.name_list.append(nombres)
            #print(self.name_list[-1])

            listWidgetItem = QtWidgets.QListWidgetItem(self.name_list[-1])
            self.listWidget.addItem(listWidgetItem)

        print('Done!')

    def showTime(self):
        current_time = QtCore.QTime.currentTime()
        current_date = QtCore.QDate.currentDate()

        #label_time = current_time.toString('hh:mm:ss')
        self.label.setText(current_date.toString('dd/MM/yy'))
        self.label_2.setText(current_time.toString('hh:mm:ss'))

    def detalle_personaje(self, id_list):
        id_row = self.listWidget.currentRow()
        print(self.char_list[id_row])



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MiPantalla()
    window.show()
    sys.exit(app.exec_())
