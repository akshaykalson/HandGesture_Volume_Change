import cv2
import mediapipe as mp
import time
import math
import numpy as np

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Set up camera parameters
pTime = 0
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize mediapipe Hands model
mpHands = mp.solutions.hands
hands = mpHands.Hands() 
mpDraw = mp.solutions.drawing_utils

# Variables to store hand landmark positions
x1, y1, x2, y2 = 0, 0, 0, 0


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
#print(minVol, maxVol)


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process hand landmarks
    results = hands.process(imgRGB)

    # Draw landmarks on the image
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 4:
                    x1, y1 = cx, cy
                elif id == 8:
                    x2, y2 = cx, cy
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        length = math.hypot(x2 - x1, y2 - y1)
        #print(length)
        #handlength 50-326
        #volume range -65.25 0

        vol = np.interp(length, [50,326], [minVol, maxVol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)



    # Display the hand landmark positions
    cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
    cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
    cv2.line(img, (x1,y1), (x2,y2), (255,0,0), 5)

    # Calculate and display FPS
    cTime = time.time()
   
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)

    # Display the image
    cv2.imshow("Image", img)

    # Check for 'q' key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
