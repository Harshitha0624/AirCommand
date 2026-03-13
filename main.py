import cv2
import time
import os

from core.hand_tracker import HandTracker
from core.cursor_controller import CursorController
from core.gesture_engine import GestureEngine
from core.voice_engine import VoiceEngine
from core.profile_manager import ProfileManager
from core.drawing_engine import DrawingEngine
from core.virtual_keyboard import VirtualKeyboard
from config import CAM_WIDTH, CAM_HEIGHT, FRAME_REDUCTION


def launch_app(name):

    if name == "chrome":
        os.system("start chrome")

    elif name == "vscode":
        os.system("code")

    elif name == "files":
        os.startfile("C:/")

    elif name == "youtube":
        os.system("start https://youtube.com")


def main():

    cap = cv2.VideoCapture(0)
    cap.set(3, CAM_WIDTH)
    cap.set(4, CAM_HEIGHT)

    tracker = HandTracker()
    cursor = CursorController()
    gesture_engine = GestureEngine()
    voice = VoiceEngine()
    profile_manager = ProfileManager()

    drawing = DrawingEngine(CAM_WIDTH, CAM_HEIGHT)
    keyboard = VirtualKeyboard()

    prev_time = 0
    mode = "MOVE"
    last_voice_text = ""

    keyboard_active = False

    calibrating = False
    calibrated = False
    calib_data = []

    calib_bounds = {
        "min_x": None,
        "max_x": None,
        "min_y": None,
        "max_y": None
    }

    saved_profile = profile_manager.load_profile()
    if saved_profile and "calibration" in saved_profile:
        calib_bounds = saved_profile["calibration"]
        calibrated = True
        print("Loaded saved calibration profile.")

    while True:

        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        frame, landmarks = tracker.process_frame(frame)

        cv2.rectangle(
            frame,
            (FRAME_REDUCTION, FRAME_REDUCTION),
            (CAM_WIDTH - FRAME_REDUCTION, CAM_HEIGHT - FRAME_REDUCTION),
            (255, 0, 255),
            2
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        if key == ord('c'):

            calibrating = not calibrating

            if not calibrating and len(calib_data) > 20:

                xs = [p[0] for p in calib_data]
                ys = [p[1] for p in calib_data]

                calib_bounds["min_x"] = min(xs)
                calib_bounds["max_x"] = max(xs)
                calib_bounds["min_y"] = min(ys)
                calib_bounds["max_y"] = max(ys)

                calibrated = True

                profile_manager.save_profile({
                    "calibration": calib_bounds
                })

                print("Calibration Complete")
                print("Saved Bounds:", calib_bounds)

            calib_data = []

        if calibrating and landmarks:

            hand = landmarks[0]
            index = next((p for p in hand if p["id"] == 8), None)

            if index:
                calib_data.append((index["x"], index["y"]))

        # ---------------- Voice Commands ---------------- #

        command = voice.get_command()

        if command:

            last_voice_text = command
            print("VOICE:", command)

            if "scroll" in command:
                mode = "SCROLL"

            elif "move" in command:
                mode = "MOVE"

            elif "open chrome" in command:
                launch_app("chrome")

            elif "open code" in command:
                launch_app("vscode")

            elif "open files" in command:
                launch_app("files")

            elif "open youtube" in command:
                launch_app("youtube")

            elif "keyboard" in command:
                keyboard_active = not keyboard_active

            elif "exit" in command:
                break

        # ---------------- Gesture Processing ---------------- #

        gesture_mode = gesture_engine.process(landmarks)

        if gesture_mode == "SCROLL":
            mode = "SCROLL"

        elif gesture_mode == "MOVE":
            mode = "MOVE"

        elif gesture_mode == "DRAW":
            mode = "DRAW"

        elif gesture_mode == "CLEAR":
            drawing.clear()

        # ---------------- Cursor Movement ---------------- #

        speed = 0
        acceleration = 1

        if mode == "MOVE":

            if calibrated:
                speed, acceleration = cursor.move(landmarks, calib_bounds)
            else:
                speed, acceleration = cursor.move(landmarks)

            cursor.handle_click(landmarks, mode)
            cursor.handle_drag(landmarks, mode)

        # ---------------- Drawing ---------------- #

        if mode == "DRAW" and landmarks:

            hand = landmarks[0]
            index_tip = next((p for p in hand if p["id"] == 8), None)

            if index_tip:
                drawing.draw(index_tip["x"], index_tip["y"])

        else:
            drawing.reset_line()

        # ---------------- Palette Click Detection ---------------- #

        if landmarks:

            hand = landmarks[0]
            index_tip = next((p for p in hand if p["id"] == 8), None)

            if index_tip:
                drawing.check_palette_click(index_tip["x"], index_tip["y"])

                if keyboard_active:
                    keyboard.press_key(index_tip["x"], index_tip["y"])

        # ---------------- Overlay Drawing ---------------- #

        frame = drawing.overlay(frame)

        # ---------------- Virtual Keyboard ---------------- #

        if keyboard_active:
            frame = keyboard.draw(frame)

        # ---------------- FPS ---------------- #

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
        prev_time = curr_time

        cv2.putText(frame, f"FPS: {int(fps)}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0),2)

        cv2.putText(frame, f"MODE: {mode}", (20,80),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)

        cv2.putText(frame, f"SPEED: {int(speed)}", (20,120),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,0),2)

        cv2.putText(frame, f"ACCEL: {acceleration:.2f}", (20,150),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)

        cv2.putText(frame, f"VOICE: {last_voice_text}", (20,185),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(200,200,200),1)

        if keyboard_active:
            cv2.putText(frame, "VIRTUAL KEYBOARD ACTIVE", (20,215),
                        cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),1)

        if calibrating:
            cv2.putText(frame,"CALIBRATING... Move hand fully",(20,240),
                        cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)

        if calibrated:
            cv2.putText(frame,"PROFILE LOADED",(20,270),
                        cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

        cv2.imshow("AirCommand - Adaptive Multimodal System", frame)

    voice.stop()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()