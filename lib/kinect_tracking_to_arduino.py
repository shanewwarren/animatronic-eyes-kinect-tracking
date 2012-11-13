#!/usr/bin/env python

import freenect
import cv
import frame_convert
import time
import serial
import math

from classifier_group import ClassifierGroup
from classifier import Classifier

def get_video():
    video = freenect.sync_get_video()
    return frame_convert.video_cv(video[0])


def detect_and_display(frame):
    frame_gray = cv.CreateImage(cv.GetSize(frame), frame.depth, 1);
    cv.CvtColor(frame, frame_gray, cv.CV_BGR2GRAY)
    cv.EqualizeHist(frame_gray, frame_gray)

    detected_object = face_group.detect(frame)
    #if detected_object is None:
    #     detected_object = upperbody_group.detect(frame)
    #if detected_object is None:
    #     detected_object = lowerbody_group.detect(frame)
   
    if detected_object is None:
        print "No object detected" 
        return None
    else:  
        x = int(detected_object[0])
        y = int(detected_object[1])
        cv.Rectangle(frame, (x-25,y-25), (x+25, y+25), 255)
        return detected_object

def scale_point(point):
   point_x = point[0]
   point_y = point[1]
   print (point_x/float(640)), radius_x * 2, center_x
   new_x = (((point_x/float(640)) -0.5)  * (radius_x * 2)) + center_x
   new_y = (((point_y/float(480)) - 0.5) * (radius_y * 2)) + center_y
   return (new_x, new_y)

safety_offset = 10
minTilt = 55 + safety_offset
maxTilt = 140 - safety_offset
minPan = 80 + safety_offset
maxPan = 140 - safety_offset

radius_x = (maxPan - minPan)/2
radius_y = (maxTilt - minTilt)/2
center_x = radius_x + minPan
center_y = radius_y + minTilt


def in_ellipse(center_x, center_y, radius_x, radius_y, x, y):
    component_x = ((x - center_x) ** 2) / float(radius_x ** 2)
    component_y = ((y - center_y) ** 2) / float(radius_y ** 2)
    fact = not (component_x + component_y) > 1
    return fact

def get_point_on_ellipse(center_x, center_y, radius_x, radius_y, x, y):
    temp_x = x - center_x
    temp_y = y - center_y
    scale = (radius_x * radius_y)/math.sqrt(((radius_x ** 2) * (temp_y ** 2)) + ((radius_y ** 2) * (temp_x ** 2)))
    coordinate_x = (scale * temp_x) + center_x
    coordinate_y = (scale * temp_y) + center_y
    return (coordinate_x, coordinate_y)

# file name for haar classifier
face_group= ClassifierGroup("FaceGroup") 
#face_group.add_classifier(Classifier("haarcascade_frontalface_alt.xml", "FrontalFaceAlt", (24,24)))
face_group.add_classifier(Classifier("haarcascade_frontalface_alt2.xml", "FrontalFaceAlt2", (24,24)))
face_group.add_classifier(Classifier("haarcascade_frontalface_default.xml", "FrontalFaceDefault", (20,20)))
#face_group.add_classifier(Classifier("haarcascade_frontalface_alt_tree.xml", "FrontalFaceTree", (20,20)))
face_group.add_classifier(Classifier("haarcascade_profileface.xml", "ProfileFace", (20*2,20*2)))

upperbody_group = ClassifierGroup("UpperBodyGroup")
upperbody_group.add_classifier(Classifier("haarcascade_upperbody.xml", "UpperBody", (22,18)))
upperbody_group.add_classifier(Classifier("haarcascade_fullbody.xml", "FullBody", (14, 28)))

lowerbody_group = ClassifierGroup("LowerBodyGroup") 
lowerbody_group.add_classifier(Classifier("haarcascade_lowerbody.xml", "LowerBody", (19, 23)))

# create the windows that'll be used for the application
cv.NamedWindow('Video')

conn = serial.Serial('/dev/ttyACM0', 9600)  
 
while 1:
    
    frame = get_video()
    detected_object = detect_and_display(frame)
    if detected_object is not None:
        print detected_object
        point = scale_point(detected_object)
        print "point!", point
        if not in_ellipse(center_x, center_y, radius_x, radius_y, point[0], point[1]):
            point = get_point_on_ellipse(center_x, center_y, radius_x, radius_y, point[0], point[1])
        
        message = str(int(point[0])).zfill(3) + str(int(point[1])).zfill(3)
        print message
        
        bytes_written = conn.write(message)
        print bytes_written
    
        waiting = conn.inWaiting()
        byte = conn.readline(waiting)
        conn.flush()           
  
    cv.ShowImage('Video', frame)

    time.sleep(3)
    if cv.WaitKey(10) == 27:
        break
