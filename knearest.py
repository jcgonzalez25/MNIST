import struct
import numpy as np
import random
from math import sqrt

#np.set_printoptions(threshold=np.nan)
class Predictor:
    def __init__(self):
        self.testing_image = None
        self.predictions   = []
        self.ks            = 25
    def getDistance(self,training_image):
        return sqrt(np.sum(self.testing_image!=training_image))
    def test(self,training_image):
        tr_id,tr_label,tr_img = training_image
        distance              = self.getDistance(tr_img)
        training_image        = (tr_id,tr_label[0],tr_img,distance)
        if len(self.predictions) > self.ks:
            self.checkCurrentPredictions(training_image)
        else:
            self.predictions.append(training_image)
        self.predictions.sort(key=lambda tup:tup[3])

    def checkCurrentPredictions(self,training_image):
        _,_,_,distance = training_image
        index    = 0
        for _,_,_,p_distance in self.predictions:
            if distance < p_distance:
                self.predictions[index] = training_image
            elif p_distance == distance:
                pred = self.predictions[index]
                self.predictions[index] = random.choice([pred,training_image])
            index+=1




class Testing:
    def __init__(self):
        self.count           = None
        self.imageFd         = None
        self.labelFd         = None
        self.training_images = None
        self.initiatefd()
    def initiatefd(self):
        imageHeaderType  = np.dtype([('count',np.uint32),('width',np.uint16),('height',np.uint16)])
        self.imageFd     = open("testing-images.bin","rb")
        self.labelFd     = open("testing-labels.bin","rb")
        self.header      = np.fromfile(self.imageFd,count=1,dtype=imageHeaderType)[0]
        self.labelHeader = np.fromfile(self.labelFd,count=1,dtype="uint32")
        self.count       = self.header[0]
    def getImageDataWithLabel(self):
        img_fd   = self.imageFd
        label_fd = self.labelFd
        image    = np.fromfile(img_fd,dtype=np.uint8,count=1024)
        label    = np.fromfile(label_fd,dtype=np.uint8,count=1)
        return(image,label)
    def initTesting(self):
        correct   = self.count
        incorrect = None
        for test_id in range(self.count-1):
            test_image,test_label       = self.getImageDataWithLabel()
            self.predict(test_image,test_label)
        self.close_files()
    def predict(self,test_image,test_label):
        KPredictor          = Predictor()
        initialiizing      = 1
        current_distance   = None
        id                 = 0
        KPredictor.testing_image = test_image
        for training_image, label in self.training_images:
            tr_tuple = (id,label,training_image)
            KPredictor.test(tr_tuple)
            id+=1
        print(test_label,"<---testin")
        print("\n\n",KPredictor.predictions)

    def close_files(self):
        self.imageFd.close()
        self.labelFd.close()

class Training:
    def __init__(self):
        self.some= ""
    def get_training_images(self):
        label       = open("training-labels.bin","rb")
        label_count = np.fromfile(label,np.uint32,count=1)
        h_type      = np.dtype([('c',np.uint32),('w',np.uint16),('h',np.uint16)])
        images_and_labels=[]
        with open("training-images.bin","rb") as file:
            header      = np.fromfile(file,dtype=h_type,count=1)
            image_count = header[0][0]
            for _ in range(image_count-1):
                image           = np.fromfile(file,count=1024,dtype=np.uint8)
                label_for_image = np.fromfile(label,count=1,dtype=np.uint8)
                images_and_labels.append((image,label_for_image))
            label.close()
        return images_and_labels
if __name__ == "__main__":
    Trainer = Training()
    Tester  = Testing()
    Tester.training_images = Trainer.get_training_images()
    Tester.initTesting()
