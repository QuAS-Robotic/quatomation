from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QLineEdit,QMessageBox,QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from program_files import program_files
from log import printlog,errorlog
from menu_objects import mainmenu_objects,filter
from menu_layouts import left_panel_buttons,confirmation_dialog,\
    measure_settings,show_image,crop_image_layout
from filters import Canny,Blur,Bilateral
from log import gui_log,errorlog
import time
global pf
import os
from save import save,load_filters
import measure as measure
import qcamera
import json
import numpy as np
import qimage2ndarray
pf = program_files("bin/appdb")
import cv2
from work_piece import work_piece
def _import_pic(self):
    path_to_images = QFileDialog.getExistingDirectory(self.widget, 'Projeyi içeren dosyayı seçiniz:',
                                                      '', QFileDialog.ShowDirsOnly)
    if path_to_images == "":
        return
    images = program_files().get_filenames(target = path_to_images,type = ".JPG")
    for image in images:
        self.image_names.append(image)
        self.images.append(work_piece(cv2.rotate(cv2.imread(os.path.join(path_to_images,image)),cv2.ROTATE_90_COUNTERCLOCKWISE),name = image))
    self.current_image = self.images[0]
    self.set_pic(self.gui.input_image_btn,self.current_image.image)
    self.s_main_image = True
    self.control()
    self.log("Resim içeri aktarıldı")

def set_pic(self, label, pic, size_hint="label"):
    size = label.size()
    #pf.goto(pf.temp)
    if isinstance(pic,str):
        self.main_pixmap = QPixmap(pic)
        self.main_pixmap_scaled = self.main_pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
        label.setPixmap(self.main_pixmap_scaled)
    else:
        if isinstance(label,QPushButton): label.setIcon(QIcon(to_pixmap(pic)))
        else: label.setPixmap(to_pixmap(pic).scaled(size, QtCore.Qt.KeepAspectRatio))

def load_project(self):
    def to_array(list):
        if list == "None" or list == None:
            return None
        else:
            out = []
            out.append(np.array(list))
            return out

    def convert_to_list(str):
        if str == "None" or str == None:
            return None
        else:
            return json.loads(str)

    """   
    if not self.s_main_image == None :
        buttonReply = confirmation_dialog(widget=self.widget, title="Dikkat !",
                                          message= "Yeni bir proje açarsanız, tüm ilerlemeniz kaybolacak onaylıyor musunuz ?")
        if not buttonReply == True:
            return
    """
    while True:
        if self.save_file == "" or self.save_file is None:
            self.save_file = QFileDialog.getExistingDirectory(self.widget, 'Projeyi içeren dosyayı seçiniz:',
                                                          '', QFileDialog.ShowDirsOnly)
        if self.save_file == "" or self.save_file is None:
            break
        loading_filters = load_filters(self.save_file)
        if loading_filters == None:
            continue  # TODO: kafam karıştı
        else:
            #self.reset_all(hint="dont_touch_image")
            i = 0
            for filter in loading_filters:
                self.mmo.new_filter(nm=filter[0], load=True)
                self.add_filter(i=i, new_filter=filter[0], params=convert_to_list(filter[1]),
                                picture=None, info=filter[3],
                                roi=convert_to_list(filter[4]),
                                draw_area=convert_to_list(filter[5]))  # TODO:Order eklenecek

                if filter[4] is None or filter[4] == [] or filter[4] == "None":
                    pass
                else:
                    self.mmo.gui_filters.op_filters[filter[0]].roi = np.array(convert_to_list(filter[4]))
                if filter[5] is None or filter[5] == [] or filter[4] == "None":
                    pass
                else:
                    self.mmo.gui_filters.op_filters[filter[0]].draw_area = np.array(convert_to_list(filter[5]))
                i += 1

            self.control()
            break
def add_filter(self,i,new_filter,params,picture,info = None,roi = None,draw_area = None):

    self.mmo.gui_filters.op_filters[new_filter].name = new_filter
    self.mmo.gui_filters.op_filters[new_filter].params = params #TODO: Daha iyi bir çözüm bul.(başlangıçta parametrelerin None olması
    self.mmo.gui_filters.op_filters[new_filter].picture = picture
    self.mmo.gui_filters.op_filters[new_filter].roi = roi
    self.mmo.gui_filters.op_filters[new_filter].draw_area = draw_area

    #self.s_filtertablist.append(self.mmo.filtertab[i]) #TODO tablist oluştur
    self.log(new_filter + " isimli filtre eklendi !")

def to_pixmap(img):
    #image_read = img.copy()
    #imread = QtGui.QImage(image_read.data, image_read.shape[1], image_read.shape[0],QtGui.QImage.Format_RGB888).rgbSwapped() #TODO: hangisi doğru sonuç veriy
    imread = qimage2ndarray.array2qimage(img)
    return QtGui.QPixmap.fromImage(imread)
def to_icon(img):
    imread = qimage2ndarray.array2qimage(img)
    return QtGui.QIcon(imread)