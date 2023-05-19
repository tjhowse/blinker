# This watches a number of blinking LEDs and prints out the rough timing of the blinks.
# This is to measure how long blinkers continue to blink for.

from __future__ import print_function
import time
from itertools import count
import cv2
import argparse
import toml
import numpy as np
import datetime
import os
import signal

max_value = 255
max_value_H = 360//2
low_H = 1
low_S = 0
low_V = 185
count_threshold = 10
cam_hue = 255
cam_gain = 255
cam_saturation = 255
high_H = 180
high_S = 255
high_V = 255
high_F = 75
morse_time = 500
click_x = 0
click_y = 0
# This gets populated by clicks on the webcam image to set up points of interest
boxes = []
prev_led_state = []
prev_box_brightness = []
box_size = 5
window_capture_name = 'Click LED'
window_settings_name = 'Settings'
filtered_detection_name = 'Filtered'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
high_F_name = 'Focus'
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos(low_H_name, window_settings_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos(high_H_name, window_settings_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos(low_S_name, window_settings_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos(high_S_name, window_settings_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos(low_V_name, window_settings_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos(high_V_name, window_settings_name, high_V)
def on_F_trackbar(val):
    global high_F
    high_F = val
    cap.set(cv2.CAP_PROP_FOCUS, high_F)
def on_count_trackbar(val):
    global count_threshold
    count_threshold = val
def on_hue_trackbar(val):
    global cam_hue
    cam_hue = val
    cap.set(cv2.CAP_PROP_HUE, cam_hue)
def on_gain_trackbar(val):
    global cam_gain
    cam_gain = val
    cap.set(cv2.CAP_PROP_GAIN, cam_gain)
def on_saturation_trackbar(val):
    global cam_saturation
    cam_saturation = val
    cap.set(cv2.CAP_PROP_SATURATION, cam_saturation)
def on_morse_time_trackbar(val):
    global morse_time
    morse_time = val
def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global click_x
        global click_y
        click_x = x
        click_y = y
        global boxes
        # Check to see whether this click is inside an existing box
        for i, box in enumerate(boxes):
            if box[0] - box_size < x < box[0] + box_size and box[1] - box_size < y < box[1] + box_size:
                # Mark this box as freed up
                boxes[i] = (0,0)
                return
        for i, box in enumerate(boxes):
            # Use the first free box we find.
            if box == (0,0):
                boxes[i] = (x, y)
                return
        # If there are no free boxes, create a new one.
        boxes.append((x, y))
        global prev_led_state
        prev_led_state.append(False)
        prev_box_brightness.append(0)

parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera device number.', default=1, type=int)
args = parser.parse_args()
# cap = cv2.VideoCapture(args.camera, cv2.CAP_DSHOW)
cap = cv2.VideoCapture(args.camera)

cv2.namedWindow(window_capture_name)
cv2.namedWindow(window_settings_name)
cv2.setMouseCallback(window_capture_name, on_click)
cv2.createTrackbar(low_H_name, window_settings_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv2.createTrackbar(high_H_name, window_settings_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv2.createTrackbar(low_S_name, window_settings_name , low_S, max_value, on_low_S_thresh_trackbar)
cv2.createTrackbar(high_S_name, window_settings_name , high_S, max_value, on_high_S_thresh_trackbar)
cv2.createTrackbar(low_V_name, window_settings_name , low_V, max_value, on_low_V_thresh_trackbar)
cv2.createTrackbar(high_V_name, window_settings_name , high_V, max_value, on_high_V_thresh_trackbar)
cv2.createTrackbar(high_F_name, window_settings_name , high_F, max_value, on_F_trackbar)
cv2.createTrackbar("Threshold", window_settings_name , count_threshold, 30000, on_count_trackbar)
cv2.createTrackbar("Hue", window_settings_name , cam_hue, 255, on_hue_trackbar)
cv2.createTrackbar("Gain", window_settings_name , cam_gain, 255, on_gain_trackbar)
cv2.createTrackbar("Saturation", window_settings_name , cam_saturation, 255, on_saturation_trackbar)
cv2.createTrackbar("Morse Time", window_settings_name , morse_time, 1000, on_morse_time_trackbar)

cam = "ps3eye"
if cam == "logitech":
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    cap.set(cv2.CAP_DSHOW, 1)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT , 240)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FPS, 60)
elif cam == "ps3eye":
    # cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    # cap.set(cv2.CAP_DSHOW, 1)
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT , 480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FPS, 60)
    pass

# CAP_PROP_SATURATION
with open("settings_watcher.toml", "r") as f:
    settings = toml.load(f)
    cam_hue = settings["hue"]
    cam_gain = settings["gain"]
    cam_saturation = settings["saturation"]
    high_F = settings["high_F"]

    cap.set(cv2.CAP_PROP_FOCUS, high_F)
    cap.set(cv2.CAP_PROP_SATURATION, cam_saturation)
    cap.set(cv2.CAP_PROP_GAIN, cam_gain)
    cap.set(cv2.CAP_PROP_HUE, cam_hue)

    low_H = settings["low_H"]
    high_H = settings["high_H"]
    low_S = settings["low_S"]
    high_S = settings["high_S"]
    low_V = settings["low_V"]
    high_V = settings["high_V"]
    count_threshold = settings["count_threshold"]
    morse_time = settings["morse_time"]
    boxes = settings["boxes"]
    prev_led_state = [False for _ in range(len(boxes))]
    prev_box_brightness = [0 for _ in range(len(boxes))]

    cv2.setTrackbarPos(low_H_name, window_settings_name, low_H)
    cv2.setTrackbarPos(high_H_name, window_settings_name, high_H)
    cv2.setTrackbarPos(low_S_name, window_settings_name, low_S)
    cv2.setTrackbarPos(high_S_name, window_settings_name, high_S)
    cv2.setTrackbarPos(low_V_name, window_settings_name, low_V)
    cv2.setTrackbarPos(high_V_name, window_settings_name, high_V)
    cv2.setTrackbarPos(high_F_name, window_settings_name, high_F)
    cv2.setTrackbarPos("Threshold", window_settings_name, count_threshold)
    cv2.setTrackbarPos("Hue", window_settings_name, cam_hue)
    cv2.setTrackbarPos("Gain", window_settings_name, cam_gain)
    cv2.setTrackbarPos("Saturation", window_settings_name, cam_saturation)
    cv2.setTrackbarPos("Morse Time", window_settings_name, morse_time)
    cv2.resizeWindow(window_settings_name, 500, 500)

def detect_led_on_off(frame, click_x, click_y):
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # frame_HSV = frame_HSV[180:200, 180:200]
    frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    frame_threshold = cv2.erode(frame_threshold, None, iterations=2)
    masked = np.zeros(frame_threshold.shape,np.uint8)
    masked[click_y-box_size:click_y+box_size,click_x-box_size:click_x+box_size] = frame_threshold[click_y-box_size:click_y+box_size,click_x-box_size:click_x+box_size]
    frame_threshold = masked
    on_off = cv2.countNonZero(frame_threshold) > count_threshold
    if on_off:
        box_colour = (0, 0, 255)
    else:
        box_colour = (255, 0, 0)

    frame = cv2.rectangle(frame, (click_x-box_size, click_y-box_size), (click_x+box_size, click_y+box_size), box_colour, thickness=1)
    return on_off, frame_threshold

def get_box_frame_brightness(frame, x,y):
    """ This returns the overall brightness summed over the box """
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_HSV = frame_HSV[y-box_size:y+box_size,x-box_size:x+box_size]
    return np.sum(frame_HSV[:,:,2])

def detect_led_on_off_based_on_brightness(frame, click_x, click_y, prev_lightness):
    b = get_box_frame_brightness(frame, click_x, click_y)
    if b - prev_lightness > count_threshold:
        on_off = True
    else:
        on_off = False
    # on_off = cv2.countNonZero(frame_threshold) > count_threshold
    if on_off:
        box_colour = (0, 0, 255)
    else:
        box_colour = (255, 0, 0)

    frame = cv2.rectangle(frame, (click_x-box_size, click_y-box_size), (click_x+box_size, click_y+box_size), box_colour, thickness=1)
    return on_off, prev_lightness

def clahe_frame(img):
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8,8))

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels

    l2 = clahe.apply(l)  # apply CLAHE to the L-channel

    lab = cv2.merge((l2,a,b))  # merge channels
    img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
    return img2

def get_blobs_in_frame(frame):
    """ This finds blobs in the frame and returns an image with the blobs draw on and a list of keypoints. """
    #https://learnopencv2.com/blob-detection-using-opencv-python-c/
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 1
    params.maxThreshold = 50

    # # Filter by Area.
    # params.filterByArea = True
    # params.minArea = 1500

    # # Filter by Circularity
    # params.filterByCircularity = True
    # params.minCircularity = 0.1

    # # Filter by Convexity
    # params.filterByConvexity = True
    # params.minConvexity = 0.87

    # # Filter by Inertia
    # params.filterByInertia = True
    # params.minInertiaRatio = 0.01

    detector = cv2.SimpleBlobDetector_create(params)
    # Convert the frame to greyscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Invert the image
    frame = cv2.bitwise_not(frame)

    # Detect blobs.
    keypoints = detector.detect(frame)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    for point in keypoints:
        print(point.pt)

    return im_with_keypoints, keypoints

on_off = False
start_time = time.time()*1000
last_transition_time = start_time
letter = []
fps_measure = start_time

fps_print_deadline = time.monotonic() + 1
print("Starting main loop")
prev_frame = None

with open("logfile.log", "a+") as logfile:
    while True:
        _, frame = cap.read()
        if frame is None:
            print("Frame is none :(")
            break
        # frame = clahe_frame(frame)
        # cv2.imshow("blobs", blobframe)
        # frame = cv2.convertTo(frame, -1, 2, 1)
        frame = cv2.convertScaleAbs(frame, alpha=2, beta=0)
        # blobframe, blobs = get_blobs_in_frame(frame)
        frame_time = time.time()*1000 - start_time
        frame_threshold = None
        for i in range(len(boxes)):
            x,y = boxes[i]
            if x == 0 and y == 0:
                continue

            on_off, thresholded = detect_led_on_off(frame, x, y)
            if i == 0:
                frame_threshold = thresholded
            else:
                frame_threshold = cv2.bitwise_or(frame_threshold, thresholded)

            # on_off, prev_box_brightness[i] = detect_led_on_off_based_on_brightness(frame, x, y, prev_box_brightness[i])
            if prev_led_state[i] != on_off:
                prev_led_state[i] = on_off
                log_msg = f"{datetime.datetime.now().isoformat()},{i},{on_off}"
                print(log_msg)
                logfile.write(log_msg+"\n")

        if frame_threshold is not None:
            cv2.imshow(filtered_detection_name, frame_threshold)

        cv2.imshow(window_capture_name, frame)

        key = cv2.waitKey(30)
        if key == ord('q') or key == 27:
            settings = {}
            settings["low_H"] = low_H
            settings["high_H"] = high_H
            settings["low_S"] = low_S
            settings["high_S"] = high_S
            settings["low_V"] = low_V
            settings["high_V"] = high_V
            settings["high_F"] = high_F
            settings["count_threshold"] = count_threshold
            settings["hue"] = cam_hue
            settings["gain"] = cam_gain
            settings["saturation"] = cam_saturation
            settings["morse_time"] = morse_time
            settings["boxes"] = boxes
            with open("settings_watcher.toml", "w") as f:
                toml.dump(settings, f)
            break

cv2.destroyAllWindows()
print("Quitting")
for _ in range(5):
    cv2.waitKey(1)

# Bloody windows. I swear.
os.kill (os.getpid (), signal.SIGTERM)