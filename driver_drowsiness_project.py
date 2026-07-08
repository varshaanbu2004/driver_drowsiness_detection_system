import cv2
import mediapipe as mp
import math
from pygame import mixer
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALARM_FILE = os.path.join(BASE_DIR, "alarm.wav")

# ==========================
# ==========================
# ALARM SETUP
# ==========================
mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

mixer.music.load(ALARM_FILE)
# ==========================
# MEDIAPIPE FACE MESH
# ==========================
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ==========================
# LANDMARKS
# ==========================

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

UPPER_LIP = 13
LOWER_LIP = 14

# ==========================
# THRESHOLDS
# ==========================

EAR_THRESHOLD = 0.23
EAR_CONSEC_FRAMES = 20

YAWN_THRESHOLD = 25

# ==========================
# VARIABLES
# ==========================

COUNTER = 0
ALARM_ON = False


# ==========================
# FUNCTIONS
# ==========================

def euclidean(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


def eye_aspect_ratio(eye):
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)

    return ear


# ==========================
# WEBCAM
# ==========================

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    h, w = frame.shape[:2]

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            points = []

            for lm in face_landmarks.landmark:
                x = int(lm.x * w)
                y = int(lm.y * h)
                points.append((x, y))

            # ======================
            # EYE DETECTION
            # ======================

            left_eye = [points[i] for i in LEFT_EYE]
            right_eye = [points[i] for i in RIGHT_EYE]

            leftEAR = eye_aspect_ratio(left_eye)
            rightEAR = eye_aspect_ratio(right_eye)

            ear = (leftEAR + rightEAR) / 2.0

            for p in left_eye:
                cv2.circle(frame, p, 2, (0, 255, 0), -1)

            for p in right_eye:
                cv2.circle(frame, p, 2, (0, 255, 0), -1)

            # ======================
            # DROWSINESS CHECK
            # ======================

            if ear < EAR_THRESHOLD:

                COUNTER += 1

                if COUNTER >= EAR_CONSEC_FRAMES:

                    cv2.putText(
                        frame,
                        "DROWSINESS ALERT!",
                        (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )

                    if not ALARM_ON:
                        mixer.music.load(ALARM_FILE)
                        mixer.music.play(-1)
                        ALARM_ON = True

            else:

                COUNTER = 0

                if ALARM_ON:
                    mixer.music.stop()
                    ALARM_ON = False

            # ======================
            # YAWN DETECTION
            # ======================

            upper_lip = points[UPPER_LIP]
            lower_lip = points[LOWER_LIP]

            mouth_open = abs(
                upper_lip[1] - lower_lip[1]
            )

            cv2.line(
                frame,
                upper_lip,
                lower_lip,
                (255, 0, 0),
                2
            )

            if mouth_open > YAWN_THRESHOLD:

                cv2.putText(
                    frame,
                    "YAWNING DETECTED!",
                    (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    3
                )

            # ======================
            # INFO DISPLAY
            # ======================

            cv2.putText(
                frame,
                f"EAR: {ear:.2f}",
                (20, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Mouth: {mouth_open}",
                (20, 190),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2
            )

    cv2.imshow(
        "Driver Drowsiness Detection System",
        frame
    )

    key = cv2.waitKey(1)

    if key == 27: # ESC key
        break

# ==========================
# CLEANUP
# ==========================

cap.release()
cv2.destroyAllWindows()



