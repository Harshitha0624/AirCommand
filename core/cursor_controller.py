import pyautogui
import numpy as np
import math
import time
from config import FRAME_REDUCTION, SMOOTHING, CAM_WIDTH, CAM_HEIGHT


class CursorController:

    def __init__(self):

        self.screen_width, self.screen_height = pyautogui.size()

        self.prev_screen_x = 0
        self.prev_screen_y = 0
        self.prev_raw = None

        self.dragging = False

        # Acceleration tuning
        self.max_acceleration = 2.5
        self.min_acceleration = 1.0
        self.acceleration_scale = 0.04

        # Click system
        self.last_click_time = 0
        self.double_click_window = 0.5
        self.click_cooldown = 0.2

        # Thumb fold threshold
        self.thumb_threshold = 40

    # -------------------------------------------------
    # Cursor Movement
    # -------------------------------------------------

    def move(self, landmarks, bounds=None):

        if len(landmarks) == 0:
            self.prev_raw = None
            return 0, 1

        hand = landmarks[0]
        index_finger = next((p for p in hand if p["id"] == 8), None)

        if index_finger is None:
            return 0, 1

        raw_x = index_finger["x"]
        raw_y = index_finger["y"]

        # Adaptive mapping
        if bounds and bounds["min_x"] is not None:
            mapped_x = np.interp(
                raw_x,
                (bounds["min_x"], bounds["max_x"]),
                (0, self.screen_width)
            )
        else:
            mapped_x = np.interp(
                raw_x,
                (FRAME_REDUCTION, CAM_WIDTH - FRAME_REDUCTION),
                (0, self.screen_width)
            )

        if bounds and bounds["min_y"] is not None:
            mapped_y = np.interp(
                raw_y,
                (bounds["min_y"], bounds["max_y"]),
                (0, self.screen_height)
            )
        else:
            mapped_y = np.interp(
                raw_y,
                (FRAME_REDUCTION, CAM_HEIGHT - FRAME_REDUCTION),
                (0, self.screen_height)
            )

        # Speed
        if self.prev_raw is not None:
            dx = raw_x - self.prev_raw[0]
            dy = raw_y - self.prev_raw[1]
            speed = math.hypot(dx, dy)
        else:
            speed = 0

        acceleration = self.min_acceleration + speed * self.acceleration_scale
        acceleration = min(acceleration, self.max_acceleration)

        mapped_x *= acceleration
        mapped_y *= acceleration

        smooth_x = self.prev_screen_x + (mapped_x - self.prev_screen_x) / SMOOTHING
        smooth_y = self.prev_screen_y + (mapped_y - self.prev_screen_y) / SMOOTHING

        smooth_x = max(1, min(self.screen_width - 2, smooth_x))
        smooth_y = max(1, min(self.screen_height - 2, smooth_y))

        pyautogui.moveTo(smooth_x, smooth_y)

        self.prev_screen_x = smooth_x
        self.prev_screen_y = smooth_y
        self.prev_raw = (raw_x, raw_y)

        return speed, acceleration

    # -------------------------------------------------
    # Click Detection
    # -------------------------------------------------

    def handle_click(self, landmarks, mode):

        if mode != "MOVE":
            return

        if len(landmarks) == 0:
            return

        hand = landmarks[0]

        thumb_tip = next((p for p in hand if p["id"] == 4), None)
        index_base = next((p for p in hand if p["id"] == 5), None)

        if not thumb_tip or not index_base:
            return

        current_time = time.time()

        distance = math.hypot(
            thumb_tip["x"] - index_base["x"],
            thumb_tip["y"] - index_base["y"]
        )

        thumb_folded = distance < self.thumb_threshold

        if thumb_folded:

            if current_time - self.last_click_time < self.double_click_window:
                pyautogui.doubleClick()
                self.last_click_time = 0

            else:

                if current_time - self.last_click_time > self.click_cooldown:
                    pyautogui.click()
                    self.last_click_time = current_time

    # -------------------------------------------------
    # Drag & Drop
    # -------------------------------------------------

    def handle_drag(self, landmarks, mode):

        if mode != "MOVE":
            return

        if len(landmarks) == 0:
            return

        hand = landmarks[0]

        thumb_tip = next((p for p in hand if p["id"] == 4), None)
        thumb_joint = next((p for p in hand if p["id"] == 3), None)

        if not thumb_tip or not thumb_joint:
            return

        thumb_folded = thumb_tip["x"] <= thumb_joint["x"]

        if thumb_folded:

            if not self.dragging:
                pyautogui.mouseDown()
                self.dragging = True

        else:

            if self.dragging:
                pyautogui.mouseUp()
                self.dragging = False