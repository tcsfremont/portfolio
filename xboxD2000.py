from picamera import PiCamera
from picamera.array import PiRGBArray
from tempimage import TempImage
import imutils
import time
import cv2  
import dropbox
import datetime
#import Buzzer


#Buzzer.Blink()
camera = PiCamera()
camera.resolution = tuple([640, 480])
camera.framerate = 40 
capture = PiRGBArray(camera, size=tuple([640,480]))

use_dropbox = True
if use_dropbox:
	# connect to dropbox and start the session authorization process
	client = dropbox.Dropbox("80CdKUTYMMAAAAAAAAAAL9nOnzcX08P4zqTjS4FfSHAGikDfWcHt_U3_PXix3Awj")
	print("[SUCCESS] dropbox account linked")

print(" ... loading ... ")
time.sleep(2.5)

avg = None
show_video = True
text = "Empty"
lastUploaded = datetime.datetime.now()
motionCounter = 0
dropbox_base_path="student_area/pranay"

for f in ( camera.capture_continuous(capture, format = "bgr", use_video_port = True)):
    text = "Empty"
    timestamp = datetime.datetime.now()
    frame = f.array

    frame = imutils.resize(frame, width = 800)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    if avg is None:
        print(" getting background...")
        avg = gray.copy().astype("float")
        capture.truncate(0)
        continue

    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDifference = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    thresh = cv2.threshold(frameDifference, 5, 255,
            cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # loop over the contours
    for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 5000:
                    continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"

    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")

    # check to see if the room is occupied
    if text == "Occupied":
        print(timestamp- lastUploaded).seconds
        print(lastUploaded)
        # check to see if enough time has passed between uploads
        if (timestamp - lastUploaded).seconds >= 10:
            # increment the motion counter
            motionCounter += 1
            print(motionCounter)

            # check to see if the number of frames with consistent motion is
            # high enough
            if motionCounter >= 8:
                #check to see if dropbox sohuld be used
                if use_dropbox:
                    # write the image to temporary file
                    t = TempImage()
                    cv2.imwrite(t.path, frame)
                    # upload the image to Dropbox and cleanup the tempory image
                    print("[UPLOAD] {}".format(ts))
                    path = "/{base_path}/{timestamp}.jpg".format(
                            base_path=dropbox_base_path, timestamp=ts)
                    client.files_upload(open(t.path, "rb").read(), path)
                    t.cleanup()
                    # update the last uploaded timestamp and reset the motion
                    # counter
                    lastUploaded = timestamp
                    motionCounter = 0

    # otherwise, the room is not occupied
    else:
        print ("reset counter")
        motionCounter = 0



    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    if show_video :
        cv2.imshow("X-Box Dynamyic 2000", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    capture.truncate(0)


