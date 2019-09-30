#!/usr/bin/python3
import sys
import numpy as np
np.set_printoptions(threshold=np.nan)
if __name__ == "__main__":
  if sys.argv[1] == "header":
    fname = sys.argv[2]
    headerType = np.dtype([('count',np.uint32),('width',np.uint16),('height',np.uint16)])
    with open("training-images.bin","rb") as file:
      x=np.fromfile(file,dtype=headerType,count=1)
      print(x)
      pixelData = np.fromfile(file,dtype=np.uint8,count=1024)
      print(pixelData.reshape(32,32))
    with open("training-labels.bin","rb") as file:
      x = np.fromfile(file,dtype=np.uint32,count=1)
      print(x)
      l = np.fromfile(file,dtype=np.uint8,count=1)
      print(l)
