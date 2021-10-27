FROM ubuntu:20.04
MAINTAINER Juri Bieler


RUN apt-get update 
RUN apt-get upgrade -y

# Install gstreamer and opencv dependencies
RUN \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata

RUN \
	apt-get install -y \
	libgstreamer1.0-0 \
	gstreamer1.0-plugins-base \
	gstreamer1.0-plugins-good \
	gstreamer1.0-plugins-bad \
	gstreamer1.0-plugins-ugly \
	gstreamer1.0-libav \
	gstreamer1.0-doc \
	gstreamer1.0-tools \
	libgstreamer1.0-dev \
	libgstreamer-plugins-base1.0-dev


RUN \
	apt-get install -y git

# just for testing
RUN \
	apt-get -y install nano net-tools netcat

# setup python
RUN \
	apt-get install -y python3-pip

RUN \
	pip3 install numpy

# get opencv and build it
RUN \
	git clone https://github.com/opencv/opencv.git

RUN \
	apt-get install -y build-essential libssl-dev

RUN \
	apt-get -y install cmake

RUN \
	cd opencv && \
	git checkout 4.5.4 && \
	git submodule update --recursive --init && \
	mkdir build && \
	cd build && \
	cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D INSTALL_C_EXAMPLES=OFF \
	-D PYTHON_EXECUTABLE=$(which python3) \
	-D BUILD_opencv_python2=OFF \
	-D CMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") \
	-D PYTHON3_EXECUTABLE=$(which python3) \
	-D PYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
	-D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
	-D WITH_GSTREAMER=ON \
	-D BUILD_EXAMPLES=ON .. && \
	make -j$(nproc) && \
	make install && \
	ldconfig


	
