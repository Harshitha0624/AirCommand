import speech_recognition as sr
import threading


class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.command = None
        self.running = True

        # Start listening in background thread
        thread = threading.Thread(target=self.listen_loop)
        thread.daemon = True
        thread.start()

    def listen_loop(self):
        while self.running:
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = self.recognizer.listen(source, phrase_time_limit=3)

                text = self.recognizer.recognize_google(audio)
                self.command = text.lower()

            except:
                pass

    def get_command(self):
        cmd = self.command
        self.command = None
        return cmd

    def stop(self):
        self.running = False
