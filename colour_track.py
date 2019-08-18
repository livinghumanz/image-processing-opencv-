import cv2
import numpy as np
def nothing(x):
    pass
cv2.namedWindow("trackbars")
cap=cv2.VideoCapture(0)
cv2.createTrackbar("L- H","trackbars",0,179,nothing)
cv2.createTrackbar("L- S","trackbars",0,255,nothing)
cv2.createTrackbar("L- V","trackbars",0,255,nothing)
cv2.createTrackbar("U- H","trackbars",179,179,nothing)
cv2.createTrackbar("U- S","trackbars",255,255,nothing)
cv2.createTrackbar("U- V","trackbars",255,255,nothing)
while True:
    _,frame =cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L- H","trackbars")
    l_s = cv2.getTrackbarPos("L- S","trackbars")
    l_v = cv2.getTrackbarPos("L- V","trackbars")
    u_h = cv2.getTrackbarPos("U- H","trackbars")
    u_s = cv2.getTrackbarPos("U- S","trackbars")
    u_v = cv2.getTrackbarPos("U- V","trackbars")
    lower_blue = np.array([l_h,l_s,l_v])
    upper_blue = np.array([u_h,u_s,u_v])
    mask=cv2.inRange(hsv,lower_blue,upper_blue)
    result=cv2.bitwise_and(frame,frame,mask=mask)
    cv2.imshow("frame",frame)
    cv2.imshow("mask",mask)
    cv2.imshow("result",result)
    key = cv2.waitKey(1)
    if key==27:
        break
cap.release()
cv2.destroyAllWindows()
