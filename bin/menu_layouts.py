from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import sys

class left_panel_buttons:
    def __init__(self,mmf,gui,fname):
        self.fname = fname
        self.Button = QtWidgets.QPushButton(gui.layoutWidget1) # TODO : Sol paneli QT 'den güncelle ve layoutwidget i değiştir.
        self.Button.setText(fname)
        self.Button.clicked.connect(lambda: mmf.delete_filter(self.fname))
        gui.left_panel_filters_layout.addWidget(self.Button)

def confirmation_dialog(widget,title ,message,):
    buttonReply = QMessageBox.question(widget,title, message,
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        return True
    else:
        return False
def measure_settings(settings,gui):
    class PopUpDLG(QtWidgets.QDialog): #Credit : Achayan/stackeroweflow
        def __init__(self,parent,settings):
            #super().__init__.py(parent)
            super(PopUpDLG, self).__init__(parent)
            self.settings = settings
            self.setObjectName("self")
            self.resize(500, 150)
            self.setMinimumSize(QtCore.QSize(500, 250))
            self.setMaximumSize(QtCore.QSize(500, 250))
            self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
            #icon = QtGui.QIcon()
            #icon.addPixmap(QtGui.QPixmap("Icons/Plus-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            #self.setWindowIcon(icon)
            self.contour_style = QtWidgets.QComboBox(self)
            items = ["DEFAULT","CCOMP","TREE"]
            self.contour_style.addItems(items)
            self.contour_style.activated[str].connect(lambda : self.update_setting(key = "c_style",value=self.contour_style.currentText()))
            self.gridLayout = QtWidgets.QGridLayout(self)
            self.gridLayout.setObjectName("gridLayout")
            self.label = QtWidgets.QLabel(self)
            self.label.setObjectName("label")
            self.label.setText("Metot Seçiniz :")
            self.gridLayout.addWidget(self.contour_style, 0, 1, 1, 1)
            self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

            self.label2 = QtWidgets.QLabel(self)
            self.label2.setObjectName("label2")
            self.label2.setText("Referans Ölçüsü Giriniz :")
            self.ref_input = QtWidgets.QLineEdit(self)
            self.ref_input.setGeometry(QtCore.QRect(80, 478, 85, 25))
            self.ref_input.textChanged.connect(lambda : self.update_setting(key="width",
                                                                            value=self.ref_input.text()))
            self.gridLayout.addWidget(self.ref_input, 1, 1, 1, 1)
            self.gridLayout.addWidget(self.label2, 1, 0, 1, 1)

            self.ok = QtWidgets.QPushButton(self)
            self.ok.setObjectName("ok")
            self.ok.setText("Tamam")

            self.gridLayout.addWidget(self.ok, 2, 0, 1, 1)
            self.cancel = QtWidgets.QPushButton(self)
            self.cancel.setObjectName("cancel_link")
            self.gridLayout.addWidget(self.cancel, 2, 1, 1, 1)
            self.cancel.setText("İptal")
            self.cancel.clicked.connect(self.reject_)
            self.ok.clicked.connect(self.done_)
            self.upd_content()
        def done_ (self,*args,**kwargs):
            self.close()
            return
        def reject_(self):
            self.close()
            return
        def upd_content(self):
            if self.settings["c_style"] == "TREE":
                self.contour_style.setCurrentIndex(2)
            elif self.settings["c_style"] == "CCOMP":
                self.contour_style.setCurrentIndex(1)
        def update_setting (self,key,value):

            if not self.settings is None:
                if key == "c_style":
                    if value == "DEFAULT":
                        return
                    self.settings[key] = value
                elif key == "width":
                    try:
                        value = float(value)
                    except:
                        return
                    if value <0:
                        return
                    self.settings[key] = value

    popup = PopUpDLG(gui,settings)
    popup.show()
#****************************************POPUP WINDOW IMAGE *******************************
class PopUpDLG(QtWidgets.QDialog): #Credit : Achayan/stackeroweflow
    def __init__(self,parent,image):
        super(PopUpDLG, self).__init__(parent)
        self.setObjectName("self")
        self.resize(parent.size())
        self.setMinimumSize(QtCore.QSize(parent.size()))
        self.setMaximumSize(QtCore.QSize(parent.size()))
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap("Icons/Plus-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.setWindowIcon(icon)
        self.image = QtWidgets.QLabel(self)
        self.image.setGeometry(QtCore.QRect(0, 0, 1200, 740))
        self.image.setObjectName("image")
        image = image.scaled(parent.size(), QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(image)
        self.ok = QtWidgets.QPushButton(self)
        self.ok.setObjectName("ok")
        self.ok.setText("Tamam")
        self.ok.setGeometry(20,30,40,150)
        self.horzlayout = QtWidgets.QHBoxLayout(self)
        self.horzlayout.setContentsMargins(0, 0, 0, 0)
        #self.horzlayout.setGeometry(QtCore.QRect(parent.size().height()-40,0,40,parent.size().width()))
        self.horzlayout.setGeometry(QtCore.QRect(460, 720, 281, 31))
        self.horzlayout.setObjectName("horzlayout")
        self.horzlayout.addWidget(self.ok)
        self.cancel = QtWidgets.QPushButton(self)
        self.cancel.setObjectName("cancel_link")
        self.horzlayout.addWidget(self.cancel)
        self.cancel.setText("İptal")
        self.cancel.setGeometry(0, 0, 40, 150)
        self.cancel.clicked.connect(self.reject_)
        self.ok.clicked.connect(self.done_)
        self.upd_content()
    def done_ (self,*args,**kwargs):
        self.close()
        return
    def reject_(self):
        self.close()
        return
    def upd_content(self):
        pass
    def update_setting (self,key,value):
        pass
class Poppi(QtWidgets.QDialog):
    def __init__(self,parent,image):
        super(Poppi, self).__init__(parent)
        self.resize(1200, 756)
        self.image = QtWidgets.QLabel(self)
        self.image.setGeometry(QtCore.QRect(0, 0, 1200, 721))
        self.image.setText("")
        self.image.setObjectName("label")

        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setGeometry(QtCore.QRect(0, 730, 201, 17))
        self.lbl.setObjectName("label_2")
        self.lbl.setText("Kesme işlemi için alan seçiniz.")
        image = image.scaled(parent.size(), QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(image)
        self.boxWid = QtWidgets.QWidget(self)
        self.box = QtWidgets.QHBoxLayout(self.boxWid)
        self.box.addWidget(self.image)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(460, 720, 281, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.ok.setStyleSheet("background-color: rgb(17, 103, 2);\n"
                                        "color: rgb(186, 189, 182);")
        self.ok.setObjectName("ok")
        self.ok.setText("OK")
        self.horizontalLayout.addWidget(self.ok)
        self.cancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancel.setStyleSheet("background-color: rgb(93, 10, 10);\n"
                                      "color: rgb(186, 189, 182);")
        self.cancel.setObjectName("cancel")
        self.cancel.setText("İptal")
        self.horizontalLayout.addWidget(self.cancel)

def show_image(gui,image):
    popup = Poppi(gui,image)
    popup.show()
def crop_image_layout(gui,image):
    class crop_pp (Poppi):
        def __init__(self,gui,image):
            super(crop_pp,self).__init__(gui,image)
            self.setMouseTracking(True)
            self.i = 0
            self.ok.clicked.connect(self.close)
            self.cancel.clicked.connect(self.close)
        def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
            print(a0.x(),a0.y())

            """   
            def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
                newHeight = self.image.geometry().height() - a0.angleDelta().y()
                width = self.image.geometry().width() - a0.angleDelta().y()
                self.image.resize(width, newHeight)
            """
    popup = crop_pp(gui,image)
    popup.show()

