# Machine Learning Numset
Working with MNIST dataset of hand written images can be found [HERE](http://yann.lecun.com/exdb/mnist/)
## Technologies Used:
* Numpy 
* Knearest Neighbor algoritthms
## Solution
* Converter transorms such data into appropiate binary data
```
TRAINIMGFNAME = "training-images.bin"
TRAINIMGLABEL = "training-labels.bin"
TESTIMGFNAME  = "testing-images.bin"
TESTLABELS    = "testing-labels.bin"
```
* Cleaner class takes binary and based on its type `p1 p2 p5` transforms it into the same binary format. Look at `cleaner.py` to understand further.

* Trainer reads and performs knearest, once testing performs a predition which is associated with a label. whichever label its prediction is closest is the overall chosen predition

### Run `test.py` 
* to see if the alphabet images were loaded correctly
## Evaluation 
* Only 83 percent accurate, planning to scale the picture size.
