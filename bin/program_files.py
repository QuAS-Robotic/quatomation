# -*- coding: utf-8 -*-
import os
import sqlite3
import shutil
class program_files:
    def __init__(self,path=None,hint = None):
        self.main = os.getcwd()
        self.chdir("gui")
        self.chdir("img")
        self.gui_img = os.getcwd()
        os.chdir(self.main)
        self.chdir("bin")
        self.bin = os.getcwd()
        self.log = os.path.join(self.bin , "log.txt")
        self.chdir("temp")
        self.temp = os.getcwd()
        self.chdir(os.path.join(self.main,"db"))
        self.db = os.getcwd()
        """      
        try:
            with sqlite3.connect(path) as self.db:
                self.cur = self.db.cursor()
                self.cur.execute ("SELECT * FROM program_files")
                self.files = cur.fetchall()[0].split(",")
        except:
            pass"""
        self.init_paths()
        self.clear_dir(self.temp)
        os.chdir(self.main)
    def chdir(self,fname):
        try:
            os.chdir(fname)
        except:
            os.mkdir(fname)
            os.chdir(fname)
    def init_paths(self):
        return
        self.main = os.getcwd()
        os.chdir("gui/img")
        self.gui_img = os.getcwd()
        os.chdir(self.main)
        self.bin = os.getcwd()
        self.log = os.path.join(self.bin,"log.txt")
        os.chdir("temp")
        self.temp = os.getcwd()
        os.chdir(os.path.join(self.main,"db"))
        self.db = os.getcwd()
        os.chdir(os.path.join(self.main,"gui"))
        self.gui = os.getcwd()
        self.filelist = [self.main,self.gui_img,self.bin,self.log,self.db,self.gui]
        self.files_to_write = "?".join(self.filelist)
        self.cur.execute("INSERT INTO program_files(dirs) VALUES (?) ",self.files_to_write)
        self.db.commit()
    def goto(self,path):
        os.chdir(path)
    def copy(self,path,to_path):
        """
        if os.path.splitext(path)[-1] != os.path.splitext(to_path)[-1]:
            to_path = to_path + os.path.splitext(path)[-1]
        execute = "cp \""+ str(path) + "\" \""+ str(to_path) +"\""
        os.system(execute)
        """
        try:
            shutil.copy(path,to_path)
        except:
            pass
            #os.remove(to_path)
            #shutil.copy(path,to_path)
        #os.system("copy "+ path +" " +to_path)
        return to_path
    def delete(self,file):
        os.remove(file)
    def listdir(self,path):
        os.chdir(path)
        return os.listdir()
    def move (self,file,dir):
        os.replace(file,dir)
    def join(self,path,path2):
        return os.path.join(path,path2)
    def clear_dir (self,path):
        files = self.listdir(path)
        if len(files) <1 : return
        for i in files:
            delt = os.path.join(path,i)
            try:
                self.delete(delt)
            except :
                pass
    def get_filenames(self,target,type = None):
        b = os.getcwd()
        os.chdir(target)
        files = os.listdir()
        new_files = []
        for file in files:
            if type == None: break
            if os.path.splitext(file)[-1] == type:
                new_files.append(file)
        os.chdir(b)
        return new_files