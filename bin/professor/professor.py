import filters
import os
import cv2
class professor:
    def __init__(self):
        self.filterlist = []
        self.main_image_path = None
        self.main_image_name = None
        self.temp_image_path = None
        self.main_image      = None
        self.output_image_path = None
        self.gray_filter = None
        self.pf = None
        self.processing_picture = self.temp_image_path
        self.output_image = None
        self.step = 0
    def load_img(self,path):
        self.main_image = filters.read(path)
    def findfilter(self,filter,fname,params):
        if self.step > 0 :
            path = self.processing_picture
        else:
            path = self.temp_image_path
        if fname == "Blur" or fname[:-1] == "Blur" or fname[:-2] == "Blur":
            self.output_image = filters.Blur(path=path, temp=filter.picture, kernel1=params[0], kernel2=params[1], roi=filter.roi)
            filter.picture = self.output_image
        elif fname [0:5] == "Canny":
            self.output_image = filters.Canny(path = path,temp= filter.picture,para1=params[0],para2=params[1],
                  aperture =params[2],roi = filter.roi)
            filter.picture = self.output_image
        if filter.draw_area is not None:
            self.output_image = self.draw_area(image = self.output_image,roi=filter.draw_area)
            filter.picture = self.output_image
            #filters.write_(image = self.output_image,path = filter.picture)
        self.processing_picture = filter.picture
    def run(self):
        self.step = 0
        self.temp_image_path = self.main_image
        #if self.gray_filter == True:
        self.temp_image_path = filters.Gray(path = self.temp_image_path,to_path = self.temp_image_path)
            #self.shadows = filters.detect_black(self.temp_image_path)
        for filter in self.filterlist:
            self.findfilter(filter = filter,fname = filter.name,params = filter.params) #0->PARA1 1->PARA2
            self.step += 1
        self.output_image_path = self.processing_picture
        #self.output_image = filters.remove_shadows(self.output_image,self.shadows)
        return self.output_image
    def select_ROI(self,image,hint = ""):
        return filters.selectROI(image,hint)
    def select_ROI_circle(self,image):
        return filters.select_ROI_manual(image)

    def draw_area(self,image,roi):
        if self.check_None(roi):
            return
        try:
            if len(roi[0]) == 4:
                return filters.drawRect(image,roi)
            else :
                return filters.drawCircle(image,roi)
        except Exception as e:
            print(e)
    def rotate(self,image,type):
        return filters.rotate(path = image,type = type)
    def resize(self,image,size):
        return filters.resize(path = image,size = size)
    def crop_image(self,image,roi):
        if self.check_None(roi):
            return
        return filters.crop_image(image,roi)
    def check_None(self,item):
        try:
            if item is None:
                return True
            elif item == None:
                return True
        except:
            pass
        return False
