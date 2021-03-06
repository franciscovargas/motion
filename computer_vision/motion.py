import random as r
import numpy as np
import cv2

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
    imagem :: ndarray
    """
    imagem = (255 - imagem)
    return imagem


def blur_thresh(img,
                sigX=0,
                sigY=0,
                size=20,
                lower_pix=2,
                upper_pix=255):
    # Gaussian kernel blur when sigX and sigY set
    # to 0 variances are computed automatically
    # based on size
    initial_blur = cv2.GaussianBlur(img,
                                    (sigX, sigY),
                                    size)
    # binary threshold which takes out very dark pixels
    # which are deemed as not mooving post to the differential
    # images procedure
    ret, thresh = cv2.threshold(initial_blur,
                                lower_pix,
                                upper_pix,
                                cv2.THRESH_BINARY)

    return thresh


def void_conts(circs=False, lines=True):
    """
    This small function/script carries out basic
    computer vision methods (thresholding + bluring
    via gaussian kernel) that in conjunction to 
    differential images allow for the detection of motion

    TODO: Maybe abstract the bluring set up and the inner
    loop bluring process.
    """
    # Initialize camera
    cam = cv2.VideoCapture(-1)

    # Obtain dimensions of window
    width = int(cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH
                        ))
    height = int(cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT
                         ))

    # bbb

    #  Read in first image and greyscale.
    initial_img = cam.read()[1]

    # Initial setup for differential images
    # tracking technique
    # t_minus = image in the past
    # t = image in the present

    t_minus = cv2.cvtColor(initial_img,
                           cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(initial_img,
                     cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(initial_img,
                          cv2.COLOR_RGB2GRAY)

    while True:
        # Random colors for countours and balls
        c1, c2, c3 = (r.randint(0, 255),
                      r.randint(0, 255),
                      r.randint(0, 255))
        b1, b2, b3 = (r.randint(0, 255),
                      r.randint(0, 255),
                      r.randint(0, 255))

        # Blur and threshold differential image to
        # Extract motion as a binary image
        thresh = blur_thresh(diffImg(t_minus,
                                     t,
                                     t_plus))

        # contours of thresholded image
        con, h = cv2.findContours(thresh,
                                  cv2.RETR_TREE,
                                  cv2.CHAIN_APPROX_SIMPLE)

        # Actual colored frame
        frame = cam.read()[1]
        # Used for testing CV methods
        img2 = np.zeros((512, 512, 3),
                        np.uint8) + 255
        # 70 200 290

        # For drawing contours
        if lines:
            img = cv2.drawContours(frame, con, -1, (
                b1,
                b2,
                b3), 3)

        # For drawing circles, looks pretty why not.
        if len(con) >= 1 and circs:
            for index, cn in enumerate(con):
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
            # print "\nProgram terminidated with ESC key.\n"
            break
    cam.release()
    cv2.destroyWindow('frame')


def inter_act():
    """
    In development. This function allows you to play with a ball on
    screan. Sadly it is quite suceptible to noise and no proper physics
    governs the motion of the ball at the moment.
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

    # Starting position of the ball
    x, y = (320, 240)

    while True:
        c1, c2, c3 = (r.randint(0, 255),
                      r.randint(0, 255),
                      r.randint(0, 255))

        # Look in to abstractions here since this is
        # repeated code.
        initial_blur = cv2.GaussianBlur((diffImg(t_minus,
                                                 t,
                                                 t_plus)),
                                        (0, 0),
                                        20)
        ret, thresh = cv2.threshold(initial_blur,
                                    2,
                                    255,
                                    cv2.THRESH_BINARY)

        # Convert from numpy.where()'s two
        # separate lists to one list of (x, y) tuples:
        con, h = cv2.findContours(thresh,
                                  cv2.RETR_TREE,
                                  cv2.CHAIN_APPROX_SIMPLE)

        frame = cam.read()[1]
        img2 = np.zeros((512, 512, 3),
                        np.uint8) + 255

        # Blue ball which appears on the screen
        # and is sensitive to motion
        # Ball should be abstracted as an object
        ball = cv2.circle(frame, (x, y),
                          30,
                          255,
                          -1)
        # Bounding box around ball which is incremented
        # When ball has been touched
        # Need to do some actual physics here...
        # instead of a chain of conditions that make
        # little sense.
        if len(con) >= 1:
            for index, cn in enumerate(con):
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

        # Read next image and update differential frames
        t_minus = t
        t = t_plus
        t_plus = cv2.cvtColor(cam.read()[1],
                              cv2.COLOR_RGB2GRAY)

        key = cv2.waitKey(10)

        # If key is exit key break
        if key == 27:
            # print "\nProgram terminidated with ESC key.\n"
            break
    cam.release()
    cv2.destroyWindow('frame')


if __name__ == "__main__":
    void_conts()
    # inter_act()
