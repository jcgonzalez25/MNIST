import os
import struct
import subprocess
import random
import numpy as np
from math import floor
from Cleaner import Cleaner
TRAINIMGFNAME = "training-images.bin"
TRAINIMGLABEL = "training-labels.bin"
TESTIMGFNAME  = "testing-images.bin"
TESTLABELS    = "testing-labels.bin"
LABELS        = {"a":1,"b":2,"c":3}
def initHeader(fileName,amountOfImages,labelfile=False):
  with open(fileName,"wb") as file:
    print("wrote Header to",fileName,"amountOfImages",amountOfImages)
    if labelfile:
      header = np.dtype('u4')
      headerForFile = np.array((amountOfImages),dtype=header).tobytes()
    else:
      header = np.dtype('u4,u2,u2')
      headerForFile = np.array((amountOfImages,32,32),dtype=header).tobytes()
    print(headerForFile)
    file.write(headerForFile)
class FileGetter:
  def __init__(self):
    self.pathToFiles     = "/u1/junk/cs617/ABC/"
    self.filesToAdd      = {}
    self.initFiles()
# TODO: figure out why labels arent loading
  def initFiles(self):
    for index,file_name in enumerate(os.listdir(self.pathToFiles)):
      if file_name == 'file.spam':continue
      path = self.pathToFiles+file_name
      label = LABELS[file_name[0]]
      with open(path) as file:
        fileType = file.readline().rstrip()
      self.filesToAdd[index]=[path,fileType,label]
  def writeTo(self,filePath,imageBytes):
    with open(filePath,"ab") as f:
      f.write(imageBytes)
  def writeImageLabelInfo(self,labelFilePath,labelOfImage):
    with open(labelFilePath,"ab") as f:
      byteLabel=np.array(labelOfImage).astype('uint8').tobytes()
      f.write(byteLabel)
  def pickRandFile(self):
    keyID      = random.choice(list(self.filesToAdd.keys()))
    filePicked = self.filesToAdd[keyID]
    self.filesToAdd.pop(keyID)
    # 0->filePath 1->fileType i.e P5 etc. 2->Label a,b,c
    return (filePicked[0],filePicked[1],filePicked[2])
  def initializeHeaders(self,totalImages,trainingFilesAmount):
    testingFilesAmount = totalImages-trainingFilesAmount
    initHeader(TRAINIMGFNAME,trainingFilesAmount)
    initHeader(TESTIMGFNAME,testingFilesAmount)
    initHeader(TRAINIMGLABEL,trainingFilesAmount,True)
    initHeader(TESTLABELS,testingFilesAmount,True)
  def startWritingProcess(self):
    amountOfFiles   = len(self.filesToAdd)
    trainingFiles   = floor(amountOfFiles * .75)
    fileToWriteData = TRAINIMGFNAME
    labelToWriteTo  = TRAINIMGLABEL
    image_data      = 0
    self.initializeHeaders(amountOfFiles,trainingFiles)
    for index,imageCount in enumerate(range(amountOfFiles)):
      filePath,fileType,label = self.pickRandFile()
      if index > trainingFiles:
        fileToWriteData = TESTIMGFNAME
        labelToWriteTo  = TESTLABELS
      if fileType == "P1":
        image_data = Cleaner.getP1Data(filePath)
      elif fileType == "P2":
        image_data = Cleaner.getP2Data(filePath)
      elif fileType == "P5":
        image_data = Cleaner.getP5Data(filePath)
      self.writeImageLabelInfo(labelToWriteTo,label)
      self.writeTo(fileToWriteData,image_data)
if __name__ == "__main__":
  FileObj = FileGetter()
  FileObj.startWritingProcess()
