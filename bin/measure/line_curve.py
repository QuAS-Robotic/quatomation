from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import imutils
import cv2
from operations import apply_canny,get_contours
global ok
ok = None
class Curve_Analysis:
    def __init__(self,id,result,image,plotlist,equation,lines):
        self.result = result
        self.id = id
        self.image = image
        self.plotlist = plotlist
        self.equation = equation
        self.lines = lines
    def __call__(self, *args, **kwargs):
        if self.result == False:
            return False
        else:
            return True
    def show(self):
        self.windowname = self.id.upper() + "- Analiz Sonucu"
        cv2.namedWindow(self.windowname, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.windowname, 1000,600)
        cv2.imshow(self.windowname,self.image)
        lcnt = len(self.plotlist)
        if lcnt == 1:
            self.plotlist.append(self.plotlist[0])
            lcnt += 1
        fig, host = plt.subplots(lcnt, sharex=True)
        for i in range (0,lcnt):
            host[i].plot(range(len(self.plotlist[i])), self.plotlist[i],marker = "o")

        plt.connect('button_press_event', self.mouse_move)
        plt.show()

    def mouse_move(self, event):
        x, y = event.xdata, event.ydata
        x = int(x) * gap + 50
        y = self.lines[-1][x, 0, 1]
        x2 = x + gap
        #x = self.lines[-1][x,0,0]
        try:
            cv2.line(self.image, (x,y), (x2, y), [255, 0, 0], 1)
            cv2.imshow(self.windowname, self.image)
        except Exception as e:
            print(e)

def LineCurve(picture,hint= None):
    global x
    #x = input(" GİR X : \t")
    x = 0.1
    global gap
    #gap = int(input("GİR gap :\t"))
    gap = 100
    image = picture
    cnts = get_contours(picture,"CCOMP")
    lines = []
    plotlist = [] # Tanjant açı değerlerini tutar
    a = 0
    bos = np.zeros((image.shape[0],image.shape[1], 3), np.uint8)
    eq = None

    for c in cnts:
        a += 1
        cv2.drawContours(bos,[c],-1,(255,0,0),-1)
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c,True)
        #print("Alan : {}, uzunluk : {} ".format(area,perimeter))
        line = np.sort(c,axis = 0)
        px, py = parse_array(line)
        coef = np.polyfit(px,py,2)
        eq = equation(coef[0],coef[1],coef[2])
        #print("coef :",coef)
        #print("f(x) = {} \treal y = {}".format(eq(line[0,0,0]),line[0,0,1]))
        #print("FAİLS : ",check_eq(line,eq))
        #cv2.drawContours(bos,fitted_line,-1,(255,255,0),-1)
        if calculate(line).width() > picture.shape[1] *0.99: # çizgiler filtrelenir.
            #print("BAKILAN KISIM :", a)
            lines.append(line)
            plotlist.append(calculate(line).trend())
        else:
            #print("LAZIM DEĞİL")
            #calculate(line).trend()
            pass

        if hint == "show_details":
            cv2.namedWindow('Cnt', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Cnt', 1000, 600)
            cv2.imshow("Cnt",bos)
            cv2.waitKey(0)

    global ok
    if ok == True:
        return True, image, plotlist, eq, lines
    else:
        return False, image, plotlist, eq, lines
class equation :
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c
    def __call__(self, x):
        return self.a * x**2 + self.b*x + self.c
def check_eq (array,eq):
    fail = 0
    for i in range (0,array.shape[0]):
        res = eq(array[i,0,0]) - array[i,0,1]
        if res >2.5:
            fail += 1
    return fail

class calculate ():
    global x
    def __init__(self,matrix):
        global array
        array = matrix
    def width(self):
        return array[-1,0,0] - array[0,0,0]
    def trend(self):
        return trend_track(array,calculate(array).width())
    def tan(self):
        dist_y = float(array[1][1]) - float(array[0][1])
        dist_x = float(x)* float(array[1][0]) - float(x)* float(array[0][0])
        return np.degrees(np.arctan(dist_y/dist_x))
    def avrg(self):
        sumx = 0
        sumy = 0
        for i,j in array:
            sumx += i
            sumy += j
        try:
            return sumx/len(array), sumy/len(array)
        except ZeroDivisionError:
            print("0 A BÖLÜNME HATASI")

def trend_track(array,width):
    global gap
    global ok
    #gap = int(width * 0.133) # ARALIK DEĞERİNİ HESAPLAR
    #gap = 100
    px,py = parse_array(array)
    if max(py) - min(px) > 100:
        print("NG !")
    #print("len :",len(py))
    c = 0
    first_point = False
    arctan = []
    gap_points = []
    ok = True
    for x, y in zip(px, py):
        if c == gap:
            if first_point == False:
                p1 = calculate(gap_points).avrg()
                gap_points.clear()
                c = 0
                first_point = True
            else:
                c = 0
                p2 = calculate(gap_points).avrg()
                arctan.append(calculate([p1,p2 ]).tan()) # ARCTANLARI HESAPLAYIP LİSTEDE TUTTU
                p1 = p2
                gap_points.clear()
        try:
            if x == gap_points[-1][0]:
                continue
        except :
            pass
        gap_points.append([x,y])
        c += 1
        if len(arctan) > 1 and arctan[-1] > arctan[-2]:
            ok = False
    #RESULTS


    print(arctan)
    return arctan

def parse_array(array):
    px = []
    py = []
    for i in range (0,array.shape[0]): # MATRİSTEN x ve y bilgilerini ayırır.
        px.append(array[i,0,0])
        py.append(array[i,0,1])
    return px,py

if __name__ == "__main__":
    os.chdir("..")
    LineCurve(picture = apply_canny.run(cv2.imread("1rng1.JPG")),width=5 )
