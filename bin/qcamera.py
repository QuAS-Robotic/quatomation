# CAMERA CLASS

import time
import cv2
import os
def init_camera():
    global camera
    x = 10000
    y = 10000
    camera = cv2.VideoCapture(0)
    time.sleep(1)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
def capture():
    global camera
    ret, frame = camera.read()
    return frame
def show():
    global camera
    ret, frame = cap.read()
    cv2.imshow('Camera',frame)
def launch():
    global camera
    try:
        init_camera()
    except Exception as e:
        print(e)
    while(True):
        ret, frame = camera.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()
    path = os.path.join(os.getcwd(),"bin","temp","camout.png")
    cv2.imwrite(path,frame)
class QCamera:
    def __init__(self,main,timer):
        self.wait = None
        self.on = False
        self.main = main
        self.timer = timer
        self.timer.setInterval = 2
        self.timer.timeout.connect(self.update_frame)
        x = 10000
        y = 10000
        self.camera = cv2.VideoCapture(0)
        time.sleep(1)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
    def capture (self):
        self.timer.stop()

        self.wait = True
        return self.frame
    def update_frame (self):
        if not self.wait == True: ret, self.frame = self.camera.read()
        self.main.set_pic(self.main.gui.input_image_btn,self.frame)
    def show(self):
        pass
    def launch(self):
        if self.on == False: return
        self.wait = False
        self.timer.start()
    def stop(self):
        self.timer.stop()
        self.on = False
        self.camera.release()
    def start(self):
        self.camera.open(0)
        self.on = True
    def setfps(self,fps):
        self.timer.setInterval = int(fps)
    def __call__(self, *args, **kwargs):
        return self.on # Camera status -> on or off
if __name__ == "__main__":
    init_camera()
    while(True):
        ret, frame = camera.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()
