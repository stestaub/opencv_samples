import numpy as np
import cv2 as cv



drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
rectA,rectB = (-1,-1),(-1,-1)

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode, rectA, rectB
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
        rectA, rectB = (ix,iy),(x,y)
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            rectA, rectB = (ix,iy),(x,y)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        rectA, rectB = (ix,iy),(x,y)

cv.namedWindow('original')
cv.setMouseCallback('original',draw_circle)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame... Exiting!")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray,30,0.005,10)
    corners = np.int0(corners)

    cv.rectangle(frame, rectA, rectB, (0,255,0), 3)

    for i in corners:
        x,y = i.ravel()
        cv.circle(frame,(x,y),3,255,-1)

    cv.imshow('original', frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
