import cv2
import mediapipe as mp
import threading
import time
from snake_game import SnakeGame

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Simple gesture interpreter (up/down/left/right based on hand position)
def gesture_loop(game):
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        direction = None
        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            h, w, _ = frame.shape
            # Use wrist and index finger tip positions
            wrist = hand.landmark[mp_hands.HandLandmark.WRIST]
            index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            dx = (index_tip.x - wrist.x) * w
            dy = (index_tip.y - wrist.y) * h

            if abs(dy) > abs(dx):
                if dy < -50:
                    direction = "UP"
                elif dy > 50:
                    direction = "DOWN"
            else:
                if dx < -50:
                    direction = "LEFT"
                elif dx > 50:
                    direction = "RIGHT"

            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        if direction:
            game.set_direction(direction)

        cv2.putText(frame, f"Dir: {direction or '-'}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    game = SnakeGame()
    t = threading.Thread(target=gesture_loop, args=(game,), daemon=True)
    t.start()
    game.run()
