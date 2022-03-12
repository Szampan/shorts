import cv2
import mediapipe as mp
import time     # to check framerate

cap = cv2.VideoCapture(0)   # webcam number

mpHands = mp.solutions.hands
hands = mpHands.Hands()    # False is a default (tracking/detection based on confidence)
mpDraw = mp.solutions.drawing_utils     # Draws lines, etc


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    # print(results.multi_hand_landmarks)     # see if any hands are detected
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:    # extract the information of each hand
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)     # handLms - single hand

    cv2.imshow("Image", img)

    k = cv2.waitKey(1) & 0xFF
    if k == ord("q"):
        break
