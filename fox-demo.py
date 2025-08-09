import cv2
import mediapipe as mp
import time
import math
import threading
import random
import numpy as np
import os
import pyttsx3
import textwrap

SPRITE_FILE = "sarcastic_sprite.png"   # transparent PNG in same folder
SPRITE_SCALE = 0.35
SPRITE_SHOW_TIME = 1.6
BUBBLE_PADDING = 12
MAX_BUBBLE_CHARS = 30

BLINK_THRESHOLD = 0.23
CLOSED_FRAMES = 2
BLINK_COOLDOWN = 1.2

PHRASES = [
    "Another blink, another semester wasted.",
    "Blink twice if you regret choosing engineering... oh, already did.",
    "Your blinks have more personality than your resume.",
    "Did blinking come with your procrastination package?",
    "That blink was approved by the Ministry of Useless Actions.",
    "New record! World's most unnecessary blink!"
]

sprite_img = None
if os.path.isfile(SPRITE_FILE):
    sprite_img = cv2.imread(SPRITE_FILE, cv2.IMREAD_UNCHANGED)
    if sprite_img is None:
        print(f"Warning: failed to load '{SPRITE_FILE}'. No sprite will be shown.")
else:
    print(f"Warning: '{SPRITE_FILE}' not found. No sprite will be shown.")

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam.")

frame_counter = 0
last_blink_time = 0.0
show_sprite_until = 0.0
total_blinks = 0

bubble_text_lines = []
bubble_until = 0.0

# ==== TTS function runs in a fresh thread for each phrase ====
def speak_phrase(phrase):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.say(phrase)
        engine.runAndWait()
    except Exception as e:
        print("TTS error:", e)

def speak_async(text):
    global bubble_text_lines, bubble_until
    bubble_text_lines = textwrap.wrap(text, width=MAX_BUBBLE_CHARS)
    bubble_duration = max(2.0, len(text) / 12)
    bubble_until = time.time() + bubble_duration
    threading.Thread(target=speak_phrase, args=(text,), daemon=True).start()

def eye_aspect_ratio(landmarks, indices):
    p1 = landmarks[indices[0]]
    p2 = landmarks[indices[1]]
    p3 = landmarks[indices[2]]
    p4 = landmarks[indices[3]]
    p5 = landmarks[indices[4]]
    p6 = landmarks[indices[5]]
    A = math.hypot(p2.x - p6.x, p2.y - p6.y)
    B = math.hypot(p3.x - p5.x, p3.y - p5.y)
    C = math.hypot(p1.x - p4.x, p1.y - p4.y)
    if C == 0:
        return 0.0
    return (A + B) / (2.0 * C)

def overlay_png_onto_bgr(bg_bgr, fg_bgra, x, y):
    fg_h, fg_w = fg_bgra.shape[:2]
    bg_h, bg_w = bg_bgr.shape[:2]
    if x >= bg_w or y >= bg_h:
        return bg_bgr
    w = min(fg_w, bg_w - x)
    h = min(fg_h, bg_h - y)
    if w <= 0 or h <= 0:
        return bg_bgr
    fg = fg_bgra[0:h, 0:w]
    if fg.shape[2] == 4:
        alpha = fg[:, :, 3] / 255.0
        alpha = alpha[..., np.newaxis]
        fg_rgb = fg[:, :, :3].astype(float)
        bg_roi = bg_bgr[y:y+h, x:x+w].astype(float)
        blended = (alpha * fg_rgb) + ((1 - alpha) * bg_roi)
        bg_bgr[y:y+h, x:x+w] = blended.astype(np.uint8)
    else:
        bg_bgr[y:y+h, x:x+w] = fg[:, :, :3]
    return bg_bgr

def draw_speech_bubble(frame, lines, anchor_x, anchor_y):
    if not lines:
        return
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    line_height = cv2.getTextSize("Test", font, font_scale, thickness)[0][1] + 6
    box_w = max(cv2.getTextSize(line, font, font_scale, thickness)[0][0] for line in lines)
    box_h = line_height * len(lines)
    box_x = anchor_x - box_w - BUBBLE_PADDING * 2
    box_y = anchor_y
    cv2.rectangle(frame,
                  (box_x, box_y - box_h - BUBBLE_PADDING * 2),
                  (box_x + box_w + BUBBLE_PADDING * 2, box_y),
                  (255, 255, 255), -1)
    cv2.rectangle(frame,
                  (box_x, box_y - box_h - BUBBLE_PADDING * 2),
                  (box_x + box_w + BUBBLE_PADDING * 2, box_y),
                  (0, 0, 0), 1)
    for i, line in enumerate(lines):
        text_y = box_y - BUBBLE_PADDING - (len(lines) - 1 - i) * line_height
        cv2.putText(frame, line, (box_x + BUBBLE_PADDING, text_y),
                    font, font_scale, (0, 0, 0), thickness)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame_h, frame_w = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        ear = None
        blink_detected = False

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
            right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
            ear = (left_ear + right_ear) / 2.0

            if ear < BLINK_THRESHOLD:
                frame_counter += 1
            else:
                if frame_counter >= CLOSED_FRAMES:
                    now = time.time()
                    if now - last_blink_time > BLINK_COOLDOWN:
                        blink_detected = True
                        last_blink_time = now
                frame_counter = 0

        if blink_detected:
            total_blinks += 1
            phrase = random.choice(PHRASES)
            print(f"[{total_blinks}] {phrase}")
            speak_async(phrase)
            show_sprite_until = time.time() + SPRITE_SHOW_TIME

        cv2.rectangle(frame, (6, 6), (230, 70), (245, 245, 245), -1)
        cv2.putText(frame, f"Blinks: {total_blinks}", (12, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 30, 30), 2)
        if ear is not None:
            cv2.putText(frame, f"EAR: {ear:.3f}", (12, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (30, 30, 30), 2)

        if time.time() < show_sprite_until and sprite_img is not None:
            target_w = int(frame_w * SPRITE_SCALE)
            sh, sw = sprite_img.shape[:2]
            scale = target_w / sw
            target_h = max(1, int(sh * scale))
            resized = cv2.resize(sprite_img, (target_w, target_h), interpolation=cv2.INTER_AREA)
            x = frame_w - target_w - 20
            y = 20
            overlay_png_onto_bgr(frame, resized, x, y)
            if time.time() < bubble_until:
                draw_speech_bubble(frame, bubble_text_lines, x, y + target_h // 2)

        elif time.time() < show_sprite_until and sprite_img is None:
            if time.time() < bubble_until:
                draw_speech_bubble(frame, bubble_text_lines, frame_w - 50, 80)

        cv2.imshow("Sarcastic Blink Detector (press 'q' to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    face_mesh.close()
    cv2.destroyAllWindows()
