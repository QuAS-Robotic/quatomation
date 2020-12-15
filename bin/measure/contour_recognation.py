import cv2
from operations import *
from math import *
import numpy as np

from bin.measure.operations import apply_canny, get_contours
cv2.namedWindow("img1",cv2.WINDOW_NORMAL)
cv2.resizeWindow('img1', 1000, 600)
#cv2.namedWindow("img2",cv2.WINDOW_NORMAL)
#cv2.resizeWindow('img2', 1000, 600)

im1 = apply_canny(sample_image(2),rotate = "left")
im2 = apply_canny(sample_image(1),rotate = "left")
cv2.imshow("aha",im2)
moments = cv2.moments(im1)
huMoments = cv2.HuMoments(moments)
im1_cnts_temp = get_contours(im1)
im2_cnts_temp = get_contours(im2)
bos1 = np.zeros((im1.shape[0],im1.shape[1], 3), np.uint8)
bos2 = np.zeros((im2.shape[0],im2.shape[1], 3), np.uint8)
compare = np.zeros((im2.shape[0],im2.shape[1], 3), np.uint8)
print(" Im1 Cnts {}, Im2 cnts : {} \n".format(len(im1_cnts_temp),len(im2_cnts_temp)))
for i in range(0,7):
    huMoments[i] = -1 * copysign(1.0, huMoments[i]) * log10(abs(huMoments[i]))
im1_cnts = []
im2_cnts = []
for c1,c2 in zip(im1_cnts_temp,im2_cnts_temp):
    if cv2.contourArea(c1) > 1: im1_cnts.append(c1)
    if cv2.contourArea(c2) > 1 and cv2.arcLength(c2,False) > 1000: im2_cnts.append(c2)
"""
for i,c1 in enumerate(im2_cnts):
    cv2.drawContours(bos1,[c1],-1,(0,250,0),-1)
    cv2.imshow("img1", bos1)
    cv2.waitKey(0)
"""
print("Im1 Cnts {}, Im2 cnts : {} \n".format(len(im1_cnts),len(im2_cnts)))

ref1 = im2_cnts[1] # Red
ref2 = im1_cnts[1] # Green
d1 = cv2.matchShapes(im1,im2,cv2.CONTOURS_MATCH_I1,0)
d2 = cv2.matchShapes(im1,im2,cv2.CONTOURS_MATCH_I2,0)
d3 = cv2.matchShapes(im1,im2,cv2.CONTOURS_MATCH_I3,0)
cv2.destroyAllWindows()
cv2.drawContours(compare,[ref1],-1,(0,0,250))
cv2.drawContours(compare,[ref2],-1,(0,250,0))

d11 = cv2.matchShapes(ref1,ref2,cv2.CONTOURS_MATCH_I1,0)
d21 = cv2.matchShapes(ref1,ref2,cv2.CONTOURS_MATCH_I2,0)
d31 = cv2.matchShapes(ref1,ref2,cv2.CONTOURS_MATCH_I3,0)

arc1 = cv2.arcLength(ref1,False)
arc2 = cv2.arcLength(ref2,False)
print("Match 1 : {}, Match 2 : {}, Match 3 : {} \n Arc1 : {}, Arc2 : {}".format(d11,d21,d31,arc1,arc2))
#cv2.imshow("aha",im2)
cv2.imshow("karsi",compare)
cv2.waitKey(0)

#print(d1,d2,d3)


