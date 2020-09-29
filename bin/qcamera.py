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
if __name__ == "__main__":
    init_camera()
    while(True):
        ret, frame = camera.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()
