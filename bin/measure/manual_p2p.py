def p2p(picture):
    global points
    points = []
    global img
    try:
        img = cv2.imread(picture)
        #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #img = cv2.bitwise_and(img, img, mask=filters.color_filter(hsv,1,2))
        img =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #img = cv2.dilate(img, np.ones((5, 5), np.uint8))
        #img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        #equ = cv2.equalizeHist(img)
        #img = np.hstack((img, equ))
        img = cv2.GaussianBlur(img, (9,9), 0)
        img = cv2.Canny(img,threshold1=50,threshold2= 150)
        img = cv2.dilate(img, None, iterations=1)
        img = cv2.erode(img, None, iterations=1)
        currentContour,_ = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        print(len(currentContour))
        try:
            cv2.drawContours(img,currentContour,-1,(255,0,150),4)
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
        img = np.zeros((512, 512, 3), np.uint8)
    def calc_dist(event, x, y, flags, param):
        global points
        global img
        #pix = 1
        pix = 0.06286255
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append([x,y])
            print(points)
            if len(points) != 2:
                    return
            dist_x = abs(points[1][0] - points[0][0])
            dist_y = abs(points[1][1] - points[0][1])
            dist = dist_x**2 + dist_y**2
            dist = dist**0.5
            dist = dist*pix
            dist_x = dist_x*pix
            dist_y = dist_y*pix
            points = []
            print("SONUÇ : R = {:.2f}mm\n"
                  "      : X = {:.2f}mm\n"
                  "      : Y = {:.2f}mm\n".format(dist,dist_x,dist_y))
            return dist
        elif event == cv2.EVENT_RBUTTONDOWN:
            try:
                (b, g, r) = img[y, x]
                print("Pixel at ({}, {}) - Red: {}, Green: {}, Blue: {}".format(x, y, r, g, b))
            except:
                print(img[ y, x])

    cv2.namedWindow('Manual Olcum',cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('Manual Olcum', calc_dist)
    cv2.imshow("Manual Olcum", img)
    cv2.waitKey(0)
    global rad, ix, iy
    ix = 0
    iy = 0
    rad = 0
    while (1):
        cv2.imshow('Manual Olcum', img)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()