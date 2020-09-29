import os
import program_files
import linecache
import sys
from datetime import datetime

#pf = program_files.program_files()

class printlog(object):
    def __init__(self,*args):
        #os.chdir(pf.log)
        try:
            self.file = open("bin/log.txt","+a")
        except:
            self.file = open("log.txt","+a")
        #os.chdir(pf.main)
        self.printout(*args)
    def __call__(self, *args, **kwargs):
        self.printout(*args)
    def clear_log(self):
        #os.chdir(pf.log)
        try:
            self.file2 = open("log.txt", "w")
        except:
            self.file2 = open("bin/log.txt","w")
        self.file2.close
        #os.chdir(pf.main)
    def printout(self,*args):
        for arg in args:
            self.file.write(arg+"\n")
class errorlog(printlog):
    def __init__(self):
        self.printlog = printlog()
        print(self.exception())
        self.printlog(self.exception())
    def __call__(self, *args, **kwargs):
        print(self.exception())
        self.printlog(self.exception())
    def exception(self,):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

class gui_log:
    def __init__(self,gui):
        self.gui = gui
        self.info = ""
    def __call__(self, *args, **kwargs):
        self.info +="\nTarih : | " + str(datetime.now().replace(second=0,microsecond=0))[0:-3] + " | : "
        for i in args:
            self.info += str(i)
        self.gui.infobox.setText(self.info)

class messagebox:
    def __init__(self,gui):
        pass
