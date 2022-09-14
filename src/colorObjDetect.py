import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

minHue = 100
maxHue = 120
hueRange = 5
minLower = 50
maxUpper = 240
frame = np.zeros((100,100))

# mouse callback function
def onMouseEvent(event,x,y,flags,param):
    global frame, minHue, maxHue
    if event == cv.EVENT_LBUTTONDOWN:
        rgb = np.uint8([[frame[y][x]]])
        color = cv.cvtColor(rgb, cv.COLOR_BGR2HSV)
        hueLow = color[0][0][0] - hueRange
        hueHigh = color[0][0][0] + hueRange
        minHue = max(hueLow, 0)
        maxHue = min(hueHigh, 179)
        print((minHue, maxHue))

cv.namedWindow('frame')
cv.setMouseCallback('frame', onMouseEvent)

while(1):
    _, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lower_color = np.array([minHue, minLower, minLower])
    upper_color = np.array([maxHue, maxUpper,maxUpper])

    mask = cv.inRange(hsv, lower_color, upper_color)

    res = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()