#!/bin/sh
git clone --branch 3.0.0 --depth 1 https://github.com/Itseez/opencv.git opencv
cd opencv
mkdir release && cd release
cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX="../.." \
    -DPYTHON_EXECUTABLE="../../bin/python" ..
make -j4
make install
cd ../..
rm -rf opencv
