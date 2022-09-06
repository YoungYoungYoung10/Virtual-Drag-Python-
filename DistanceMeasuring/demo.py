"""  """"""
Author: Young
2022-7-6
"""

#import
import cv2 
import numpy as np
import math

#mediapipe JUSTIFICATION
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

#camera
cap = cv2.VideoCapture(0)

#
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))


#
square_x = 100
square_y = 100
square_width = 100

L1 = 0
L2 = 0
is_activate = False

while True:
    #
    ret,frame = cap.read()

    #
    frame = cv2.flip(frame,1)

    #mediapipe
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    frame.flags.writeable = False
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame)

    # Draw the hand annotations on the image.
    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    #hands detected?
    if results.multi_hand_landmarks:
        #
        #
        #MAX_NUM_HANDS
      for hand_landmarks in results.multi_hand_landmarks:
        #loop through 21 points 
        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

        # print(hand_landmarks)
        #hand_landmarks
        
        #Create lists for 21 points
        x_list = []
        y_list = []
        for landmark in hand_landmarks.landmark:
            # print(landmark)
            # print(landmark.x)
            #append to x
            x_list.append(landmark.x)
            #append to y
            y_list.append(landmark.y)
        # print(len(x_list))

        #get coordinate for index finger: index is 8
        index_finger_x = int(x_list[8] * width)
        index_finger_y = int(y_list[8] * height)
        # print(index_finger_x,index_finger_y) #float


        #middle_finger 
        middle_finger_x = int(x_list[12] * width) 
        middle_finger_y = int(y_list[12] * height)

        # the P theorem
        finger_len = math.hypot((index_finger_x - middle_finger_x),(index_finger_y - middle_finger_y))
        # print(finger_len)


        # distance less than 30？
        if finger_len < 30 :



        # draw circle to test if we get the coordinates or no 
        # cv2.circle(frame,(index_finger_x,index_finger_y),20,(255,0,255),-1)
        # print(index_finger_x,index_finger_y)

        #If index_finger on squrare?
            if (index_finger_x > square_x) and (index_finger_x < (square_x + square_width)) and (index_finger_y > square_y) and (index_finger_y < (square_y + square_width)):
                # print('on')
                if is_activate == False:
                  L1 = abs(index_finger_x - square_x)
                  L2 = abs(index_finger_y - square_y)
                  is_activate = True
            else:
                  # print('not on')
                  pass
                  #
        else:
            # deactivate
            is_activate = False

        if is_activate:
            # square_x = index_finger_x
            # square_y = index_finger_y
            square_x = index_finger_x - L1
            square_y = index_finger_y - L2






    # draw a square 
    # cv2.rectangle(frame,(square_x,square_y),(square_x + square_width,square_y + square_width),(255,0,0),-1)
    # draw a transparent square
    overlay = frame.copy()
    cv2.rectangle(frame,(square_x,square_y),(square_x + square_width,square_y + square_width),(0,255,0),-1)
    frame = cv2.addWeighted(overlay,0.5,frame,0.5,0)

    #show
    cv2.imshow('Virtual drag',frame)
    #quit
    if cv2.waitKey(10) & 0XFF == 27:
        break
    
cap.release()
cv2.destroyAllWindows()