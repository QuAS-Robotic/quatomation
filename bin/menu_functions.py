from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QLineEdit,QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from program_files import program_files
from log import printlog,errorlog
from menu_objects import mainmenu_objects,filter
from menu_layouts import left_panel_buttons,confirmation_dialog,\
    measure_settings,show_image,crop_image_layout
from log import gui_log,errorlog
from measure import hole_analysis
global pf
import os
from save import save,load_filters
import measure as measure
import qcamera
from measure.line_curve import LineCurve,Curve_Analysis
from measure.scratch_detection import DetectScratch,ScratchAnalysis
from measure.hole_diameter import HoleMeasurement
from cloud_ import firebase
pf = program_files("bin/appdb")
import cv2
import gui
import qimage2ndarray
from threading import Thread
from work_piece import work_piece
class mainmenu_funcs():
    def __init__(self):
        self.crop_flag = False
        self.rotate_right = None
        self.rotate_left = None
        self.project = None
        self.main_image = None
        self.main_pic = None
        self.gate = False
        self.status()
        self.mmo = mainmenu_objects()
        self.settings = {"c_style":"TREE","width":16.6}
        self.save_file = None
        self.images = []
        self.image_names = []
        self.imageno = -1
        self.scratch = False # TODO: Kaldır, geçici bir çözüm bu
    def load_gui (self,gui,app,wdg,log,proc):
        self.gui = gui
        self.log = log
        self.log.gui = self.gui

        self.gui.actionRun.triggered.connect(lambda: LineCurve(picture =
                                                                 self.professor.output_image,
                                                                 width = self.settings["width"]))
        self.gui.actionLoadProject.triggered.connect(self.load_project)
        self.gui.actionSave.triggered.connect(lambda: save(dbpath = self.save(),
                                                            filterlist = self.mmo.gui_filters.op_filters))

        self.gui.actionPRoje.triggered.connect(self.reset_all)
        self.gui.toolbar_plot.triggered.connect(self.analysis_)
        self.app = app
        self.widget = wdg
        self.mmo.load_gui(self.gui)
        self.pictures()
        self.professor = proc
        self.professor.pf = pf
        self.control()

    def emp(self):
        print(self.settings.values())
        self.resize(size = None)
    def load_menu(self,menu):
        self.menu = menu
    def save(self,):
        if self.save_file == None:
            self.save_file =  QFileDialog.getSaveFileName(self.widget, 'Kaydet')[0]
        return self.save_file
    def load_project(self):
        gui.load_project(self)
    def reset_all(self,hint = None):
        self.rotate_right = None
        self.rotate_left = None
        self.crop_flag = None
        if confirmation_dialog(widget = self.widget,title = "Dikkat !",message = "Tüm veriler temizlenecek onaylıyor musunuz ?") == False :
            return
        self.status(hint="reset")
        if not hint == "dont_touch_image":
            self.save_file = None #TODO:SAVE FILE RESETINI AYARLA
            self.s_main_image = None
            self.main_image = None
            self.gui.picture_main.clear()
        self.mmo.reset()
        #self.run()
        self.control()
    def status(self, hint=None, var=None, action=None):
        return
    def control(self,hint=None):
        if self.professor.filterlist == [] or self.images == []: self.gate = False
        else: self.gate = True
        """
        for filter_ in self.mmo.gui_filters.op_filters.values():
            if self.s_main_image == None:
                break
            if filter_.picture is None and  self.main_pic is not None:
                filter_.picture = self.professor.main_image
        
        
        if hint == "filter":
            self.professor.filterlist = []
            if self.gui.checkBox.checkState() == 2:
                self.professor.gray_filter = True
            else:
                self.professor.gray_filter = False

            for filter in self.mmo.gui_filters.op_filters.values():
                self.professor.filterlist.append(filter)
            return
        if hint == "post-process":
            self.output_image = self.professor.output_image
        elif hint == "update_pics": pass
        #self.professor.filterlist = []
        """
#**********************************  MAIN TAB FUNCS  ******************************
    def import_image_processing(self):
        gui.load_project(self)
        self.professor.filterlist = []
        self.professor.gray_filter = True
        for filter in self.mmo.gui_filters.op_filters.values():
            self.professor.filterlist.append(filter)
    def _import_pic(self):
        gui._import_pic(self)
    def set_pic(self,label,pic,size_hint = "label"):
        gui.set_pic(self,label,pic,size_hint = "label")
    def pictures(self):
        return
    def delete_filter (self,fname):
        buttonReply = confirmation_dialog(widget = self.widget,title = "Dikkat !",message = fname + "Filtresini sileceksiniz. Onaylıyor musunuz ?")
        if buttonReply == True:
            print('Filtre silinecek.')
        else:
            print('İptal edildi.')

    def add_filter_from_panel(self,fname):
        self.log("Filtre Eklendi")
        if fname == "+ Filtre Ekle":
            return
        if self.s_main_image == False:
            self.gui.comboBox.setCurrentIndex(0)
            QMessageBox.information(self.widget,"HATA !","Filtrelenecek resminiz bulunmuyor !")
            return
        self.gui.comboBox.setCurrentIndex(0)
        for i in range (0,len(self.s_filterlist)+1):# MAIN MENUDEKİ BOŞ FİLTRE ALANLARI
            if i == len(self.s_filterlist) and i < len(self.mmo.filterpic):
                new_filter = self.mmo.new_filter(nm = fname)
                #path_to_filter = new_filter+os.path.splitext(self.main_pic)[-1]
                #self.add_filter(i= i,new_filter = new_filter,params =[7,7,7],picture=pf.copy(path=self.main_pic, to_path=pf.join(pf.temp,path_to_filter))   )
                self.add_filter(i=i, new_filter=new_filter, params=[7, 7, 7],
                                picture=self.professor.main_image)
                break
        self.control()
    def add_filter(self,i,new_filter,params,picture,info = None,roi = None,draw_area = None):
        gui.add_filter(self,i,new_filter,params,picture,info = None,roi = None,draw_area = None)

