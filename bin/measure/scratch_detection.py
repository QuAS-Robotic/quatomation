import imutils
import cv2
import operations as op

class ScratchAnalysis:
    def __init__(self,id,result,im,refim,refim_cnts = None,im_cnts = None):
        self.result = result
        self.id = id
        self.image = im
        self.refim = refim

        self.refim_cnts = refim_cnts
        self.im_cnts = im_cnts

    def __call__(self, *args, **kwargs):
        if self.result == False:
            return False
        else:
            return True

    def show(self):
        cv2.namedWindow("Çizik Tespit Edildi",cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Çizik Tespit Edildi", (self.image.shape[1], self.image.shape[0]))
        cv2.imshow("Çizik Tespit Edildi",self.image)
        return


def DetectScratch (im,refim = None,hint = None,roi = None): # refim : ref image
    im_cnts = op.get_contours(im)
    if hint == "compare":
        ref_cnts = op.get_contours(refim)
        return compare_contour_count(refim,im)

    for c in im_cnts:
        #moments.append(Hu_Moment(c))
        for r in roi:
            if op.is_inside_rect(outer = r,inner = cv2.boundingRect(c)):
                print("HATALIII!")
                return False,im,refim

    print("HATA YOK")
    return True,im,refim
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
    if op.is_inside_rect([0,0,900,900],[200,200,700,700]):
        print("TUTTİ")
    else:
        print("nop")