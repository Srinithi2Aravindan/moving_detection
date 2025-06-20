import cv2 #to open cv
import imutils #to resize image

cam = cv2.VideoCapture(0) #initializing camera id

firstFrame = None
area = 500

while True:
    _, img = cam.read()  #read from camera
    text = "Normal"

    img = imutils.resize(img, width = 1000) #resize img
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #color to grayscale
    gaussianImg = cv2.GaussianBlur(grayImg, (21,21), 0) #smoothened

    if firstFrame is None:
        firstFrame = gaussianImg
        continue

    imgDiff = cv2.absdiff(firstFrame, gaussianImg) #absolute difference

    threshImg = cv2.threshold(imgDiff, 25, 255, cv2.THRESH_BINARY)[1]
    threshImg = cv2.dilate(threshImg, None, iterations =2) #to remove left over erotion

    counts = cv2.findContours(threshImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    counts = imutils.grab_contours(counts)

    for c in counts:
        if cv2.contourArea(c) < area:
            continue
        (x,y,w,h) = cv2.boundingRect(c)
        cv2.rectangle(img,(x,y),(x+w , y+h),(0,255,0),2)
        text = "Moving object detected"
    print(text)
    cv2.putText(img,text, (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
    cv2.imshow("CameraFeed" ,img)

    key = cv2.waitKey(10)
    print(key)
    if key == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()

        
        
