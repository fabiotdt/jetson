import tkinter as tk
from tkinter import *
from tkinter import ttk
import os

base_root = '/media/jetson/Volume/Data'

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
    
class window():
    def __init__(self, base_root):
        self.root = storing_data(base_root)

        self.frame = tk.Tk()
        screen_width = self.frame.winfo_screenwidth()
        screen_height = self.frame.winfo_screenheight()

        self.frame.title("Files summary")
        self.frame.geometry(str(int(screen_width*0.45)) + "x" + str(int(screen_height*0.5)))

        self.l_img = tk.Label(self.frame, text="Left image: ", font=("Helvetica", 16))
        self.l_img.grid(row=0, column=0, ipadx=10, ipady=10)

        self.l_img_num = tk.Label(self.frame, font=("Helvetica", 16))
        self.l_img_num.grid(row=0, column=1, ipadx=10, ipady=10)

        self.r_img = tk.Label(self.frame, text="Right image: ", font=("Helvetica", 16))
        self.r_img.grid(row=1, column=0, ipadx=10, ipady=10)

        self.r_img_num = tk.Label(self.frame, font=("Helvetica", 16))
        self.r_img_num.grid(row=1, column=1, ipadx=10, ipady=10)

        self.d_img = tk.Label(self.frame, text="Depth image: ", font=("Helvetica", 16))
        self.d_img.grid(row=2, column=0, ipadx=10, ipady=10)

        self.d_img_num = tk.Label(self.frame, font=("Helvetica", 16))
        self.d_img_num.grid(row=2, column=1, ipadx=10, ipady=10)

        self.p_cloud = tk.Label(self.frame, text="Point cloud: ", font=("Helvetica", 16))
        self.p_cloud.grid(row=3, column=0, ipadx=10, ipady=10)

        self.p_cloud_num = tk.Label(self.frame, font=("Helvetica", 16))
        self.p_cloud_num.grid(row=3, column=1, ipadx=10, ipady=10)

        self.recap = tk.Label(self. frame, text="Recap: ", font=("Helvetica", 16))
        self.recap.grid(row=4, column=0, ipadx=10, ipady=10)

        self.recap_num = tk.Label(self.frame, font=("Helvetica", 16))
        self.recap_num.grid(row=4, column=1, ipadx=10, ipady=10)

    def update(self):
        self.l_img_num.config(text=str(self.root.__len__(self.root.left_img)))
        self.r_img_num.config(text=str(self.root.__len__(self.root.right_img)))
        self.d_img_num.config(text=str(self.root.__len__(self.root.depth_img)))
        self.p_cloud_num.config(text=str(self.root.__len__(self.root.point_cloud)))
        self.recap_num.config(text=str(self.root.__len__(self.root.recap_root)))
        
        self.frame.after(1000, window.update)


main_frame = window(base_root)
#main_frame.update
main_frame.frame.mainloop()
