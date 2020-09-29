import sqlite3
import os
import numpy as np

class save:
    def __init__(self,dbpath,filterlist):
        path = os.path.split(dbpath)[0]
        filename = os.path.split(dbpath)[1]
        try:
            os.makedirs(os.path.join(path,filename))
        except:
            pass
        self.db = sqlite3.connect(os.path.join(dbpath,"filters.db"))
        self.cur = self.db.cursor()
        for filter in filterlist.values(): #TODO: Uptade here
            """ 
            if filter.name[0:4] == "Blur":
                return
            elif filter.name[0:5] == "Canny": #TODO: ilk 5i şeklinde yap
                self.layout(filter)
            """
            self.layout(filter)
    def layout(self,filter):
        execute = " CREATE TABLE IF NOT EXISTS " + filter.name+\
                  """ (                 name text NOT NULL,
                                        params text,
                                        picture text,    
                                        info text,                                   
                                        roi text,
                                        draw_area text,  
                                        order_ text                                 
                                    ); """
        self.cur.execute(execute)
        vals = []
        for params in vars(filter).items():
            if type(params[1]) == np.ndarray:
                parameter = params[1].tolist()
            else:
                parameter = params[1]
            vals.append(str(parameter))
        self.cur.execute("SELECT * from "+ filter.name)
        current = self.cur.fetchall()
        if len(current) > 0:
            self.cur.execute("DELETE from "+filter.name+" where name = '"+filter.name + "'")
        insert ="INSERT INTO "+str(filter.name)+ """ (name,params,picture,info,
                       roi,draw_area,order_) VALUES (?,?,?,?,?,?,?);"""

        self.cur.execute(insert,vals)
        self.db.commit()
def load_filters(dbpath):
    path = os.path.split(dbpath)[0]
    filename = os.path.split(dbpath)[1]
    filters = []
    try:
        os.makedirs(os.path.join(path,filename))
    except:
        pass
    print(dbpath)
    db = sqlite3.connect(os.path.join(dbpath,"filters.db"),detect_types=sqlite3.PARSE_DECLTYPES)
    cur = db.cursor()
    cur.execute('SELECT name from sqlite_master where type= "table"')
    filternames = cur.fetchall()
    for filtername in filternames:
        filtername = filtername[0]
        cur.execute("SELECT * FROM "+filtername)
        for f in cur.fetchall():
            filters.append(f)
    return filters
