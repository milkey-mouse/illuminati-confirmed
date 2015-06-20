import cv2
import math
import time
import numpy as np
#capture = cv2.VideoCapture("space_weird_thing.mp4")
capture = cv2.VideoCapture("dhmis.mp4")
#capture = cv2.VideoCapture(2)
visualizing = True
drawAllEdges = True
framethresh = [(-200,-200)]
future = time.time() + 1
fps = 0
triangles = 0
while True:
    try:
        if not visualizing:
            if time.time() >= future:
                future = time.time() + 1
                print "fps: " + str(fps) + " triangles: " + str(triangles)
                fps = 0
                triangles = 0
        if framethresh == [(-300,-300)]:
            for i in range(1,30):
                flag, frame = capture.read()
                fps += 1
                if flag == 0:
                    break
            skipall = False
        if len(framethresh) == 0:
            for i in range(1,3):
                flag, frame = capture.read()
                fps += 1
                if flag == 0:
                    break
        flag, frame = capture.read() #Flag returns 1 for success, 0 for failure. Frame is the currently processed frame
        fps += 1
        newframethresh = []
        if flag == 0: #Something is wrong with your data, or the end of the video file was reached
            break
        frame = cv2.blur(frame, (3,3))
        bframe = cv2.Canny(frame,30,200)
        contours,hierarchy = cv2.findContours(bframe, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        skipall = False
        for cnt in contours:
            epsilon = 0.04*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon,True)
            pts = approx.reshape((-1,1,2))
            if len(approx) == 3:
                area = cv2.contourArea(cnt) #750 threshold
                has_dists = True
                dists = []
                for lidx in range(0,3):
                    x = pts[lidx][0]
                    if (lidx + 1) == 3:
                        y = pts[0][0]
                    else:
                        y = pts[(lidx + 1)][0]
                        dists.append(math.hypot(x[1] - x[0], y[1] - y[0]))
                min_length = min(dists)
                max_length = max(dists)
                maxdist = (max_length/min_length)
                perimeter = cv2.arcLength(cnt,True)
                if maxdist < 1.1 and (area / perimeter) > 5:
                    color = (0,127,255)
                    for ellipse in framethresh:
                        y = pts[0][0]
                        if visualizing:
                            cv2.circle(frame, ellipse, 75, (128,255,128))
                        if abs(math.hypot(ellipse[1] - ellipse[0], y[1] - y[0])) > 75:
                            color = (0,255,0)
                            triangles += 1
                            newframethresh = [(-300,-300)]
                            framethresh = []
                            skipall = True
                            break
                    if visualizing:
                        cv2.putText(frame, str(maxdist), (pts[0][0][0],pts[0][0][1]), cv2.FONT_HERSHEY_PLAIN, 2, color, thickness=4, lineType=cv2.CV_AA)
                    if skipall == False:
                        newframethresh.append((pts[0][0][0],pts[0][0][1]))
                else:
                    color = (0,255,255)
                if visualizing:
                    cv2.polylines(frame,[pts],True,color, 5)
            else:
                if visualizing and drawAllEdges:
                    cv2.polylines(frame,[pts],True,(0,0,255), 1)
        framethresh = newframethresh
    except:
        pass
    if visualizing:
        try:
            cv2.imshow('frame',frame)
        except:
            pass
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
if visualizing:
    cv2.destroyAllWindows()
