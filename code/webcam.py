from __future__ import print_function
import time
from itertools import count
import cv2 as cv
import argparse
import toml
import numpy as np

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

parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera device number.', default=1, type=int)
args = parser.parse_args()
cap = cv.VideoCapture(args.camera, cv.CAP_DSHOW)

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
dit = "dit"
dah = "dah"
morse = {
    'a': [dit, dah],
    'b': [dah, dit, dit, dit],
    'c': [dah, dit, dah, dit],
    'd': [dah, dit, dit],
    'e': [dit],
    'f': [dit, dit, dah, dit],
    'g': [dah, dah, dit],
    'h': [dit, dit, dit, dit],
    'i': [dit, dit],
    'j': [dit, dah, dah, dah],
    'k': [dah, dit, dah],
    'l': [dit, dah, dit, dit],
    'm': [dah, dah],
    'n': [dah, dit],
    'o': [dah, dah, dah],
    'p': [dit, dah, dah, dit],
    'q': [dah, dah, dit, dah],
    'r': [dit, dah, dit],
    's': [dit, dit, dit],
    't': [dah],
    'u': [dit, dit, dah],
    'v': [dit, dit, dit, dah],
    'w': [dit, dah, dah],
    'x': [dah, dit, dit, dah],
    'y': [dah, dit, dah, dah],
    'z': [dah, dah, dit, dit],
    '1': [dit, dah, dah, dah, dah],
    '2': [dit, dit, dah, dah, dah],
    '3': [dit, dit, dit, dah, dah],
    '4': [dit, dit, dit, dit, dah],
    '5': [dit, dit, dit, dit, dit],
    '6': [dah, dit, dit, dit, dit],
    '7': [dah, dah, dit, dit, dit],
    '8': [dah, dah, dah, dit, dit],
    '9': [dah, dah, dah, dah, dit],
    '0': [dah, dah, dah, dah, dah],
    # Fun story: I'm using copilot to write this, and it started filling out 0-9 by itself
    # so I let it run with it. It then started doing the below which I'm reasonably
    # sure it invented from whole cloth.
    # '.': [dit, dah, dah, dah, dah, dah],
    # ',': [dah, dah, dah, dah, dah, dit],
    # '?': [dit, dit, dah, dah, dit, dit],
    # '\'': [dit, dit, dah, dah, dah, dah],
    # '!': [dit, dit, dah, dah, dah, dah, dah],
    # '/': [dah, dit, dit, dah, dah],
    # '(': [dah, dit, dah, dit, dah],
    # ')': [dah, dit, dah, dit, dah, dah],
    # '&': [dit, dit, dah, dit, dah, dit],
    # ':': [dah, dah, dah, dah, dah, dah, dah],
    # ';': [dah, dah, dah, dah, dah, dah, dit],
    # '=': [dah, dah, dah, dah, dah, dah, dah, dah],
    # '+': [dah, dah, dah, dah, dah, dah, dah, dah, dah],
    # '-': [dah, dah, dah, dah, dah, dah, dah, dah, dah, dah],
    # '_': [dah, dah, dah, dah, dah, dah, dah, dah, dah, dah, dah],
    # '"': [dit, dit, dah, dah, dah, dah, dah, dah, dah, dah, dah],
    # '$': [dah, dit, dah, dah, dah, dah, dah, dah, dah, dit, dah],
    # '@': [dah, dit, dah, dah, dah, dah, dah, dah, dah, dah, dah, dah],
}
# CAP_PROP_SATURATION
with open("settings.toml", "r") as f:
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
on_off = False
start_time = time.time()*1000
last_transition_time = start_time
letter = []
fps_measure = start_time

