import tkinter as tk
from tkinter import PhotoImage

def show_image(root, image_path):
    image = PhotoImage(file=image_path)
    image_label = tk.Label(root, image=image)
    image_label.image = image  #
    image_label.pack()

def main_window():
    #global root
    root = tk.Tk()
    root.title("Image Viewer")
    
    # Call the function to display the image
    show_image(root, "info_measurments.png")
    
    root.mainloop()

if __name__ == "__main__":
    main_window()