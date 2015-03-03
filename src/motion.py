import cv2
import random as r
import numpy as np


def diffImg(t0,
            t1,
            t2):
    """
    Args:
    t0 first frame :: ndarray
    t1 second frame :: ndarray
    t2 third frame :: ndarray
    
    This function takes in 3 frames detecting
    the absolute difference in between them
    to then conjunct the differences returning
    the change in pixels.
    In a sense this quantifies the motion.

    Returns:
    cv2.bitwise_and(d1,d2) :: ndarray
    """
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


def inverte(imagem):
    """
    Args
    imagem :: ndarray
    takes in an image
    and ireturns an inverted image

    Returns
    imagem ::ndarray
    """
    imagem = (255 - imagem)
    return imagem


def void_conts():
    """
    In a sense this is a main like method
    it takes in nothing and returns nothing (void)
    but it does trigger IO and uses both binary thresh-
    holds and gaussian kernels to detect motion
    from the web cam, plotting it as a countour plot
    which then changes collor randomly
    """
    cam = cv2.VideoCapture(0)

    width = int(cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH
                        ))
    height = int(cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT
                         ))

    initial_blur = cv2.GaussianBlur(cam.read()[1],
                                   (5, 5),
                                    0)
    t_minus = cv2.cvtColor(initial_blur,
                           cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(initial_blur,
                     cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(initial_blur,
                          cv2.COLOR_RGB2GRAY)

    x, y = (320, 240)

    while True:
        c1, c2, c3 = (r.randint(0, 255),
                      r.randint(0, 255),
                      r.randint(0, 255))
        b1, b2, b3 = (r.randint(0, 255),
                      r.randint(0, 255),
                      r.randint(0, 255))
        initial_blur = cv2.GaussianBlur((diffImg(t_minus,
                                                 t,
                                                 t_plus)),
                                        (0, 0),
                                        15)
        ret, thresh = cv2.threshold(initial_blur,
                                    2,
                                    255,
                                    cv2.THRESH_BINARY)
        second_blur = cv2.GaussianBlur(thresh,
                                       (5, 5),
                                       15)
        ret2, thresh2 = cv2.threshold(second_blur,
                                      240,
                                      255,
                                      cv2.THRESH_BINARY)
        # Convert from numpy.where()'s two
        #separate lists to one list of (x, y) tuples:
        con, h = cv2.findContours(thresh2,
                                  cv2.RETR_TREE,
                                  cv2.CHAIN_APPROX_SIMPLE)
        cnt = con[:]
        frame = cam.read()[1]
        img2 = np.zeros((512, 512, 3),
                        np.uint8) + 255
#70 200 290
        img = cv2.drawContours(frame, cnt, -1, (
            b1,
            b2,
            b3), 3)

        if len(cnt) >= 1:
            for index, cn in enumerate(cnt):
                center = tuple(cn[0][0])
                cv2.circle(frame,
                           center,
                           20,
                           (c1, c2, c3),
                           -1)

        cv2.imshow('img2',
                   frame)
        # Read next image:
        t_minus = t
        t = t_plus
        t_plus = cv2.cvtColor(cam.read()[1],
                              cv2.COLOR_RGB2GRAY)

        key = cv2.waitKey(10)
        if key == 27:

            break
    cam.release()
    cv2.destroyWindow('frame')
    print"#######################################################"


def inter_act():
    cam = cv2.VideoCapture(0)

    width = int(cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH
                        ))
    height = int(cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT
                         ))

    initial_blur = cv2.GaussianBlur(cam.read()[1],
                                   (5, 5),
                                    0)
    t_minus = cv2.cvtColor(initial_blur,
                           cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(initial_blur,
                     cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(initial_blur,
                          cv2.COLOR_RGB2GRAY)

    x, y = (320, 240)

    while True:
        c1, c2, c3 = (r.randint(0, 255),
                      r.randint(0, 255),
                      r.randint(0, 255))
        initial_blur = cv2.GaussianBlur((diffImg(t_minus,
                                                 t,
                                                 t_plus)),
                                        (0, 0),
                                        15)
        ret, thresh = cv2.threshold(initial_blur,
                                    2,
                                    255,
                                    cv2.THRESH_BINARY)
        second_blur = cv2.GaussianBlur(thresh,
                                       (5, 5),
                                       15)
        ret2, thresh2 = cv2.threshold(second_blur,
                                      240,
                                      255,
                                      cv2.THRESH_BINARY)
        # Convert from numpy.where()'s two
        #separate lists to one list of (x, y) tuples:
        con, h = cv2.findContours(thresh2,
                                  cv2.RETR_TREE,
                                  cv2.CHAIN_APPROX_SIMPLE)
        cnt = con[:]
        frame = cam.read()[1]
        img2 = np.zeros((512, 512, 3),
                        np.uint8) + 255
        """
        img = cv2.drawContours(frame, cnt, -1, (
            70,
            200,
            290), 3)
        """
        ball = cv2.circle(frame, (x, y),
                          30,
                          255,
                          -1)

        if len(cnt) >= 1:
            for index, cn in enumerate(cnt):
                center = tuple(cn[0][0])
                if center[0] > x - 45 and center[0] < x:
                    x += 20
                if center[0] >= x and center[0] < x + 45:
                    x -= 20
                if center[0] > y - 45 and center[0] < y:
                    y += 20
                if center[0] >= y and center[0] < x + 45:
                    y -= 20
                if y <= 10:
                    y += 50
                if y >= 460:
                    y -= 50
                if x <= 10:
                    x += 50
                if x >= 620:
                    y -= 50

        cv2.imshow('img2',
                   frame)
        # Read next image:
        t_minus = t
        t = t_plus
        t_plus = cv2.cvtColor(cam.read()[1],
                              cv2.COLOR_RGB2GRAY)

        key = cv2.waitKey(10)
        if key == 27:

            break
    cam.release()
    cv2.destroyWindow('frame')
    print"#######################################################"


def void_circles():
    cam = cv2.VideoCapture(0)

    width = int(cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH
                        ))
    height = int(cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT
                         ))

    initial_blur = cv2.GaussianBlur(cam.read()[1],
                                   (5, 5),
                                    0)
    t_minus = cv2.cvtColor(initial_blur,
                           cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(initial_blur,
                     cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(initial_blur,
                          cv2.COLOR_RGB2GRAY)

    x, y = (320, 240)

    while True:
        c1, c2, c3 = (r.randint(0, 255),
                      r.randint(0, 255),
                      r.randint(0, 255))
        initial_blur = cv2.GaussianBlur((diffImg(t_minus,
                                                 t,
                                                 t_plus)),
                                        (0, 0),
                                        15)
        ret, thresh = cv2.threshold(initial_blur,
                                    2,
                                    255,
                                    cv2.THRESH_BINARY)
        second_blur = cv2.GaussianBlur(thresh,
                                       (5, 5),
                                       15)
        ret2, thresh2 = cv2.threshold(second_blur,
                                      240,
                                      255,
                                      cv2.THRESH_BINARY)
        # Convert from numpy.where()'s two
        #separate lists to one list of (x, y) tuples:
        con, h = cv2.findContours(thresh2,
                                  cv2.RETR_TREE,
                                  cv2.CHAIN_APPROX_SIMPLE)
        cnt = con[:]
        frame = cam.read()[1]
        img2 = np.zeros((512, 512, 3),
                        np.uint8) + 255
        """
        img = cv2.drawContours(frame, cnt, -1, (
            70,
            200,
            290), 3)
        """

        if len(cnt) >= 1:
            for index, cn in enumerate(cnt):
                center = tuple(cn[0][0])
                cv2.circle(frame,
                           center,
                           20,
                           (c1, c2, c3),
                           -1)

        cv2.imshow('img2',
                   frame)
        # Read next image:
        t_minus = t
        t = t_plus
        t_plus = cv2.cvtColor(cam.read()[1],
                              cv2.COLOR_RGB2GRAY)

        key = cv2.waitKey(10)
        if key == 27:

            break
    cam.release()
    cv2.destroyWindow('frame')
    print"#######################################################"

#inter_act()
#void_conts()
