import cv2
from tkinter import *
from OpenGL.GLUT import *
from PIL import Image, ImageTk


def on_button_click():
    text1 = entry1.get()
    text2 = entry2.get()
    print(f"Text from Entry 1: {text1}")
    print(f"Text from Entry 2: {text2}")

def display():
    
    win = Tk()
    win.title("Flower Image and Measurement Manager")

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    win.geometry(f"{screen_width}x{screen_height}")

    image_L = Image.open('taget_0.png')
    cv2.namedWindow("LEFT_IMAGES", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("LEFT_IMAGES", int(sc_w*0.24), int(sc_h*0.4))
    cv2.moveWindow("LEFT_IMAGES", int(sc_w*0.52), int(sc_h*0.55))
    cv2.imshow("LEFT_IMAGES", image_L.get_data())
    cv2.waitKey(1)
    # Create a window to display the right image
    #if 'image_R' is not None:
    image_R = Image.open('taget_0.png')
    cv2.namedWindow("RIGHT_IMAGES", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("RIGHT_IMAGES", int(sc_w*0.24), int(sc_h*0.4))
    cv2.moveWindow("RIGHT_IMAGES", int(sc_w*0.85), int(sc_h*0.55))
    cv2.imshow("RIGHT_IMAGES", image_R.get_data())
    cv2.waitKey(1)

   
    win.mainloop()


display()
