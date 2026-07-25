import cv2
import mediapipe as mp
import pyautogui
import math
from collections import deque
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)
screen_w, screen_h = pyautogui.size()
history_len = 5
x_history, y_history = deque(maxlen=history_len), deque(maxlen=history_len)
left_click_active = False
right_click_active = False
cap = cv2.VideoCapture(0)
while True:
    success, frame = cap.read()
    if not success:
        continue
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    action_color = (255, 255, 255) 
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, _ = frame.shape
            lm = hand_landmarks.landmark
            index_x, index_y = int(lm[8].x * w), int(lm[8].y * h)    
            thumb_x, thumb_y = int(lm[4].x * w), int(lm[4].y * h)    
            middle_x, middle_y = int(lm[12].x * w), int(lm[12].y * h) 
            target_x = int(lm[8].x * screen_w)
            target_y = int(lm[8].y * screen_h)
            x_history.append(target_x)
            y_history.append(target_y)
            smooth_x = int(sum(x_history) / len(x_history))
            smooth_y = int(sum(y_history) / len(y_history))
            pyautogui.moveTo(smooth_x, smooth_y)
            dist_index_thumb = math.hypot(index_x - thumb_x, index_y - thumb_y)
            dist_middle_thumb = math.hypot(middle_x - thumb_x, middle_y - thumb_y)
            if dist_index_thumb < 35: 
                if not left_click_active:
                    pyautogui.click()
                    left_click_active = True
                action_color = (0, 255, 0) 
            else:
                left_click_active = False
            if dist_middle_thumb < 35:
                if not right_click_active:
                    pyautogui.click(button="right")
                    right_click_active = True
                action_color = (0, 0, 255) 
            else:
                right_click_active = False
            if dist_middle_thumb < 40:
                if middle_y < thumb_y - 20:  
                    pyautogui.scroll(50)
                    action_color = (255, 0, 0)  
                elif middle_y > thumb_y + 20:
                    pyautogui.scroll(-50)
                    action_color = (255, 0, 0)
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=action_color, thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=action_color, thickness=2, circle_radius=3)
            )
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 255), -1) 
            cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 255), -1)  
            cv2.circle(frame, (middle_x, middle_y), 10, (0, 165, 255), -1) 
    cv2.imshow("Finger Tracking Mouse", frame)
    if cv2.waitKey(1) & 0xFF == 27: 
        break
cap.release()
cv2.destroyAllWindows()
