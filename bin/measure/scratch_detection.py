import imutils
import cv2
import operations as op
import numpy as np
class ScratchAnalysis:
    def __init__(self,id,orig,result,im,refim, roi= None,scratchs = None ,refim_cnts = None,im_cnts = None):
        self.result = result
        self.id = id # ID?
        self.image = im
        self.refim = refim # REF ALINAN IMG
        self.orig = orig # ORİG IMAGE
        self.refim_cnts = refim_cnts
        self.im_cnts = im_cnts
        self.scratchs = scratchs
        if roi is None:self.roi = [0,0,0,0]
        else : self.roi = roi
    def __call__(self, *args, **kwargs):
        if self.result == False:
            return False
        else:
            return True

    def show(self):
        cv2.namedWindow("Çizik Tespit Edildi",cv2.WINDOW_NORMAL)
        cv2.namedWindow("Orijinal Resim", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Çizik Tespit Edildi", (self.image.shape[1], self.image.shape[0]))
        #cpy = cv2.cvtColor(self.image.copy(),cv2.BINARY2RGB)
        cpy = self.orig.copy()
        orig = self.orig.copy()
        for roi in self.roi:
            cv2.rectangle(orig,(roi[0],roi[1]),(roi[0]+roi[2],roi[1]+roi[3]),(0,255,0),1)
        for scratch in self.scratchs:
            box = cv2.boxPoints(cv2.minAreaRect(scratch))
            box = np.int0(box)
            cv2.drawContours(cpy, [box], 0, (0, 0, 255), 1)
        cv2.imshow("Orijinal Resim",orig)
        cv2.imshow("Çizik Tespit Edildi",cpy)
        return


def DetectScratch (im,refim = None,hint = None,roi = None): # refim : ref image
    im_cnts = op.get_contours(im)
    flag = True
    scratchs = []
    if hint == "compare":
        ref_cnts = op.get_contours(refim)
        return compare_contour_count(refim,im)

    for c in im_cnts:
        #moments.append(Hu_Moment(c))
        for r in roi:
            print(r)
            if op.is_inside_rect(outer = r,inner = cv2.boundingRect(c)):
                flag = False
                scratchs.append(c)
    if flag == False: return False,im,refim,roi,scratchs
    else: return True,im,refim
def compare_contour_count(ref_cnts,im_cnts):
    if len(im_cnts) > len(ref_cnts):
        return False,refim,im,ref_cnts,im_cnts
    else :
        return True,refim,im,ref_cnts,im_cnts
def Hu_Moment(cnt):
    moment = cv2.moments(cnt)
    return cv2.HuMoments(moment)
if __name__ == "__main__":
    #detect_scratch(refim = cv2. )
    """
    if op.is_inside_rect([0,0,900,900],[200,200,700,700]):
        print("TUTTİ")
    else:
        print("nop")
    """
    c = 0
    gap = 10
    for i in range(0,100):
        print(c)
        if c == gap:
            break
        c += 1