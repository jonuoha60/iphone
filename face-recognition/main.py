import os

import threading
import numpy as np
import cv2
from deepface import DeepFace

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

counter = 0
face_match = False

script_dir = os.path.dirname(os.path.abspath(__file__))

reference_img = cv2.imread(os.path.join(script_dir, "asset/reference.jpg"))

if reference_img is None:
    print(f"ERROR: Could not load image from {os.path.join(script_dir, 'asset/reference2.jpg')}")
    exit(1)

def check_face(frame):
    global face_match 
    try:
        result = DeepFace.verify(frame, reference_img)
        face_match = result['verified']
    except ValueError:
        face_match = False



while True:
    ret, frame = capture.read()

    if ret:
        if counter % 30 == 0:
            try:
                thread = threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1

        

        if face_match:
            cv2.putText(frame, "Matched!", (20, 450), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "No match!", (20, 450), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()