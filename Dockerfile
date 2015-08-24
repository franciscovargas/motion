FROM	ubuntu:14.04

RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update
RUN	apt-get install -y -q wget curl
RUN	apt-get install -y -q build-essential
RUN	apt-get install -y -q cmake
RUN  apt-get install -y -q libgtk2.0-dev pkg-config git
RUN	apt-get install -y -q python2.7 python2.7-dev
RUN	\
  wget 'https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg' && \
  /bin/sh setuptools-0.6c11-py2.7.egg && \
  rm -f setuptools-0.6c11-py2.7.egg

RUN	 curl 'https://bootstrap.pypa.io/get-pip.py' -o 'get-pip.py'
RUN  python2.7 get-pip.py
# RUN  apt-get install -y python-pip python-dev build-essential
RUN  pip install -U setuptools
RUN  pip install  -U pip 
RUN  pip install  -U virtualenv
RUN	 pip install -U numpy
RUN	apt-get install -y -q libavformat-dev libavcodec-dev libavfilter-dev libswscale-dev
RUN	apt-get install -y -q libjpeg-dev libpng-dev libtiff-dev libjasper-dev zlib1g-dev libopenexr-dev libxine-dev libeigen3-dev libtbb-dev
RUN apt-get install -y -q libtbb2 libdc1394-22-dev
ADD	cv.sh	cv.sh
RUN	chmod a+x cv.sh
RUN	apt-get install -y unzip
RUN	./cv.sh
ADD computer_vision computer_vision
RUN apt-get install build-essential
RUN dpkg-reconfigure -phigh build-essential
RUN ls -q dev/stdout
RUN  apt-get install -y -q cheese
RUN  grep -e video /etc/group
RUN apt-get install -y aptitude
RUN aptitude install -y tree

# RUN chown root.video /dev/usb/video*
RUN   mknod /dev/video0 c 81 0
ADD MAKEDEV MAKEDEV
RUN chmod u+x MAKEDEV
RUN ./MAKEDEV
RUN aptitude install -y xawtv
# RUN chmod g+rw dev/video0

# RUN  chmod 777 dev/video*

CMD python computer_vision/motion.py