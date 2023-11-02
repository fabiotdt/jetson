import tkinter as tk
import cv2
import pyzed.sl as sl
from tkinter import Entry, Label, Button
from PIL import Image, ImageTk
import numpy as np

class ZedVideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zed Camera Video Stream")

        # Create text boxes on the left
        self.text_box_left = Entry(self.root, width=40)
        self.text_box_left.grid(row=0, column=0, padx=10, pady=10)

        # Create a video frame on the right
        self.video_frame = tk.Frame(self.root, width=640, height=480)
        self.video_frame.grid(row=0, column=1, padx=10, pady=10)
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()

        self.zed = sl.Camera()
        self.init_params = sl.InitParameters()
        self.runtime_params = sl.RuntimeParameters()

        if self.zed.is_opened():
            self.zed.close()

        self.init_params.camera_resolution = sl.RESOLUTION.HD720
        self.init_params.camera_fps = 30

        err = self.zed.open(self.init_params)
        if err != sl.ERROR_CODE.SUCCESS:
            print(f"ZED Camera Open error: {err}")
            return

        self.streaming = True
        self.update_video_stream()

    def update_video_stream(self):
        if self.zed.grab(self.runtime_params) == sl.ERROR_CODE.SUCCESS:
            left_image = sl.Mat()
            self.zed.retrieve_image(left_image, sl.VIEW.LEFT)
            frame = left_image.get_data()

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.video_label.config(image=photo)
            self.video_label.image = photo
            self.video_frame.update()
            self.root.after(10, self.update_video_stream)

if __name__ == "__main__":
    root = tk.Tk()
    app = ZedVideoApp(root)
    root.mainloop()