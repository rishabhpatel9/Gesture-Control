import numpy as np
import os
import cv2

filename = 'video.mp4'
frames_per_second = 10.0
res = '720p'

# Set resolution for the video capture
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
}

# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["720p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['mp4']

cap = cv2.VideoCapture(1)
out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

while True:
    ret, frame = cap.read()
    #cv2.imshow('rgb', frame)

    #Region of Interest
    roi=frame[100:300, 100:200]    
    cv2.rectangle(frame,(100,100),(600,400),(100,255,0),0) 
    cv2.imshow('roi', frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    lower_blue = np.array([0, 48, 80]) #([0, 20, 70]) 
    upper_blue = np.array([20, 255, 255]) 
    mask = cv2.inRange(hsv, lower_blue, upper_blue) 
    result = cv2.bitwise_and(frame, frame, mask = mask)
    frame = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    out.write(frame)

    cv2.imshow('frame', mask) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()