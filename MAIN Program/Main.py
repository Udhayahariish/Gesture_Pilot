import cv2
import time
import math
import numpy as np
import mediapipe as mp
import pyautogui
import platform

CAM_INDEX = 0
WCAM, HCAM = 640, 480
FRAME_R = 70
SMOOTHENING = 5.0
MODEL_COMPLEXITY = 0
DETECTION_CONF = 0.72
TRACKING_CONF = 0.72
MAX_NUM_HANDS = 1

TI_PINCH_RATIO = 0.27
TM_PINCH_RATIO = 0.27
IM_PINCH_RATIO = 0.24
RELEASE_RATIO = 0.38
THUMB_AWAY_RATIO = 0.44

CLICK_MIN_TIME = 0.03
CLICK_MAX_TIME = 0.30
CLICK_STABLE_FRAMES = 4
CLICK_MOVE_RATIO = 0.18
CLICK_COOLDOWN = 0.28
POST_CLICK_FREEZE = 0.12

SCROLL_START_DELAY = 0.04
SCROLL_DEADZONE = 1.5
SCROLL_GAIN = 1.8
SCROLL_SMOOTH = 0.68

SHOW_DEBUG_TEXT = True

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
SCREEN_W, SCREEN_H = pyautogui.size()

IS_WINDOWS = platform.system().lower() == "windows"
if IS_WINDOWS:
    import ctypes
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010

def os_click(button, x, y):
    x = int(max(0, min(x, SCREEN_W - 1)))
    y = int(max(0, min(y, SCREEN_H - 1)))
    if IS_WINDOWS:
        ctypes.windll.user32.SetCursorPos(x, y)
        if button == "left":
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.012)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        else:
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            time.sleep(0.012)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    else:
        pyautogui.mouseDown(x=x, y=y, button=button)
        time.sleep(0.012)
        pyautogui.mouseUp(x=x, y=y, button=button)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=MAX_NUM_HANDS,
    model_complexity=MODEL_COMPLEXITY,
    min_detection_confidence=DETECTION_CONF,
    min_tracking_confidence=TRACKING_CONF,
)

backend = cv2.CAP_DSHOW if IS_WINDOWS else 0
cap = cv2.VideoCapture(CAM_INDEX, backend)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WCAM)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HCAM)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

prev_x, prev_y = SCREEN_W / 2, SCREEN_H / 2
cur_x, cur_y = prev_x, prev_y

last_left_click = 0
last_right_click = 0
freeze_until = 0

left_active = False
left_start_time = 0
left_frames = 0
left_start_mid = None
left_scale = 1.0
left_fired = False

right_active = False
right_start_time = 0
right_frames = 0
right_start_mid = None
right_scale = 1.0
right_fired = False

scroll_active = False
scroll_start_time = 0
scroll_last_y = 0
scroll_velocity = 0

effects = []
prev_time = 0

def lm_px(hand_landmarks, idx, w, h):
    lm = hand_landmarks.landmark[idx]
    return np.array([int(lm.x * w), int(lm.y * h)], dtype=np.float32)

def dist(p1, p2):
    return float(np.linalg.norm(p2 - p1))

def clamp(v, lo, hi):
    return max(lo, min(v, hi))

def interp_screen(x, y, w, h):
    sx = np.interp(x, (FRAME_R, w - FRAME_R), (0, SCREEN_W))
    sy = np.interp(y, (FRAME_R, h - FRAME_R), (0, SCREEN_H))
    return clamp(sx, 0, SCREEN_W - 1), clamp(sy, 0, SCREEN_H - 1)

def hand_scale(points):
    return max(dist(points[5], points[17]), 1.0)

def add_effect(x, y, label, color):
    effects.append({"x": int(x), "y": int(y), "start": time.time(), "label": label, "color": color})

def draw_effects(img, now):
    if not effects:
        return
    overlay = img.copy()
    kept = []
    for e in effects:
        age = now - e["start"]
        duration = 0.35
        if age <= duration:
            t = age / duration
            radius = int(12 + 55 * t)
            thickness = max(1, int(5 * (1 - t)))
            cv2.circle(overlay, (e["x"], e["y"]), radius, e["color"], thickness)
            cv2.circle(overlay, (e["x"], e["y"]), 8, e["color"], cv2.FILLED)
            cv2.putText(overlay, e["label"], (e["x"] - 12, e["y"] - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, e["color"], 2)
            kept.append(e)
    cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)
    effects[:] = kept

