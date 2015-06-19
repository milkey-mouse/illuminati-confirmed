import cv2
capture = cv2.VideoCapture("space_weird_thing.mp4")
while True:
    flag, frame = capture.read() #Flag returns 1 for success, 0 for failure. Frame is the currently processed frame

    if flag == 0: #Something is wrong with your data, or the end of the video file was reached
        break
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()