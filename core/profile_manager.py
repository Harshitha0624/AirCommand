import json
import os


class ProfileManager:
    def __init__(self, filename="user_profile.json"):
        self.filename = filename

    def save_profile(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_profile(self):
        if not os.path.exists(self.filename):
            return None

        with open(self.filename, "r") as f:
            return json.load(f)
