import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# initialize hand tracking
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

screenW, screenH = pyautogui.size()

prev_x, prev_y = None, None
# alpha = 0 no smooth, 1 = max smooth
alpha = 0.5
scrolling_down = False

# capture vid stream
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    flip = cv2.flip(frame,1)
    if not ret:
        continue

    # Convert BGR to RGB
    image = cv2.cvtColor(flip, cv2.COLOR_BGR2RGB)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # process image and find hands
    res = hands.process(image)

    if res.multi_hand_landmarks:
        # we only need the 1st hand detected
        hand_landmarks = res.multi_hand_landmarks[0]

        # we get coordinates of the fingers?
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        mid_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        mid_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

        camH, camW, _ = frame.shape
        x, y = int(index_tip.x * camW), int(index_tip.y * camH)
        midTipx, midTipy = int(mid_tip.x * camW), int(mid_tip.y * camH)
        midx, midy = int(mid_dip.x * camW), int(mid_dip.y * camH)
        thx, thy = int(thumb_tip.x * camW), int(thumb_tip.y * camH)

        # display a circle
        cv2.circle(image, (x, y), 10, (127, 0, 255), 3)
        cv2.circle(image, (midTipx, midTipy), 10, (255, 204, 153), 3)
        cv2.circle(image, (midx, midy), 10, (127, 255, 255), 3)
        cv2.circle(image, (thx, thy), 10, (0, 255, 0), 3)

        # use x values of middip and thumbtip if < 20??? then click
        print('midx: ', midx)
        print('thx: ', thx)
        #print(x,y)

        # right click
        if abs(thx - midx) < 30 and abs(thy - midy) < 30:
            print('Left click')
            pyautogui.click()

        # left click
        if abs(thx - midTipx) < 30 and abs(thy - midTipy) < 30:
            print('Right click')
            pyautogui.rightClick()

        # scroll up
        if y <  midy and abs(x - midTipx) < 30 and abs(y - midTipy) < 30:
            pyautogui.scroll(5)

        # scroll down
        if y > midy and abs(x - midTipx) < 30 and abs(y - midTipy) < 30:
            pyautogui.scroll(-5)
            scrolling_down = True

        # set boundaries
        x_ix = int(np.interp(x, (150, camW - 150), (0, screenW*2)))
        y_ix = int(np.interp(y, (150, camH - 150), (0, screenH)))

        # smooth the coordinates so mouse isn't jittery and check if its scrolling down or not
        if not scrolling_down:  # Only smooth if not scrolling down
            x_smooth = alpha * x_ix + (1 - alpha) * prev_x if prev_x is not None else x_ix
            y_smooth = alpha * y_ix + (1 - alpha) * prev_y if prev_y is not None else y_ix
        else:
            x_smooth, y_smooth = prev_x, prev_y  # Keep previous coordinates if scrolling down


        # update prev coords
        prev_x,prev_y = x_smooth, y_smooth

        # move cursor if its not scrolling down
        if not scrolling_down:
            pyautogui.moveTo(int(x_smooth),int(y_smooth))

        # Display box range
        cv2.rectangle(image, (150, 150), (camW - 150, camH - 150), (255, 0, 100), 2)

    cv2.imshow('AI Mouse', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # resets scrolling down status
    if scrolling_down:
        scrolling_down = False

# exit
cap.release()
cv2.destroyAllWindows()