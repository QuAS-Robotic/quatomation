import cv2
def sample_image(code = 0):
    if code == 1: nm = "testng.JPG"
    elif code == 2: nm = "testng2.JPG"
    elif code == 3: nm = "line.JPG"
    else: nm = "test.JPG"
    import os
    path = os.getcwd().split(os.sep)
    path = os.path.join(os.sep,*path[:-2],"gui","img",nm)
    return cv2.imread(path)
def apply_canny (img,blur =9  ,tresh1= 50, tresh2 = 150,proc = False,rotate = None ):
    '''
    You can apply canny with default parameters to any image
    :param img: image array ( you can use cv2.imread(path) for this)
    :param blur: blur param
    :param tresh1: tresh
    :param tresh2: tresh2
    :param proc: if you want dilote and erose processes give True to this param
    :return: output image array
    '''
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # img = cv2.bitwise_and(img, img, mask=filters.color_filter(hsv,1,2))
    if rotate == "left": img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif rotate == "right":img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if proc == True:
        img = cv2.dilate(img, np.ones((5, 5), np.uint8))
        img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    # equ = cv2.equalizeHist(img)
    # img = np.hstack((img, equ))
    img = cv2.GaussianBlur(img, (blur, blur), 0)
    img = cv2.Canny(img, threshold1=tresh1, threshold2=tresh2)
    img = cv2.dilate(img, None, iterations=1)
    img = cv2.erode(img, None, iterations=1)

    return img

def compare_images(ref,image):
    refim = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(refim, im, full=True)
    diff = (diff * 255).astype("uint8")  # fark resmi

    return score

def get_contours(img,hint= None):
    '''
    :type: etc.
    :param img: image array
    :param hint: retrieve type,|"TREE" or "CCOMP"| default is: CCOMP
    :return: list of contours
    '''
    image = img
    if hint == "TREE":
        method = cv2.RETR_TREE
        method2 = cv2.CHAIN_APPROX_SIMPLE
    else:
        method = cv2.RETR_CCOMP
        method2 = cv2.CHAIN_APPROX_NONE

    try:
        cnts, hierarchy = cv2.findContours(img.copy(), method, method2)
    except Exception as e:
        print(e)
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cnts, hierarchy = cv2.findContours(image.copy(), method, method2)

    return cnts

def is_inside_rect(outer,inner,hint = None):
    if outer[0] <= inner[0] and outer[1] <= inner[1] and outer[0] + outer[2] >= inner[0] + inner[2] and outer[1]+ outer[3]\
        >= inner[1] + inner[3]: return True # xo <= xi , yo <= yi, xo+wo > xi + wi , yo + h0 < yi + hi

    else:
        return  False
def create_filled_rect(points):
    out = []
    if len(points) < 3: points = points[0]

    for px in range (points[0],points[0]+points[2]):
        for py in range (points[1],points[1]+points[3]):
            out.append([px,py])

    return out
