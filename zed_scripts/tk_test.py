import tkinter as tk
from tkinter import ttk
from random import randint
import os

class storing_data():
    def __init__(self, base_root):
        #self.base_root = '/media/jetson/Volume/Data'
        
        self.left_img = os.path.join(base_root, 'left_image')
        self.right_img = os.path.join(base_root, 'right_image')
        self.depth_img = os.path.join(base_root, 'depth')
        self.point_cloud = os.path.join(base_root, 'point_cloud')
        self.recap_root = os.path.join(base_root, 'recap')

    def __len__(self, path):        
        return len(os.listdir(path))
    
    def __split__(self, path):
        return path.split('/')[-1]


def window(root):
    
    frame = tk.Tk()
    screen_width = frame.winfo_screenwidth()
    screen_height = frame.winfo_screenheight()
    
    frame.title("Files summary")
    frame.geometry(str(int(screen_width*0.45)) + "x" + str(int(screen_height*0.5)))

    ttk.Button(frame, text=root.__split__(root.left_img)).pack()
    ttk.Button(frame, text=root.__split__(root.right_img)).pack()
    ttk.Button(frame, text=root.__split__(root.depth_img)).pack()
    ttk.Button(frame, text=root.__split__(root.point_cloud)).pack()
    ttk.Button(frame, text=root.__split__(root.recap_root)).pack()

    frame.mainloop()

def main():
    base_root = '/media/jetson/Volume/Data'
    root = storing_data(base_root)
    window(root)


if __name__ == "__main__":
    main()