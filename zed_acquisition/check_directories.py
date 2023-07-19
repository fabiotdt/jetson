import tkinter as tk
from tkinter import *
from tkinter import ttk
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
    

base_root = '/media/jetson/Volume/Data'
root = storing_data(base_root)

frame = tk.Tk()
screen_width = frame.winfo_screenwidth()
screen_height = frame.winfo_screenheight()

frame.title("Files summary")
frame.geometry(str(int(screen_width*0.45)) + "x" + str(int(screen_height*0.5)))

def update():
    l_img_num.config(text=str(root.__len__(root.left_img)))
    r_img_num.config(text=str(root.__len__(root.right_img)))
    d_img_num.config(text=str(root.__len__(root.depth_img)))
    p_cloud_num.config(text=str(root.__len__(root.point_cloud)))
    recap_num.config(text=str(root.__len__(root.recap_root)))
    
    frame.after(1000, update)


l_img = tk.Label(frame, text="Left image: ", font=("Helvetica", 16))
l_img.grid(row=0, column=0, ipadx=10, ipady=10)

l_img_num = tk.Label(frame, font=("Helvetica", 16))
l_img_num.grid(row=0, column=1, ipadx=10, ipady=10)

r_img = tk.Label(frame, text="Right image: ", font=("Helvetica", 16))
r_img.grid(row=1, column=0, ipadx=10, ipady=10)

r_img_num = tk.Label(frame, font=("Helvetica", 16))
r_img_num.grid(row=1, column=1, ipadx=10, ipady=10)

d_img = tk.Label(frame, text="Depth image: ", font=("Helvetica", 16))
d_img.grid(row=2, column=0, ipadx=10, ipady=10)

d_img_num = tk.Label(frame, font=("Helvetica", 16))
d_img_num.grid(row=2, column=1, ipadx=10, ipady=10)

p_cloud = tk.Label(frame, text="Point cloud: ", font=("Helvetica", 16))
p_cloud.grid(row=3, column=0, ipadx=10, ipady=10)

p_cloud_num = tk.Label(frame, font=("Helvetica", 16))
p_cloud_num.grid(row=3, column=1, ipadx=10, ipady=10)

recap = tk.Label(frame, text="Recap: ", font=("Helvetica", 16))
recap.grid(row=4, column=0, ipadx=10, ipady=10)

recap_num = tk.Label(frame, font=("Helvetica", 16))
recap_num.grid(row=4, column=1, ipadx=10, ipady=10)

update()
frame.mainloop()

