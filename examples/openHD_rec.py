# -*- coding: utf-8 -*-
"""
    receives the openHD video stream and stores a jpg
    every second.
    receives the mavlink stream and writes the current to position
    to a csv file.

    tested python version: 3.8
"""

__author__ = "Juri Bieler"
__email__ = "juri.bieler@diaven.com"
__status__ = "Development"

import time
import datetime
import os
import threading
import cv2
import pymavlink.mavutil as mavutil

FRAME_RATE = 1

try:
    os.mkdir("log")
except:
    pass
try:
    os.mkdir("img")
except:
    pass

def mav_thread():
    mav1 = mavutil.mavlink_connection(
        'udp::5004', dialect="ardupilotmega", autoreconnect=True)
    print("wait for HB")
    mav1.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" %
      (mav1.target_system, mav1.target_component))
    f = open(datetime.datetime.now().strftime("log/%Y-%m-%d_%H-%M-%S.csv"), "w")
    f.write("ts,lat,lon,alt,alt_rel,hdg\n")
    while True:
        # https://mavlink.io/en/messages/common.html#GLOBAL_POSITION_INT
        msg = mav1.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        f.write("{:.3f},{:.7f},{:.7f},{:.3f},{:.3f},{:.1f}\n".format(
                time.time(),
                msg.lat*10e-8,
                msg.lon*10e-8,
                msg.alt*10e-4,
                msg.relative_alt*10e-4,
                msg.hdg*10e-3))
        f.flush()
        print("got pos")
    mav1.close()

x = threading.Thread(target=mav_thread, name="mav_rec")
x.setDaemon(True)
x.start()

cap = cv2.VideoCapture("udpsrc port=5600 ! h264parse ! decodebin ! videoconvert ! appsink", cv2.CAP_GSTREAMER)
last_frame_ts = 0
while True:
    ret,frame = cap.read()
    if(time.time() - last_frame_ts >= FRAME_RATE):
        last_frame_ts = time.time()
        if not ret:
            print("no frame")
            time.sleep(1)
            continue
        print("got frame")
        cv2.imwrite('img/{:.1f}.jpg'.format(time.time()), frame)
cv2.destroyAllWindows()
cap.release()
