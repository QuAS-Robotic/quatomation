import sys
import os
sys.path.append("bin")
sys.path.append("bin/measure")

import toolbar_rc
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtGui import QIcon, QPixmap
from menu_functions import mainmenu_funcs
from menu_objects import mainmenu_objects
from log import gui_log,errorlog
from professor import professor

global mmf
mmf = mainmenu_funcs()
mmo = mainmenu_objects()
def version_control():
    app_version = "0.1"
    version_info = ""
    return app_version,version_info
class mainwin(QtWidgets.QMainWindow):
    def __init__(self,):
        super(mainwin, self).__init__()
        uic.loadUi('automotion_gui.ui', self)
        self.clicks()

    def clicks(self):
        self.start_stop_btn.clicked.connect(mmf.run)
        self.input_image_btn.clicked.connect(mmf._import_pic)
        self.image_proc_btn.clicked.connect(mmf.import_image_processing)
        self.output_graph_btn.clicked.connect(mmf.show_output)
        self.pushButton.clicked.connect(mmf.segmentation)
        self.pre_pro_output_btn.clicked.connect(lambda : mmf.show_pic(mmf.current_image()))
        self.scratch_detection_btn.clicked.connect(mmf.scratch_detection)
        self.pushButton_2.clicked.connect(lambda : mmf.show_pic(mmf.professor.output_image))
        #self.empty.clicked.connect(mmf.reset_all)
        #self.filter_options.clicked.connect(mmf.delete_filter)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainwin()
    log = gui_log(ui)
    app.setStyle("fusion")
    info = "Hoş Geldiniz ! \nUygulama Sürümü : " + version_control()[0] + "\n"
    log(info)
    process = professor()
    mmf.load_gui(gui=ui,app=app,wdg=MainWindow,log = log,proc = process) # load class features to mm func module
    mmo.load_gui(ui) # load class gui to menu objects
    ui.show()
    sys.exit(app.exec_())
