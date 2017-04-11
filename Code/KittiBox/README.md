# KittiBox  --  implementation on windows10 GeForce960

Based on the project KittiBox https://github.com/MarvinTeichmann/KittiBox
This is the compiled version of KittiBox, with the system os as windows10, and gpu of GeForce960
I wrote this to leave a note for myself, as it WORKED. 
And I am with the hope of getting hints for others, just like many open sources helped me.

Ok let's talk about how to make it work.... pls follow these steps:
##  nividia driver
cuda toolkit v8.0 

## cuDNN v5.1 
You will need to register and answer some questions before download....
https://developer.nvidia.com/rdp/cudnn-download, making sure the version selected is for cuda8.0 and windows10.
unzip cuDNN and put the 3 files into corresponding folders in path for cudatoolkit, such as C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v8.0. Yes, just copy them over, that's the best installation.

## Microsof visual studio cpp
visual studio 2015 community,  Microsoft Visual C++ and its sdk etc, the more complete (C++) the better... 
test your installation via opening project: Samples_vs2015.sln
at:  C:\ProgramData\NVIDIA Corporation\CUDA Samples\v8.0

## python3.5 
install python3.5, then install the following packages by downloading .whl from http://www.lfd.uci.edu/~gohlke/pythonlibs/ and 

cmd:  pip install xxx_cp35‑cp35m‑win_amd64.whl

* matplotlib
* numpy
* Pillow
* scipy
* cython
* tensorflow-gpu, (pip install tensorflow-gpu, or follow the guidance at tensorflow web)
test your installation via cmd->python->import xxx (such as:matplotlib)
The do what tells you at: https://github.com/sturlamolden/cython-cpp-test

## kittibox
download this kittibox project

cmd:  d:

cmd： cd D:\PyProj\DD2017\Code\KittiBox\submodules\utils 

cmd:  python setup.py build_ext --inplace

this should give you a re-maked file, stitch_wrapper.pyd
     
## varify    
cmd: python `demo.py --input_image data/demo.png` #to obtain a prediction using [demo.png](data/demo.png) as input.

Run: `python evaluate.py` #to compute train and validation scores.

Run: `python train.py` #to train a new model on the Kitti Data.


# Acknowledge
This project started out as a fork of [KittiBox](https://github.com/MarvinTeichmann/KittiBox).

-------