#**********************************  CANNY LAYOUT TAB FUNCTIONS  ******************************

    def resize(self,size): #TODO: Size seçim penceresi ekle
        self.professor.main_image = self.professor.resize(image =self.professor.main_image,size = size)
        self.s_main_image = True
        self.control()
    def crop(self,hint = None):
        self.crop_flag = True

        if hint != "auto":
            self.crop_roi = self.professor.select_ROI(image=self.professor.main_image,
                                                                hint="one")
        self.professor.main_image = self.professor.crop_image(image=self.professor.main_image,
                                  roi=self.crop_roi)
        self.set_pic(self.gui.picture_main,self.professor.main_image)
        #self.set_pic(self.gui.picture_main, self.professor.main_image_name)
        self.s_main_image = True
        self.control()
    def rotate(self,hint):
        if hint == "right":
            self.rotate_right = True
        elif hint == "left":
            self.rotate_left = True
        self.professor.main_image = self.professor.rotate(image = self.professor.main_image,type = hint)
        self.set_pic(self.gui.picture_main,self.professor.main_image)
        self.s_main_image = True
        self.control()

    def run(self):
        if self.imageno == len(self.images):
            print("RESİMLER BİTTİ")
            return
        self.control()
        if not self.gate == True:
            self.test_run()
        self.current_image = self.images[self.imageno]
        self.set_pic(self.gui.input_image_btn, self.current_image.image)
        self.set_pic(self.gui.pre_pro_output_btn,self.current_image())
        self.professor.main_image = self.current_image()
        self.gui.part_name_lbl.setText("PARÇA ADI: "+self.image_names[self.imageno].upper()+"--"+ str(self.current_image.partno))
        if self.scratch == True:
            scratch_detection = DetectScratch(self.professor.run(),roi = self.scratch_roi)
            self.result = ScratchAnalysis(self.current_image.name,*scratch_detection)
        else:
            curve_analysis = LineCurve(self.professor.run())
            self.result = Curve_Analysis(self.current_image.name, *curve_analysis)

        self.set_pic(self.gui.image_proc_btn, self.professor.output_image)
        if self.result() == False:
            self.mmo.set_ng(self.gui.okng_btn)
        else: self.mmo.set_ok(self.gui.okng_btn)

        self.control(hint="post-process")
        if self.current_image.partno >= len(self.current_image.part): # NEW IMAGE CONDITIONS
            self.imageno+=1
        else:
            self.current_image.partno += 1

    def next_step (self):
        self.imageno += 1

    def test_run(self):
        self.save_file = '/home/ogibalboa/Desktop/PICTURES'
        self.import_image_processing()
        for image in program_files().get_filenames(target=self.save_file, type=".JPG"):
            self.image_names.append(image)
            read = os.path.join(self.save_file, image)
            self.images.append(work_piece(cv2.rotate(cv2.imread(read), cv2.ROTATE_90_COUNTERCLOCKWISE),name = image))
        #cv2.imshow("bbos",self.images[self.imageno])
        self.gate = True

    def show_output(self):
        self.result.show()
    def measure(self):
        try:
            results = measure.run(picture=self.professor.output_image,
                        width=self.settings["width"],
                        hint=self.settings["c_style"])
            self.measure_database.save_measurement(results)
        except:
            pass
        #self.measure_database.print_db("Obje1")

    def analysis_(self):
        hole_analysis.analysis.analysis().auto(self.measure_database.cur)

    def to_pixmap(self,img):
        image_read = img.copy()
        imread = QtGui.QImage(image_read.data, image_read.shape[1], image_read.shape[0],QtGui.QImage.Format_RGB888).rgbSwapped()
        #imread = qimage2ndarray.array2qimage(img).rgbSwapped()
        return QtGui.QPixmap.fromImage(imread)
    def segmentation (self):
        self.current_image.segmentation()

    def show_pic(self,pic):
        cv2.namedWindow("Resim",cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Resim",(pic.shape[1],pic.shape[0]))
        cv2.imshow("Resim",pic)

    def scratch_detection (self,):
        self.scratch = True
        self.scratch_roi = self.professor.select_ROI(self.current_image())