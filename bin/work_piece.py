import cv2

class work_piece:
    def __init__(self,image,name = ""):
        self.name = name
        self.image = image
        self.part = []
        self.partno = 0
    def __call__(self, *args, **kwargs):
        for arg in args:
            if arg == "reset_partno":
                self.partno = 0
        if len(self.part) < 1: return self.image
        else: return self.part[self.partno-1]


    def segmentation (self, x = 1000, y = 500):
        image = self.image.copy()
        temp = image.copy()
        global k
        k = None
        def mous_pos(event,px,py,params,flag):
            global mx,my
            mx = px
            my = py
        while x <= self.image.shape[1]:
            while True:
                cv2.namedWindow('ALAN SEC',cv2.WINDOW_NORMAL)
                k = cv2.waitKey(1) & 0xFF
                cv2.setMouseCallback('ALAN SEC', mous_pos)
                if k == 27:
                    cv2.destroyAllWindows()
                    break
                if k == 32:
                    temp = image.copy()
                    cv2.rectangle(temp, (mx, my), (mx + x, my + y), (0, 0, 255), 3)
                    cords = [mx, my]
                if k == 13:
                    cv2.rectangle(image, (cords[0],cords[1]),(cords[0]+x,cords[1]+ y), (0, 0, 255), 3)
                    temp = image.copy()
                    r = cords + [cords[0] + x, cords[1] + y]
                    self.part.append(self.image[r[1]:r[3], r[0]:r[2]])
                    cv2.imshow("PART0",self.part[-1])
                cv2.putText(temp, "Hello World!!!", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
                cv2.imshow("ALAN SEC",temp)
            break
