import numpy as np
np.set_printoptions(threshold=np.nan)
def typeOfData(line):
  if line[0] == "#" or line[0] == "P":
    return "unnecessary"
class Cleaner:
  def getP2Data(fromPath):
    with open(fromPath) as p2File:
      data = p2File.read().rstrip().split('\n')
      header = False
      for index,d in enumerate(data):
        if typeOfData(d) == "unnecessary":
          header = True
        elif header:
          header = False
        else:
          image=np.array(data[index+1:]).astype('uint8')
          image=np.where(image==255,0,1).astype('uint8')
          return image.tobytes()
  def getP1Data(fromPath):
    with open(fromPath) as p2File:
      data = p2File.read().rstrip().split('\n')
      header = False
      pcount = 0
      for index,d in enumerate(data):
        if typeOfData(d) == "unnecessary":
          header = True
        elif header:
          header = False
        else:
          image = np.array(list(''.join(data[index:]))).astype('uint8')
          return image.tobytes()
  def getP5Data(fromPath):
    with open(fromPath,"rb") as f:
      fileData  = f.read(-1).decode('utf-8').split("\n")
      humanData = fileData[:-1]
      image     = np.fromstring(fileData[-1],dtype='uint8')
      image     = np.where(image==0,1,0).astype('uint8')
      return image.tobytes()
