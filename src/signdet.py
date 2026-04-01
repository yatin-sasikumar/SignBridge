import cv2
import mediapipe as mp
import pickle
import time
from collections import deque
import nlp

# Load model once
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def run_sign_detection(callback=None):

    def update(msg):
        if callback:
            callback(msg)
        else:
            print(msg)

    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands()

    pred_buffer = deque(maxlen=10)

    word_list = []
    last_added_word = ""

    last_detection_time = time.time()
    TIMEOUT = 3  # seconds

    update("Show gestures...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        prediction = ""

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:

                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                data = []
                for lm in hand_landmarks.landmark:
                    data.extend([lm.x, lm.y, lm.z])

                pred = model.predict([data])[0]
                pred_buffer.append(pred)

                if len(pred_buffer) == pred_buffer.maxlen:
                    prediction = max(set(pred_buffer), key=pred_buffer.count)

                    
                    if prediction != last_added_word:
                        word_list.append(prediction)
                        update(" ".join(word_list))
                        last_added_word = prediction

                    last_detection_time = time.time()

        # Show live prediction
        cv2.putText(frame, f"{prediction}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Sign Detection", frame)

        # 🛑 STOP CONDITION (no gesture for 5 sec)
        if time.time() - last_detection_time > TIMEOUT:
            update("No gesture detected. Ending...")
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    # 🔥 NEXT PROCESS (for now just print)
    print("Final Word List:", word_list)

    return word_list
