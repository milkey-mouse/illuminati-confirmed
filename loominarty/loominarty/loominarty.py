import cv2
import math
import time
import numpy as np
import peladophobian
#capture = cv2.VideoCapture("space_weird_thing.mp4")
#capture = cv2.VideoCapture("dhmis.mp4")
capture = cv2.VideoCapture("loominarty.mp4")
#capture = cv2.VideoCapture("2minarty.mp4")
#capture = cv2.VideoCapture(2)
visualizing = True
drawAllEdges = True
announceTriangles = True
bluramt = 3
distthresh = 1.35
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
        frame = cv2.blur(frame, (bluramt,bluramt))
        bframe = cv2.Canny(frame,30,200)
        contours,hierarchy = cv2.findContours(bframe, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        skipall = False
        for cnt in contours:
            epsilon = 0.04*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon,True)
            pts = approx.reshape((-1,1,2))
            if len(approx) == 3:
                has_dists = True
                dists = []
                for lidx,lidy in [(0,1),(1,2),(2,0)]:
                    x = pts[lidx][0]
                    y = pts[lidy][0] 
                    dists.append(abs(math.hypot(*y-x)))
                min_length = min(dists)
                max_length = max(dists)
                #real_area = math.sqrt(s*(s-dists[0])*(s-dists[1])*(s-dists[2]))
                #theoretical_area = (1.0/4.0) * math.sqrt(3.0) * (max_length**2.0) #this finds the ideal area if the shape were a perfectly equilateral triangle
                #theoretically one could do something like (real_area/theoretical_area) to see another value of equilateralness
                s = sum(dists) / 2.0
                maxdist = (max_length/min_length)
                if maxdist < distthresh:
                    color = (0,127,255)
                    for ellipse in framethresh:
                        y = pts[0][0]
                        if visualizing:
                            cv2.circle(frame, ellipse, 75, (128,255,128))
                        if abs(math.hypot(*y-ellipse)) > 75 and abs(math.hypot(*y-lastsucceeded)) > 75:
                            color = (0,255,0)
                            if announceTriangles:
                                narrator.mlgsay("Wake up sheeple. We have a triangle. It must be the work of the Illuminati.")
                            triangles += 1
                            newframethresh = [(-300,-300)]
                            framethresh = []
                            lastsucceeded = (pts[0][0][0],pts[0][0][1])
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
    except Exception, e:
        if flag == 0:
            break
        else:
            print e
    if visualizing:
        try:
            cv2.imshow('frame',frame)
        except:
            pass
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
if visualizing:
    cv2.destroyAllWindows()