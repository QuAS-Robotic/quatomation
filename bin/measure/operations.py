import cv2
def apply_canny (img,blur =9  ,tresh1= 50, tresh2 = 150 ):
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # img = cv2.bitwise_and(img, img, mask=filters.color_filter(hsv,1,2))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.dilate(img, np.ones((5, 5), np.uint8))
    # img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
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

def get_contours(pic,hint= None):
    image = pic
    if hint == "CCOMP":
        method = cv2.RETR_CCOMP
        method2 = cv2.CHAIN_APPROX_NONE
    elif hint == "TREE":
        method = cv2.RETR_TREE
        method2 = cv2.CHAIN_APPROX_SIMPLE
    else:
        method = cv2.RETR_CCOMP
        method2 = cv2.CHAIN_APPROX_NONE

    try:
        cnts, hierarchy = cv2.findContours(pic.copy(), method, method2)
    except Exception as e:
        print(e)
        image = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
        cnts, hierarchy = cv2.findContours(image.copy(), method, method2)

    return cnts

def is_inside_rect(outer,inner,hint = None):
    if outer[0] <= inner[0] and outer[1] <= inner[1] and outer[0] + outer[2] >= inner[0] + inner[2] and outer[1]+ outer[3]\
        >= inner[1] + inner[3]: return True # xo > xi , yo < yi, xo+wo > xi + wi , yo + h0 < yi + hi

    else:
        return  False
def create_filled_rect(points):
    out = []
    if len(points) < 3: points = points[0]

    for px in range (points[0],points[0]+points[2]):
        for py in range (points[1],points[1]+points[3]):
            out.append([px,py])

    return out