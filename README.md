# Web Cam OpennCV motion detector

The following software is undergoing some refactoring and documentation. For running
Make sure requirements are satisfied.

    $ python motion.py

Will run the main motion detection algorithm. A command line tool facility will be in development soon.

To run using docker container with the motion app:

    $ docker build -t img .
    $ xhost +
    $ docker run -it --privileged -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY  -v $HOME/.Xauthority:/root/.Xauthority img

