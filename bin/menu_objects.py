#---MENU OBJECTS MODULE--

from PyQt5 import QtCore, QtGui, QtWidgets
from menu_layouts import left_panel_buttons
class filter:
    def __init__(self,nm = None,params = None):
        self.name = nm
        self.params = params
        self.picture = None
        self.info = "info"
        self.roi = None
        self.draw_area = None
        self.order = None
    def parameters(self):
        return self.params
class gui_filters:
    def __init__(self):
        self.reset()
    def reset (self,hint = None):
        self.namelist = []
        self.tabs = {}
        self.pictures = {}
        self.widgets = {}
        self.left_panel = {}
        self.op_filters = {} # PARAMETERS ARE HERE (Filter Class)
        self.draw_are = {}
    def add_filter(self,fname):
        self.namelist.append(fname)

        self.tabs.update({fname:fname})
        self.tabs[fname] = QtWidgets.QWidget()
        self.tabs[fname].setObjectName(fname)

        self.pictures.update({fname:fname})

        self.widgets.update({fname:fname})

        self.left_panel.update({fname: fname})
        self.op_filters.update({fname:filter()})
class mainmenu_objects:
    def __init__(self,):
        pass
    def load_gui(self,gui):
        self.gui = gui

        self.gui_filters = gui_filters()


    def new_filter(self,nm = None,param = None,btn = None,load=None): # CREATES NEW NAME AND WIDGET
        if load == True:
            self.gui_filters.add_filter(nm)
            return nm
        if nm == None:
            nm = "filtre"
            default = "filtre"
        else:
            default = nm
        i = 1
        while True:
            if default in self.gui_filters.namelist:
                default = nm+ str(i)
                i += 1
                if i == 200:
                    break
            else :
                self.filtername = default
                break
        self.gui_filters.add_filter(self.filtername)
        return self.filtername

    def reset(self):
        for tab in self.gui_filters.tabs.values():
            self.gui.tabWidget.removeTab(1)
        for lp in self.gui_filters.left_panel.values():
            try:
                lp.Button.deleteLater()
            except:
                pass
        self.gui_filters.reset()
    def set_ng(self,object):
        object.setStyleSheet("background-color: rgb(164, 0, 0);")
        object.setText("NG")
    def set_ok(self,object):
        object.setStyleSheet("background-color: rgb(13, 51, 15);")
        object.setText("OK")