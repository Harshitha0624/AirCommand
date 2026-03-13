import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import threading
import time

from core.hand_tracker import HandTracker
from core.cursor_controller import CursorController
from core.gesture_engine import GestureEngine
from core.voice_engine import VoiceEngine
from config import CAM_WIDTH, CAM_HEIGHT


class AirCommandApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AirCommand - AI Multimodal System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")

        self.running = False

        # Backend engines
        self.tracker = HandTracker()
        self.cursor = CursorController()
        self.gesture_engine = GestureEngine()
        self.voice = VoiceEngine()  # still running if needed later

        self.mode = "MOVE"

        # Camera display
        self.video_label = tk.Label(root)
        self.video_label.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(root, bg="#1e1e1e")
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Start", command=self.start_system).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Stop", command=self.stop_system).grid(row=0, column=1, padx=10)

        self.status_label = tk.Label(root, text="Status: Idle", fg="white", bg="#1e1e1e")
        self.status_label.pack()

        self.cap = None

    def start_system(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="Status: Running")
            self.cap = cv2.VideoCapture(0)
            self.cap.set(3, CAM_WIDTH)
            self.cap.set(4, CAM_HEIGHT)

            thread = threading.Thread(target=self.video_loop)
            thread.daemon = True
            thread.start()

    def stop_system(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.status_label.config(text="Status: Stopped")

    def video_loop(self):
        prev_time = 0

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)

            # -------- Hand Tracking -------- #
            frame, landmarks = self.tracker.process_frame(frame)

            # -------- Gesture Mode -------- #
            gesture_mode = self.gesture_engine.process(landmarks)
            self.mode = gesture_mode

            # -------- Cursor Movement -------- #
            if self.mode == "MOVE":
                self.cursor.move(landmarks)

            # -------- Gesture Click (Thumb-based) -------- #
            # IMPORTANT: pass current mode to avoid scroll conflict
            self.cursor.handle_click(landmarks, self.mode)

            # -------- FPS -------- #
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
            prev_time = curr_time

            cv2.putText(frame,
                        f"FPS: {int(fps)}",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2)

            cv2.putText(frame,
                        f"MODE: {self.mode}",
                        (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2)

            # -------- Stabilize Display -------- #
            frame = cv2.resize(frame, (800, 500))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

            time.sleep(0.01)

        if self.cap:
            self.cap.release()


if __name__ == "__main__":
    root = tk.Tk()
    app = AirCommandApp(root)
    root.mainloop()
