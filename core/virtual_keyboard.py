import cv2
import pyautogui


class VirtualKeyboard:

    def __init__(self):

        self.keys = [
            ["Q","W","E","R","T","Y","U","I","O","P"],
            ["A","S","D","F","G","H","J","K","L"],
            ["Z","X","C","V","B","N","M"]
        ]

        self.key_size = 60
        self.start_x = 50
        self.start_y = 350

    def draw(self, frame):

        for row_idx, row in enumerate(self.keys):

            for col_idx, key in enumerate(row):

                x = self.start_x + col_idx * self.key_size
                y = self.start_y + row_idx * self.key_size

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + self.key_size, y + self.key_size),
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    key,
                    (x + 20, y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2
                )

        return frame

    def press_key(self, x, y):

        for row_idx, row in enumerate(self.keys):

            for col_idx, key in enumerate(row):

                kx = self.start_x + col_idx * self.key_size
                ky = self.start_y + row_idx * self.key_size

                if kx < x < kx + self.key_size and ky < y < ky + self.key_size:

                    pyautogui.press(key.lower())