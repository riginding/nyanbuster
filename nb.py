import sys
import os
import time
import face_recognition
import argparse
import pickle
import cv2

fail_count = 0
locked = False

def inFrontOfCamera():
    cam = cv2.VideoCapture(0)
    s, img = cam.read()
    if s:
        cv2.imwrite("screenshot.jpg",img)

    data = pickle.loads(open('encodings.pickle', "rb").read())

    image = cv2.imread('screenshot.jpg')
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb, model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes)

    matches = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(data['encodings'], encoding)

    return any(match for match in matches)


def bust(fail_count, locked):
    if fail_count > 3:
        print("bye")
        fail_count = 0
        os.system("/home/ryan/.i3/i3lock-fancy-multimonitor/lock -n -b='5x3'")
        locked = True

    if inFrontOfCamera():
        print("found")
        if locked:
            os.system("killall i3lock")
            locked = False
    else:
        print("not found")
        fail_count = fail_count + 1
        time.sleep(3.00)
        bust(fail_count, locked)


start_time = time.time()
while True:
    bust(fail_count, locked)
    time.sleep(10.0 - (time.time() - start_time) % 10.0 )