while True:
    ok, img = cap.read()
    if not ok:
        break

    now = time.time()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    cv2.rectangle(img, (FRAME_R, FRAME_R), (w - FRAME_R, h - FRAME_R), (255, 0, 255), 2)

    gesture_text = "Move"

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        pts = {}
        for idx in [4, 5, 8, 12, 17]:
            pts[idx] = lm_px(hand_landmarks, idx, w, h)

        thumb_tip = pts[4]
        index_tip = pts[8]
        middle_tip = pts[12]

        scale = hand_scale(pts)

        ti_ratio = dist(thumb_tip, index_tip) / scale
        tm_ratio = dist(thumb_tip, middle_tip) / scale
        im_ratio = dist(index_tip, middle_tip) / scale

        scroll_condition = im_ratio < IM_PINCH_RATIO and ti_ratio > THUMB_AWAY_RATIO and tm_ratio > THUMB_AWAY_RATIO
        left_condition = ti_ratio < TI_PINCH_RATIO and tm_ratio > THUMB_AWAY_RATIO and im_ratio > IM_PINCH_RATIO
        right_condition = tm_ratio < TM_PINCH_RATIO and ti_ratio > THUMB_AWAY_RATIO and im_ratio > IM_PINCH_RATIO

        if scroll_condition:
            left_active = False
            right_active = False
            left_fired = False
            right_fired = False

            mid_y = (index_tip[1] + middle_tip[1]) * 0.5
            cv2.circle(img, tuple(index_tip.astype(int)), 10, (0, 255, 255), cv2.FILLED)
            cv2.circle(img, tuple(middle_tip.astype(int)), 10, (0, 255, 255), cv2.FILLED)

            if not scroll_active:
                scroll_active = True
                scroll_start_time = now
                scroll_last_y = mid_y
                scroll_velocity = 0
            else:
                if now - scroll_start_time > SCROLL_START_DELAY:
                    dy = scroll_last_y - mid_y
                    if abs(dy) > SCROLL_DEADZONE:
                        scroll_velocity = scroll_velocity * SCROLL_SMOOTH + dy * (1 - SCROLL_SMOOTH)
                        amount = int(scroll_velocity * SCROLL_GAIN)
                        if amount != 0:
                            pyautogui.scroll(amount)
                    scroll_last_y = mid_y
            gesture_text = "Scroll"
        else:
            scroll_active = False
            scroll_velocity = 0

            freeze_cursor = now < freeze_until or left_active or right_active

            if not freeze_cursor:
                target_x, target_y = interp_screen(index_tip[0], index_tip[1], w, h)
                move_dist = math.hypot(target_x - prev_x, target_y - prev_y)
                dynamic_smooth = max(2.8, min(SMOOTHENING, SMOOTHENING - move_dist / 300.0))
                cur_x = prev_x + (target_x - prev_x) / dynamic_smooth
                cur_y = prev_y + (target_y - prev_y) / dynamic_smooth
                cur_x = clamp(cur_x, 0, SCREEN_W - 1)
                cur_y = clamp(cur_y, 0, SCREEN_H - 1)
                pyautogui.moveTo(int(cur_x), int(cur_y))
                prev_x, prev_y = cur_x, cur_y

            cv2.circle(img, tuple(index_tip.astype(int)), 10, (0, 255, 0), cv2.FILLED)

            if left_condition and now - last_left_click > CLICK_COOLDOWN:
                mid = (thumb_tip + index_tip) / 2.0
                if not left_active:
                    left_active = True
                    left_start_time = now
                    left_frames = 1
                    left_start_mid = mid.copy()
                    left_scale = scale
                    left_fired = False
                else:
                    left_frames += 1

                duration = now - left_start_time
                move_ok = dist(mid, left_start_mid) <= left_scale * CLICK_MOVE_RATIO
                time_ok = CLICK_MIN_TIME <= duration <= CLICK_MAX_TIME
                frame_ok = left_frames >= CLICK_STABLE_FRAMES

                if not left_fired and move_ok and time_ok and frame_ok:
                    os_click("left", cur_x, cur_y)
                    last_left_click = now
                    freeze_until = now + POST_CLICK_FREEZE
                    left_fired = True
                    add_effect(mid[0], mid[1], "L", (0, 255, 0))
                    gesture_text = "Left Click"
                else:
                    gesture_text = "Left Tap"
            else:
                if left_active and (ti_ratio > RELEASE_RATIO or now - left_start_time > CLICK_MAX_TIME):
                    left_active = False
                    left_fired = False
                    left_frames = 0

            if right_condition and now - last_right_click > CLICK_COOLDOWN:
                mid = (thumb_tip + middle_tip) / 2.0
                if not right_active:
                    right_active = True
                    right_start_time = now
                    right_frames = 1
                    right_start_mid = mid.copy()
                    right_scale = scale
                    right_fired = False
                else:
                    right_frames += 1

                duration = now - right_start_time
                move_ok = dist(mid, right_start_mid) <= right_scale * CLICK_MOVE_RATIO
                time_ok = CLICK_MIN_TIME <= duration <= CLICK_MAX_TIME
                frame_ok = right_frames >= CLICK_STABLE_FRAMES

                if not right_fired and move_ok and time_ok and frame_ok:
                    os_click("right", cur_x, cur_y)
                    last_right_click = now
                    freeze_until = now + POST_CLICK_FREEZE
                    right_fired = True
                    add_effect(mid[0], mid[1], "R", (0, 165, 255))
                    gesture_text = "Right Click"
                else:
                    gesture_text = "Right Tap"
            else:
                if right_active and (tm_ratio > RELEASE_RATIO or now - right_start_time > CLICK_MAX_TIME):
                    right_active = False
                    right_fired = False
                    right_frames = 0

        cv2.line(img, tuple(thumb_tip.astype(int)), tuple(index_tip.astype(int)), (0, 255, 0) if left_condition else (0, 0, 255), 2)
        cv2.line(img, tuple(thumb_tip.astype(int)), tuple(middle_tip.astype(int)), (0, 165, 255) if right_condition else (255, 200, 0), 2)
        cv2.line(img, tuple(index_tip.astype(int)), tuple(middle_tip.astype(int)), (0, 255, 255), 2)

        if SHOW_DEBUG_TEXT:
            cv2.putText(img, f"Gesture: {gesture_text}", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 255, 50), 2)
            cv2.putText(img, f"TI:{ti_ratio:.2f} TM:{tm_ratio:.2f} IM:{im_ratio:.2f}", (10, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    draw_effects(img, now)

    cur_time = time.time()
    fps = 1 / (cur_time - prev_time) if prev_time else 0
    prev_time = cur_time

    cv2.putText(img, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow("Hand Mouse Control", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
