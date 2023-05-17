# This watches a number of blinking LEDs and prints out the rough timing of the blinks.
# This is to measure how long blinkers continue to blink for.

from __future__ import print_function
import time
from itertools import count
import cv2 as cv
import argparse
import toml
import numpy as np
import datetime

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
    cv.setTrackbarPos(low_H_name, window_settings_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_settings_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_settings_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_settings_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_settings_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_settings_name, high_V)
def on_F_trackbar(val):
    global high_F
    high_F = val
    cap.set(cv.CAP_PROP_FOCUS, high_F)
def on_count_trackbar(val):
    global count_threshold
    count_threshold = val
def on_hue_trackbar(val):
    global cam_hue
    cam_hue = val
    cap.set(cv.CAP_PROP_HUE, cam_hue)
def on_gain_trackbar(val):
    global cam_gain
    cam_gain = val
    cap.set(cv.CAP_PROP_GAIN, cam_gain)
def on_saturation_trackbar(val):
    global cam_saturation
    cam_saturation = val
    cap.set(cv.CAP_PROP_SATURATION, cam_saturation)
def on_morse_time_trackbar(val):
    global morse_time
    morse_time = val
def on_click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        global click_x
        global click_y
        click_x = x
        click_y = y
        global boxes
        boxes.append((x, y))
        global prev_led_state
        prev_led_state.append(False)

parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera device number.', default=1, type=int)
args = parser.parse_args()
# cap = cv.VideoCapture(args.camera, cv.CAP_DSHOW)
cap = cv.VideoCapture(args.camera)

cv.namedWindow(window_capture_name)
cv.namedWindow(window_settings_name)
cv.setMouseCallback(window_capture_name, on_click)
cv.createTrackbar(low_H_name, window_settings_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_settings_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_settings_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_settings_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_settings_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_settings_name , high_V, max_value, on_high_V_thresh_trackbar)
cv.createTrackbar(high_F_name, window_settings_name , high_F, max_value, on_F_trackbar)
cv.createTrackbar("Threshold", window_settings_name , count_threshold, 1024, on_count_trackbar)
cv.createTrackbar("Hue", window_settings_name , cam_hue, 255, on_hue_trackbar)
cv.createTrackbar("Gain", window_settings_name , cam_gain, 255, on_gain_trackbar)
cv.createTrackbar("Saturation", window_settings_name , cam_saturation, 255, on_saturation_trackbar)
cv.createTrackbar("Morse Time", window_settings_name , morse_time, 1000, on_morse_time_trackbar)
cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv.CAP_DSHOW, 1)
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
cap.set(cv.CAP_PROP_FRAME_HEIGHT , 240)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv.CAP_PROP_FPS, 60)
# CAP_PROP_SATURATION
with open("settings_watcher.toml", "r") as f:
    settings = toml.load(f)
    cam_hue = settings["hue"]
    cam_gain = settings["gain"]
    cam_saturation = settings["saturation"]
    high_F = settings["high_F"]

    cap.set(cv.CAP_PROP_FOCUS, high_F)
    cap.set(cv.CAP_PROP_SATURATION, cam_saturation)
    cap.set(cv.CAP_PROP_GAIN, cam_gain)
    cap.set(cv.CAP_PROP_HUE, cam_hue)

    low_H = settings["low_H"]
    high_H = settings["high_H"]
    low_S = settings["low_S"]
    high_S = settings["high_S"]
    low_V = settings["low_V"]
    high_V = settings["high_V"]
    count_threshold = settings["count_threshold"]
    morse_time = settings["morse_time"]
    boxes = settings["boxes"]
    prev_led_state = [False for i in range(len(boxes))]

    cv.setTrackbarPos(low_H_name, window_settings_name, low_H)
    cv.setTrackbarPos(high_H_name, window_settings_name, high_H)
    cv.setTrackbarPos(low_S_name, window_settings_name, low_S)
    cv.setTrackbarPos(high_S_name, window_settings_name, high_S)
    cv.setTrackbarPos(low_V_name, window_settings_name, low_V)
    cv.setTrackbarPos(high_V_name, window_settings_name, high_V)
    cv.setTrackbarPos(high_F_name, window_settings_name, high_F)
    cv.setTrackbarPos("Threshold", window_settings_name, count_threshold)
    cv.setTrackbarPos("Hue", window_settings_name, cam_hue)
    cv.setTrackbarPos("Gain", window_settings_name, cam_gain)
    cv.setTrackbarPos("Saturation", window_settings_name, cam_saturation)
    cv.setTrackbarPos("Morse Time", window_settings_name, morse_time)
    cv.resizeWindow(window_settings_name, 500, 500)

def detect_led_on_off(frame, click_x, click_y):
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # frame_HSV = frame_HSV[180:200, 180:200]
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    frame_threshold = cv.erode(frame_threshold, None, iterations=2)
    masked = np.zeros(frame_threshold.shape,np.uint8)
    masked[click_y-box_size:click_y+box_size,click_x-box_size:click_x+box_size] = frame_threshold[click_y-box_size:click_y+box_size,click_x-box_size:click_x+box_size]
    frame_threshold = masked
    on_off = cv.countNonZero(frame_threshold) > count_threshold
    if on_off:
        box_colour = (0, 0, 255)
    else:
        box_colour = (255, 0, 0)

    frame = cv.rectangle(frame, (click_x-box_size, click_y-box_size), (click_x+box_size, click_y+box_size), box_colour, thickness=1)
    return on_off, frame_threshold

on_off = False
start_time = time.time()*1000
last_transition_time = start_time
letter = []
fps_measure = start_time

fps_print_deadline = time.monotonic() + 1
print("Starting main loop")
while True:
    ret, frame = cap.read()
    if frame is None:
        print("Frame is none :(")
        break
    frame_time = time.time()*1000 - start_time
    frame_threshold = None
    with open("logfile.log", "a+") as logfile:
        for i in range(len(boxes)):
            x,y = boxes[i]
            on_off, thresholded = detect_led_on_off(frame, x, y)
            if i == 0:
                frame_threshold = thresholded
            else:
                frame_threshold = cv.bitwise_or(frame_threshold, thresholded)
            if prev_led_state[i] != on_off:
                prev_led_state[i] = on_off
                log_msg = f"{datetime.datetime.now().isoformat()},{i},{on_off}"
                print(log_msg)
                logfile.write(log_msg+"\n")
        cv.imshow(window_capture_name, frame)
        # cv.imshow(window_detection_name, frame_threshold)
        if frame_threshold is not None:
            cv.imshow(filtered_detection_name, frame_threshold)

        key = cv.waitKey(30)
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
