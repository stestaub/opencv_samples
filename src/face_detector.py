from mimetypes import init
import cv2 as cv
import numpy as np

def in_rect(lowerl, upperr, pt):
    return lowerl <= pt and pt <= upperr


def set_scale(value):
    global scaleFactor
    scaleFactor = max(1.1,value / 10.0)

def set_minNeighbors(value):
    global minNeighbors
    minNeighbors = value

def init_from_frame(frame):
    global initialized, lockin_lowerl, lockin_upperr
    if initialized: 
        return
    width = len(frame[0])
    height = len(frame)
    centerX = np.uint(width / 2)
    centerY = np.uint(height / 2)
    lockin_lowerl = (centerX - np.uint(width / 5), centerY - np.uint(height / 5))
    lockin_upperr = (centerX + np.uint(width / 5), centerY + np.uint(height / 5))
    print(width, height)
    print(centerX, centerY)
    print(lockin_lowerl, lockin_upperr)
    initialized = True


initialized = False

face_locked_in = False
lock_in_countdown = 50
lockin_lowerl = np.array((0,0))
lockin_upperr = np.array((0,0))

face_cascade = cv.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')
scaleFactor=1.5
minNeighbors=3


cap = cv.VideoCapture(0)
cv.namedWindow('frame')
cv.createTrackbar('scale', 'frame', 15, 50, lambda v: set_scale(v))
cv.createTrackbar('minNeighbors', 'frame', 3, 15, lambda v: set_minNeighbors(v))

while(1):
    _, frame = cap.read()
    init_from_frame(frame)
    grayScale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(grayScale, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
    for(x, y, w, h) in faces:
        cv.rectangle(frame, (x,y), (x + w, y + h), (255,0,0))

    if not face_locked_in and len(faces) > 0 :
        faceX, faceY, w, h = faces[0]
        if in_rect(lockin_lowerl, lockin_upperr, (faceX, faceY)) and in_rect(lockin_lowerl, lockin_upperr, (faceX + w, faceY + h)):
            cv.rectangle(frame, lockin_lowerl, lockin_upperr, (0,255,0))
        else:
            cv.rectangle(frame, lockin_lowerl, lockin_upperr, (0,0,255))
    else:
        cv.rectangle(frame, lockin_lowerl, lockin_upperr, (0,0,255))


    cv.imshow('frame',frame)
    key = cv.waitKey(2) & 0xFF

    if key == ord('q'):
        break


cap.release()
cv.destroyAllWindows()