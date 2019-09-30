import numpy as np
from math import ceil
np.set_printoptions(threshold=np.nan)
header_type         = np.dtype([('c',np.uint32),('w',np.uint16),('h',np.uint16)])

TRAINING_IMAGE_PATH = "/u1/junk/cs617/Data/training-images.bin"
TRAINING_LABEL_PATH = "/u1/junk/cs617/Data/training-images.bin"
TESTING_IMAGE_PATH  = "/u1/junk/cs617/Data/testing-images.bin"
TESTING_LABEL_PATH  = "/u1/junk/cs617/Data/testing-labels.bin"
class BlowUp:
    def __init__(self):
        self.image = None
        self.draft = np.zeros(1024).reshape(32,32).astype(np.uint8)
    def getSize(self,non_zeros):
        row    = non_zeros[0]
        col    = non_zeros[1]
        width  = (np.amax(row) - np.amin(row))
        height = (np.amax(col) - np.amin(col))
        x  =np.amin(row)
        x1 =np.amax(row)+1
        y  =np.amin(col)
        y1 =np.amax(col)+1
        new_image = self.image[x:x1,y:y1]
        return (new_image,width,height)
    def getPixelValue(self,u,v):
        return self.image[int(u)][int(v)];
    def startProcess(self):
        non_zeros = np.nonzero(self.image)
        new_image,w,h       = self.getSize(non_zeros)
        print(new_image)
        for rind,row in enumerate(self.draft):
            u = (rind/32) * h
            for cind,col in enumerate(row):
                v = (cind/32) * w
                self.draft[rind,cind] = self.getPixelValue(u,v)
        
    def getBlowUpImage(self):
        return self.image

class ImageEnhancer:
    def __init__(self):
        self.filePath = None
        self.imageFd  = None
        self.image    = None
        self.BlowUp   = BlowUp()
    def startEnhancing(self):
        self.imageFd = open(self.filePath,"rb")
        self.goThroughImages()
    def goThroughImages(self):
        imageCount,_,_ = np.fromfile(self.imageFd,dtype=header_type,count=1)[0]
        for i in range(imageCount):
            imagePixels = np.fromfile(self.imageFd,dtype=np.uint8,count=1024)
            imagePixels = np.where(imagePixels == 0,1,0)
            self.BlowUp.image = imagePixels.reshape(32,32).astype(np.uint8)
            self.BlowUp.startProcess()
        self.closeFile()

    def write(self):
        print("should Write")
    def closeFile(self):
        self.imageFd.close()
if __name__ == "__main__":
    Images = ImageEnhancer()
    Images.filePath = TRAINING_IMAGE_PATH
    Images.startEnhancing()
