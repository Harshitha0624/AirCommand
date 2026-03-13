import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands=1):
        self.max_hands = max_hands

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=self.max_hands,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        landmarks_list = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                single_hand = []
                h, w, _ = frame.shape

                for idx, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    single_hand.append({
                        "id": idx,
                        "x": cx,
                        "y": cy,
                        "z": lm.z
                    })

                landmarks_list.append(single_hand)

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return frame, landmarks_list
