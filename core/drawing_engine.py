import cv2


class DrawingEngine:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.canvas = cv2.UMat(height, width, cv2.CV_8UC3).get()
        self.canvas[:] = 0

        self.prev_point = None
        self.color = (0, 0, 255)
        self.thickness = 5

        # Color palette boxes
        self.palette = {
            "red": ((10, 10, 70, 50), (0, 0, 255)),
            "blue": ((80, 10, 140, 50), (255, 0, 0)),
            "green": ((150, 10, 210, 50), (0, 255, 0)),
            "yellow": ((220, 10, 280, 50), (0, 255, 255)),
            "eraser": ((290, 10, 350, 50), (0, 0, 0))
        }

    def draw(self, x, y):

        if self.prev_point is None:
            self.prev_point = (x, y)
            return

        cv2.line(
            self.canvas,
            self.prev_point,
            (x, y),
            self.color,
            self.thickness
        )

        self.prev_point = (x, y)

    def reset_line(self):
        self.prev_point = None

    def clear(self):
        self.canvas[:] = 0

    def overlay(self, frame):

        frame = cv2.add(frame, self.canvas)

        # Draw palette UI
        for name, (box, color) in self.palette.items():

            x1, y1, x2, y2 = box

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)

            cv2.putText(
                frame,
                name,
                (x1 + 2, y2 + 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (255, 255, 255),
                1
            )

        return frame

    def check_palette_click(self, x, y):

        for name, (box, color) in self.palette.items():

            x1, y1, x2, y2 = box

            if x1 < x < x2 and y1 < y < y2:

                if name == "eraser":
                    self.color = (0, 0, 0)
                    self.thickness = 20
                else:
                    self.color = color
                    self.thickness = 5