# while True:
#     ret, frame = cap.read()
#     print("FPS: {}".format(1/(time.time()-fps_measure)))
#     fps_measure = time.time()
#     frame_threshold = frame
#     cv.imshow(window_capture_name, frame)
#     cv.imshow(window_detection_name, frame_threshold)
fps_print_deadline = time.monotonic() + 1
while True:
    ret, frame = cap.read()
    # if time.monotonic() > fps_print_deadline:
    #     print("FPS: {}".format(1/(time.time()-fps_measure)))
    #     fps_print_deadline = time.monotonic() + 1
    # fps_measure = time.time()
    if frame is None:
        break
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # frame_HSV = frame_HSV[180:200, 180:200]
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    frame_threshold = cv.erode(frame_threshold, None, iterations=2)
    masked = np.zeros(frame_threshold.shape,np.uint8)
    masked[click_y-box_size:click_y+box_size,click_x-box_size:click_x+box_size] = frame_threshold[click_y-box_size:click_y+box_size,click_x-box_size:click_x+box_size]
    frame_threshold = masked
    frame = cv.rectangle(frame, (click_x-box_size, click_y-box_size), (click_x+box_size, click_y+box_size), (255, 0, 255), thickness=1)

    # print(cv.countNonZero(frame_threshold))

    frame_time = time.time()*1000 - start_time

    if cv.countNonZero(frame_threshold) > count_threshold:
        if not on_off:
            on_off = True
            # print("{}, off".format(frame_time-last_transition_time))
            off_time = frame_time-last_transition_time
            if off_time < 2*morse_time:
                pass
                # print(" ", end="")
                # letter += " "
            elif off_time > 2*morse_time:
                for k,v in morse.items():
                    if letter == v:
                        print(k, end="")
                        break
                else:
                    print("?", end="")
                letter = []
                if off_time > 4*morse_time:
                    print("")


            # print("{}, on".format(frame_time))
            last_transition_time = frame_time
    else:
        if on_off:
            on_off = False
            # print("{}, on".format(frame_time-last_transition_time))
            on_time = frame_time-last_transition_time
            if on_time < 2*morse_time:
                # print("dit", end = "")
                letter += ["dit"]
            else:
                # print("dah", end = "")
                letter += ["dah"]
            last_transition_time = frame_time
            # print("{}, off".format(frame_time))

    cv.imshow(window_capture_name, frame)
    # cv.imshow(window_detection_name, frame_threshold)
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
        with open("settings.toml", "w") as f:
            toml.dump(settings, f)
        break

# Logs from testing:
'''
    e
posuere
sagittis
nam
tincidunt
vel
nulla
eu
tempor
abcdef
qwerty
ahdfg
zxcvb
lorem
ipsum
dolor
sit
amet
consectetur
adipiscing
elit
donec
faucibus
orci
quis
iaculis
volutpat
lacus
mi
sollicitudin
sem
at
dignissim
turpis
arcu
nec
est
fusce
elementum
vitae
risus
non
aliquam
proin
finibus
arcu
ullamcorper
scelerisque
orci
egestas
varius
mi
nulla
bibendum
eros
sit
amet
leo
pellentesque
lobortis
curabitur
a
gravida
mauris
ac
tincidunt
ex
phasellus
sagittis
congue
massa
quis
tincidunt
felis
nunc
et
orci
eget
mi
mollis
viverra
non
in
nunc
nullam
dapibus
pulvinar
lectus
ut
facilisis
neque
vestibulum
at
tellus
id
enim
posuere
sagittis
nam
tincidunt
vel
nulla
eu
tempor
abcdef
qwerty
asdfg
zxcvb
lorem
ipsum
dolor
sit
amet
consectetur
adipiscing
elit
donec
faucibus
orci
quis
iaculis
volutpat
lacus
mi
sollicitudin
sem
at
dignissim
turpis
arcu
nec
est
fusce
elementum
vitae
risus
non
aliquam
proin
finibus
arcu
ullamcorper
scelerisque
orci
egestas
?arius
mi
nulla
bibendum
eros
sit
amet
leo
pellentesque
lobortis
curabitur
a
gravida
mauris
ac
tincidunt
ex
phasellus
sagittis
congue
massa
quis
tincidunt
felis
nunc
et
orci
eget
mi
mollis
viverra
non
in
nunc
nullam
dapibus
pulvinar
lectus
ut
'''