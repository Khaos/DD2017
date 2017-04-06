# KittiBox  --  implementation on windows10 GeForce960

Based on the project KittiBox https://github.com/MarvinTeichmann/KittiBox
This is the compiled version of KittiBox, with the system os as windows10, and gpu of GeForce960
I wrote this to leave a note for myself, as it WORKED. 
And with the hope of getting hints for others, just like many open sources helped me.

## install nividia 
cuda toolkit v8.0 

## downlaod cuDNN v5.1 
for cuda8.0 and windows10
unzip cuDNN and put the 3 files into corresponding folders in path for cudatoolkit, such as C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v8.0

## install MCVS
visual studio 2015 community,  Microsoft Visual C++ and its sdk etc
test your installation via opening project 

## install python3.5 
then install the following packages by downloading .whl from http://www.lfd.uci.edu/~gohlke/pythonlibs/ and cmd;pip install xxx.whl
* matplotlib
* numpy
* Pillow
* scipy
* cython
* Tensorflow-gpu newest, follow the guidance at tensorflow web 
test your installation via running; https://github.com/sturlamolden/cython-cpp-test

## kittibox
download this kittibox project
cmd; cd xxx/kittibox/submodules/utils -> python setup.py build_ext --inplace
     this should give you a re-maked file, stitch_wrapper.pyd
     
## varify    
cmd: python demo.py --input_image data/demo.png #to obtain a prediction using [demo.png](data/demo.png) as input.

Run: `python evaluate.py` to compute train and validation scores.

Run: `python train.py` to train a new model on the Kitti Data.


# Acknowledge
This project started out as a fork of [KittiBox](https://github.com/MarvinTeichmann/KittiBox).

-------

