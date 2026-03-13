import pyautogui


class GestureEngine:

    def __init__(self):
        self.prev_y = None
        self.scroll_sensitivity = 3

    def finger_is_up(self, tip, pip):
        return tip["y"] < pip["y"]

    def process(self, landmarks):

        if len(landmarks) == 0:
            self.prev_y = None
            return "MOVE"

        hand = landmarks[0]

        # -------- Finger Landmarks -------- #

        index_tip = next((p for p in hand if p["id"] == 8), None)
        index_pip = next((p for p in hand if p["id"] == 6), None)

        middle_tip = next((p for p in hand if p["id"] == 12), None)
        middle_pip = next((p for p in hand if p["id"] == 10), None)

        ring_tip = next((p for p in hand if p["id"] == 16), None)
        ring_pip = next((p for p in hand if p["id"] == 14), None)

        pinky_tip = next((p for p in hand if p["id"] == 20), None)
        pinky_pip = next((p for p in hand if p["id"] == 18), None)

        if None in (
            index_tip, index_pip,
            middle_tip, middle_pip,
            ring_tip, ring_pip,
            pinky_tip, pinky_pip
        ):
            return "MOVE"

        # -------- Finger States -------- #

        index_up = self.finger_is_up(index_tip, index_pip)
        middle_up = self.finger_is_up(middle_tip, middle_pip)
        ring_up = self.finger_is_up(ring_tip, ring_pip)
        pinky_up = self.finger_is_up(pinky_tip, pinky_pip)

        # ---------------- CLEAR (4 fingers) ---------------- #

        if index_up and middle_up and ring_up and pinky_up:
            return "CLEAR"

        # ---------------- DRAW (2 fingers) ---------------- #

        if index_up and middle_up and not ring_up:
            return "DRAW"

        # ---------------- SCROLL (3 fingers) ---------------- #

        if index_up and middle_up and ring_up and not pinky_up:

            current_y = index_tip["y"]

            if self.prev_y is not None:
                delta_y = self.prev_y - current_y

                if abs(delta_y) > 5:
                    pyautogui.scroll(int(delta_y * self.scroll_sensitivity))

            self.prev_y = current_y
            return "SCROLL"

        self.prev_y = None
        return "MOVE"