import cv2
import math
import numpy as np
#capture = cv2.VideoCapture("space_weird_thing.mp4")
capture = cv2.VideoCapture("dhmis.mp4")
while True:
    flag, frame = capture.read() #Flag returns 1 for success, 0 for failure. Frame is the currently processed frame

    if flag == 0: #Something is wrong with your data, or the end of the video file was reached
        break
    frame = cv2.blur(frame, (4,4))
    bframe = cv2.Canny(frame,30,200)
    contours,hierarchy = cv2.findContours(bframe, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        epsilon = 0.03*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        pts = approx.reshape((-1,1,2))
        if len(approx) == 3:
            area = cv2.contourArea(cnt) #750 threshold
            perimeter = cv2.arcLength(cnt,True)
            avg_length = perimeter / 3
            print pts
            has_dists = True
            for lidx in range(0,3):
                x = pts[lidx][0]
                if (lidx + 1) == 3:
                    y = pts[0][0]
                else:
                    y = pts[(lidx + 1)][0]
                avgdist = abs(avg_length-math.hypot(x[1] - x[0], y[1] - y[0]))/avg_length
                if avgdist > 1.5:
                    has_dists = False
                    break
            if area > 650 and (area / perimeter) >= 5:
                color = (0,255,0)
                #cv2.putText(frame, str(avgdists), (pts[0][0][0],pts[0][0][1]), cv2.FONT_HERSHEY_PLAIN, 2, color, thickness=4, lineType=cv2.CV_AA)
            else:
                color = (0,255,255)
            cv2.polylines(frame,[pts],True,color, 5)
        else:
            cv2.polylines(frame,[pts],True,(0,0,255), 5)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()