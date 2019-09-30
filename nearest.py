import struct
import numpy as np
from math import sqrt
np.set_printoptions(threshold=np.nan)
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
            label_prediction,train_id   = self.predict(test_image)
            print(test_id,test_label[0],end=" ")
            print(train_id,label_prediction[0])
            if test_label != label_prediction:correct-=1
        incorrect = self.count - correct
        print(correct,incorrect,float(correct/self.count))
        self.close_files()
    def predict(self,test_image):
        current_prediction = None
        initialiizing      = 1
        current_distance   = None
        id                 = 0
        for training_image, label in self.training_images:
            if initialiizing:
                current_prediction =(label,id)
                current_distance   = sqrt(np.sum(test_image!=training_image))
                initialiizing      = 0
                continue
            distance = sqrt(np.sum(test_image!=training_image))
            if distance < current_distance:
                current_distance   = distance
                current_prediction = (label,id)
            id+=1
        return current_prediction
    def close_files(self):
        self.imageFd.close()
        self.labelFd.close()

class Training:
    def __init__(self):
        self.some= ""
    def get_training_images(self):
        label = open("training-labels.bin","rb")
        label_count = np.fromfile(label,np.uint32,count=1)
        h_type = np.dtype([('c',np.uint32),('w',np.uint16),('h',np.uint16)])
        images_and_labels=[]
        with open("training-images.bin","rb") as file:
            header = np.fromfile(file,dtype=h_type,count=1)
            image_count = header[0][0]
            for _ in range(image_count-1):
                image = np.fromfile(file,count=1024,dtype=np.uint8)
                label_for_image = np.fromfile(label,count=1,dtype=np.uint8)
                images_and_labels.append((image,label_for_image))
            label.close()
        return images_and_labels
if __name__ == "__main__":
    Trainer = Training()
    Tester  = Testing()
    Tester.training_images = Trainer.get_training_images()
    Tester.initTesting()
