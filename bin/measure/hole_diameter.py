from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import os
import filters
import imutils
import cv2

def HoleMeasurement(picture, width=30, hint="TREE"):
    global window_flag
    window_flag = False
    if hint == "CCOMP":
        method = cv2.RETR_CCOMP
        method2 = cv2.CHAIN_APPROX_NONE
    elif hint == "TREE":
        method = cv2.RETR_TREE
        method2 = cv2.CHAIN_APPROX_SIMPLE
    else:
        method = cv2.RETR_TREE
        method2 = cv2.CHAIN_APPROX_SIMPLE

    image = picture
    results = []

    def midpoint(ptA, ptB):  # orta noktayı bulmayı sağlıyor
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

    # görüntüyü yükleyin, gri tonlamaya dönüştürün ve biraz bulanıklaştırın

    # kenar haritasında konturlar bul
    try:
        cnts, hierarchy = cv2.findContours(image.copy(), method, method2)
    except:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cnts, hierarchy = cv2.findContours(image.copy(), method, method2)

    # cnts = imutils.grab_contours(cnts)

    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (cnts, _) = contours.sort_contours(cnts)
    hierarchy = hierarchy[0]
    global pixelsPerMetric
    pixelsPerMetric = None
    # loop over the contours individually

    # for c in cnts:
    mask = np.zeros(image.shape[:2], dtype=image.dtype)

    def show(c):
        global window_flag
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 100:
            pass

        # compute the rotated bounding box of the contour
        global pixelsPerMetric
        orig = image.copy()
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box
        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

        # loop over the original points and draw them
        # cv2.circle daire çizer----cv2.circle(image, center_coordinates, radius, color, thickness)---
        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        # unpack the ordered bounding box, then compute the midpoint
        # between the top-left and top-right coordinates, followed by
        # the midpoint between bottom-left and bottom-right coordinates
        # çizilen kutunun alt ve üst kenarlarının orta noktalarını buldu
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

        # compute the midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-righ and bottom-right
        # orta noktaların arasını hesapladı
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        # draw the midpoints on the image
        cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

        # draw lines between the midpoints
        cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
        cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)

        # compute the Euclidean distance between the midpoints
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        # if the pixels per metric has not been initialized, then
        # compute it as the ratio of pixels to supplied metric
        # (in this case, inches)
        if pixelsPerMetric is None:
            pixelsPerMetric = dB / width
        # compute the size of the object

        dimA = dA / pixelsPerMetric

        dimB = dB / pixelsPerMetric
        if dimA < width / 5 or dimB < width / 5:
            pass
        # draw the object sizes on the image
        cv2.putText(orig, "{:.2f}mm".format(dimA),
                    (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 2)
        cv2.putText(orig, "{:.2f}mm".format(dimB),
                    (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 2)

        # show the output image
        if window_flag != True:
            cv2.namedWindow("Sonuc Ekrani", cv2.WINDOW_NORMAL)
            window_flag = True
        # cv2.resizeWindow("Ölçüm Resmi")
        cv2.imshow("Sonuc Ekrani", orig)

        cv2.waitKey(0)
        return (round(dimA, 2), round(dimB, 2))
    print(len(cnts))
    for component in zip(cnts, hierarchy):
        currentContour = component[0]
        currentHierarchy = component[1]
        if currentHierarchy[2] < 0:
            results.append(show(currentContour))
        elif currentHierarchy[3] < 0:
            results.append(show(currentContour))
        if results[-1] == None:
            results.pop()
    window_flag = False
    return results