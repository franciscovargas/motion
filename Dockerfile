FROM	ubuntu:14.04

# Ubuntu sides with libav, I side with ffmpeg.
# RUN	echo "deb http://ppa.launchpad.net/jon-severinsson/ffmpeg/ubuntu quantal main" >> /etc/apt/sources.list
# RUN	apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1DB8ADC1CFCA9579


RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update
RUN	apt-get install -y -q wget curl
RUN	apt-get install -y -q build-essential
RUN	apt-get install -y -q cmake
RUN sudo apt-get install -y -q libgtk2.0-dev pkg-config git
RUN	apt-get install -y -q python2.7 python2.7-dev
RUN	\
  wget 'https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg' && \
  /bin/sh setuptools-0.6c11-py2.7.egg && \
  rm -f setuptools-0.6c11-py2.7.egg

RUN	sudo curl 'https://bootstrap.pypa.io/get-pip.py' -o 'get-pip.py'
RUN sudo python2.7 get-pip.py
# RUN sudo apt-get install -y python-pip python-dev build-essential
RUN sudo pip install -U setuptools
RUN sudo pip install  -U pip 
RUN sudo pip install  -U virtualenv
RUN	sudo pip install -U numpy
RUN	apt-get install -y -q libavformat-dev libavcodec-dev libavfilter-dev libswscale-dev
RUN	apt-get install -y -q libjpeg-dev libpng-dev libtiff-dev libjasper-dev zlib1g-dev libopenexr-dev libxine-dev libeigen3-dev libtbb-dev
RUN apt-get install -y -q libtbb2 libdc1394-22-dev
ADD	cv.sh	cv.sh
RUN	chmod a+x cv.sh
RUN	apt-get install -y unzip
RUN	./cv.sh
ADD computer_vision computer_vision
RUN apt-get install build-essential linux-headers-`uname -r`
RUN dpkg-reconfigure -phigh build-essential linux-headers-`uname -r`
RUN sudo chmod 777 /dev/video*

CMD python2.7 computer_vision/motion.py