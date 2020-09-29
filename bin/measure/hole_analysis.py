import sqlite3
class database:
    def __init__(self):
        with sqlite3.connect(":memory:") as self.db:
            self.cur = self.db.cursor()
            self.vars = {}
            self.varcnt = 0
    def up_varname(self):
        self.varcnt+=1
        self.varname = "Obje" + str(self.varcnt)
        return self.varname
    def save_measurement(self,vars):
        table_name = self.up_varname()
        self.cur.execute("CREATE TABLE IF NOT EXISTS "+ table_name + " (results text)")
        self.vars.update({self.varname:vars})
        for var in vars:
            s_var = str(var[0]) + ","+ str(var[1])
            self.cur.execute("INSERT INTO "+table_name+" (results) VALUES (?);",(s_var,))
        self.db.commit()
    def print_db(self,table_name):
        self.cur.execute("SELECT * FROM "+table_name)
        print(self.cur.fetchall())
    def save_db(self,):
        c = sqlite3.connect('saved.db')
        with c:
            for line in self.db.iterdump():
                if line not in ('BEGIN;', 'COMMIT;'):  # let python handle the transactions
                    c.execute(line)
        c.commit()
        cur = c.cursor()
        cur.execute("SELECT * FROM Obje1")
from matplotlib import pyplot as plt
class analysis:

    def __init__(self):
        self.objects = []
        self.measures = {}
    def to_float_list(self,datas):
        out = []
        for data in datas:
            data_new = data[0].split(",")
            for i in range (len(data_new)):
                data_new[i] = float(data_new[i])
            out.append(data_new)
        return out
    def fetch_datas(self,cur):
        cur.execute('SELECT name from sqlite_master where type= "table"')
        for data in cur.fetchall():
            self.objects.append(data[0])
            cur.execute("SELECT * FROM "+data[0])
            self.measures.update({data[0] : self.to_float_list(cur.fetchall()) })
    def plot(self):
        x_axis = []
        for i in range (len(self.objects)):
            x_axis.append(i)
        y_axis1 = []
        y_axis2 = []
        y_axis3 = []
        y_axis4 = []
        for measures in self.measures.values():
            y_axis1.append(measures[0])
            y_axis2.append(measures[1])
            try:
                y_axis3.append(measures[2])
                y_axis4.append((measures[3]))
            except:
                pass
        fig, host = plt.subplots(4,sharex=True)
        fig.suptitle('Ölçüm Sonuç Grafikleri')
        host[0].plot(x_axis,y_axis1,marker = "o")
        plt.xlabel = "Obje Numarası"
        plt.ylabel = "Ölçülen Değer (mm)"
        host[1].plot(x_axis, y_axis2,marker = "o")
        plt.ylabel = "Ölçülen Değer (mm)"
        host[2].plot(x_axis,y_axis3,marker = "o")
        host[3].plot(x_axis,y_axis4,marker = "o")
        plt.show()
    def auto(self,cur):
        self.fetch_datas(cur)
        self.plot()
if __name__ == "__main__":
    db = sqlite3.connect("saved.db")
    analysis().auto(cur = db.cursor())