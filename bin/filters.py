#FİLTERS
import cv2
import numpy as np
def Canny (path,temp,para1 = 50,para2 = 150,aperture = 3,roi = None,dilate = None,erode= None):
    #image = cv2.imread(path) #TODO: canny ' ye l2grad ve edged parametreleri eklenecek
    image = path
    if roi is None:
        roi = [None]
    for r in roi:
        if not r is None:
            filtered = image[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]
        else :
            filtered = image.copy()
        filtered = cv2.Canny(filtered,threshold1=para1,threshold2= para2,apertureSize=aperture)

        if dilate == None:
            filtered = cv2.dilate(filtered, None, iterations=1)
        if erode == None:
            filtered = cv2.erode(filtered, None, iterations=1)

        if not r is None:
            try:
                image[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = filtered
            except:
                image[r[1]:r[1] + r[3], r[0]:r[0] + r[2],0] = filtered
                image[r[1]:r[1] + r[3], r[0]:r[0] + r[2], 1] = filtered
                image[r[1]:r[1] + r[3], r[0]:r[0] + r[2], 2] = filtered
        else :
            image = filtered
    #cv2.imwrite(temp, image)
    return image
def Blur (path,temp,kernel1 = 9,kernel2 = 9,roi = None): # TODO : Blur parametreleri ?
    #image = cv2.imread(path)
    image = path
    if roi is None:
        roi = [None]
    for r in roi:
        if not r is None:
            filtered = image[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]
        else :
            filtered = image.copy()
        filtered = cv2.GaussianBlur(filtered, (kernel1,kernel2), 0)
        if not r is None:
            try:
                image[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = filtered
            except:
                image[r[1]:r[1] + r[3], r[0]:r[0] + r[2],0] = filtered
                image[r[1]:r[1] + r[3], r[0]:r[0] + r[2], 1] = filtered
                image[r[1]:r[1] + r[3], r[0]:r[0] + r[2], 2] = filtered
        else :
            image = filtered
    #cv2.imwrite(temp,image)
    return image
def Bilateral (image,core = 7,para1 = 50,para2 = 50):
    image = cv2.imread(image)
    return cv2.bilateralFilter(image, core, para1, para2)
def Gray(path,to_path):
    #image = cv2.imread(path)
    image = path
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite(to_path,gray)
    return gray
def drawRect(image,roi):
    for r in roi:#TODO : Alan seçimi yapılmazsa ?
        """
        image = cv2.rectangle(img = image,pt1= (r[0], r[1]),pt2= (r[0]+r[2],r[1]+r[3]), color=(0, 0, 0),thickness= -1)
        """
        filtered = image[r[1]:r[1] + r[3], r[0]:r[0] + r[2]]
        filtered[:] = 0
        image[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] = filtered
    #TODO: Not al, roi den gelen output : [x,y,w,h] şeklinde. Üstte ise point belirtiyorsun.
    return image
def drawCircle(image,roi):
    for r in roi:#TODO : Alan seçimi yapılmazsa ?
        image = cv2.circle(img = image, center = (r[0],r[1]),radius=r[2], color=(0, 0, 0),thickness= -1)
    return image
def selectROI(image,hint = ""):
    cv2.namedWindow("roi_win", cv2.WINDOW_NORMAL)
    if hint == "one":
        roi = cv2.selectROI(windowName="roi_win",img=image)
    else:
        roi = cv2.selectROIs(windowName="roi_win",img=image)
    if roi is not None:
        cv2.destroyAllWindows()
        return roi

# MANUAL CIRCLE DRAWING

def select_ROI_manual(image):
    global drawing, mode
    drawing = False
    img = cv2.imread(image)
    roi = []
    def interactive_drawing(event, x, y, flags, param):
        global mouse_x, mouse_y, drawing, draw_x, draw_y, rad, img2, ix, iy, center_x, center_y
        if event == cv2.EVENT_LBUTTONDOWN:
            rad = 0
            drawing = True
            center_x, center_y = x, y
            img2 = cv2.imread(image)
            cv2.imshow('ROI Seçiniz', img2)
        elif event == cv2.EVENT_MOUSEMOVE:

            if drawing == True:
                img2 = cv2.imread(image)
                if x > ix or y > iy:
                    rad += 1
                    ix = x
                elif x < ix or y < iy and rad > 1:
                    ix = x
                    rad -= 1
                cv2.circle(img2, (center_x, center_y), rad, (0, 0, 255), 3)
                cv2.imshow('ROI Seçiniz', img2)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            img2 = cv2.imread(image)
            cv2.circle(img2, (center_x, center_y), rad, (0, 0, 255), 3)
            cv2.imshow('ROI Seçiniz', img2)
            # print x,y
            # cv2.line(img,(x,y),(x,y),(0,0,255),10)
        return x, y

    global img2
    img2 = img.copy()
    static = img.copy()
    cv2.namedWindow('ROI Seçiniz')
    cv2.setMouseCallback('ROI Seçiniz', interactive_drawing)
    global rad, ix, iy
    ix = 0
    iy = 0
    rad = 0
    while (1):
        cv2.imshow('ROI Seçiniz', img2)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            """            
            combined = img2[:, :, 0] + img2[:, :, 1] + img2[:, :, 2]
            roi[0],roi[1] = np.where(combined > 0)
            roi[0] = roi[0].tolist()
            roi[1] = roi[1].tolist()
            """
            break
        elif k == 13:
            roi.append([center_x, center_y, rad])
    cv2.destroyAllWindows()
    return roi

def rotate (path,type):
    image = path
    if type == "right":
        image = cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
    elif type == "left":
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return image
def resize (path,size):
    image = path
    scale_percent = 60  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width,height)
    image = cv2.resize(image,dim)
    return image
def read_(path):
    return cv2.imread(path)
def write_(image,path):
    return
    cv2.imwrite(path,image)
    return
def read(image):
    return cv2.imread(image)
def crop_image(im,r):
    im = im[r[1]:r[1] + r[3], r[0]:r[0] + r[2]]
    return im

def color_filter(img,tresh1,tresh2):
    lower_blue = np.array([40, 10, 19])
    upper_blue = np.array([212, 20, 81])

    # preparing the mask to overlay
    mask = cv2.inRange(img, lower_blue, upper_blue)

    # The black region in the mask has the value of 0,
    # so when multiplied with original image removes all non-blue regions
    return mask

