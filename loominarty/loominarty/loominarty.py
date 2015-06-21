import cv2
import math
import time
import numpy as np
import peladophobian
#qqqcapture = cv2.VideoCapture("space_weird_thing.mp4")
capture = cv2.VideoCapture("dhmis.mp4")
#capture = cv2.VideoCapture(2)
visualizing = True
drawAllEdges = True
framethresh = [(-200,-200)]
lastsucceeded = (-200,-200)
future = time.time() + 1
fps = 0
triangles = 0
narrator = peladophobian.peladophobian()
lfc = [[300,300,300]]*8
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
        if flag == 0:
            break
        fps += 1
        width = frame.shape[0]
        height = frame.shape[1]
        ul = frame[0][0]     #get corners
        ur = frame[width-1,0]
        ll = frame[0,height-1]
        lr = frame[width-1,height-1]
        hw = (width/2)
        hh = (height/2)
        iul = frame[hw,hh]
        iur = frame[hw+1,hh]
        ill = frame[hw,hh+1]
        ilr = frame[hw+1,hh+1]
        nlfc = (ul,ur,ll,lr,iul,iur,ill,ilr)
        pix_epsilon = 5
        issimilar = True
        for pix in range(0,len(nlfc)-1): #epsilon of corners
            for color in range(0,2):
                ocol = lfc[pix][color] 
                ncol = nlfc[pix][color]
                diff = abs(ocol-ncol) 
                if diff > pix_epsilon:
                    issimilar = False
                    break
            if issimilar == False:
                break
        if issimilar == True:
            break
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
                for lidx,lidy in [(0,1),(1,2),(2,0)]:
                    x = pts[lidx][0]
                    y = pts[lidy][0] 
                    dists.append(math.hypot(x[1] - x[0], y[1] - y[0]))
                min_length = min(dists)
                max_length = max(dists)
                maxdist = (max_length/min_length)
                perimeter = cv2.arcLength(cnt,True)
                if maxdist < 1.05 and (area / perimeter) > 5:
                    color = (0,127,255)
                    for ellipse in framethresh:
                        y = pts[0][0]
                        if visualizing:
                            cv2.circle(frame, ellipse, 75, (128,255,128))
                        if abs(math.hypot(ellipse[1] - ellipse[0], y[1] - y[0])) > 75 and abs(math.hypot(lastsucceeded[1] - lastsucceeded[0], y[1] - y[0])) > 75:
                            color = (0,255,0)
                            narrator.mlgsay("Wake up sheeple. We have a triangle. It must be the work of the Illuminati.")
                            triangles += 1
                            newframethresh = [(-300,-300)]
                            framethresh = []
                            lastsucceeded = (pts[0][0][0],pts[0][0][1])
                            skipall = True
                            break
                    if visualizing:
                        ndists = ""
                        for dist in dists:
                            ndists += str(round(dist)) + "\n"
                        cv2.putText(frame, ndists, (pts[0][0][0],pts[0][0][1]), cv2.FONT_HERSHEY_PLAIN, 2, color, thickness=4, lineType=cv2.CV_AA)
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