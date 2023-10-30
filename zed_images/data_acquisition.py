import pyzed.sl as sl
import os
import viewer as gl
import math
import numpy as np
import sys
import csv
import cv2
import matplotlib.pyplot as plt
from tkinter import *
from OpenGL.GLUT import *

flowers = {
    #'ager' : 'agerato',
    'bocl' : 'bocche_leone',
    #'bego' : 'begonie',
    #'marg' : 'margherite',
    #'cale' : 'calendule',
    #'borr' : 'borraggine',
    #'fior' : 'fiordaliso',
    #'dagr' : 'dalie_grandi',
    #'dapi' : 'dalie_picole',
    #'garo' : 'garofani',
    #'fucs' : 'fucsie',
    #'impa' : 'impatients',
    #'gera' : 'geranei',
    #'prim' : 'primule',
    #'rose' : 'rose',
    'taget' : 'tagete',
    #'vipo' : 'violette_piccole',
    'viga' : 'violette_grandi'
    }

cam = sl.Camera()

class storing_data():
    def __init__(self, base_root):
        #self.base_root = '/media/jetson/Volume/Data'
        
        self.left_img = os.path.join(base_root, 'left_image')
        self.right_img = os.path.join(base_root, 'right_image')
        self.dim_root = os.path.join(base_root, 'measures')
        self.recap_root = os.path.join(base_root, 'recap')

def params():
    
    """Set the parameters for the ZED camera
    Args:
        None

    Returns:  
        init_params (pyzed.sl.InitParameters): The parameters for the ZED camera
        runtime_parameters (pyzed.sl.RuntimeParameters): The runtime parameters for the ZED camera
    """
    
    #Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP # Standard coordinate system
    init_params.camera_resolution = sl.RESOLUTION.HD2K # Image Resolution (HD2K, HD1080, HD720, SVGA, VGA)
    #init_params.camera_fps = 30

    # Create and set RuntimeParameters after opening the camera
    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.confidence_threshold = 100
    runtime_parameters.texture_confidence_threshold = 100

    return init_params, runtime_parameters

def file_writer(variety, writer_input, win):

    """
    Generate:
        - a csv file containing information about the retrieved data
        - a left and right images
        - a csv contianing the information about the flower dimensions

    Args:
        root (storing_data): The root directory to store the data
        idx (int): The index of the point cloud
        timestamp (int): The timestamp of the point cloud
        image_L_to_save (pyzed.sl.Mat, optional): The left image to save. Default to None.
        image_R_to_save (pyzed.sl.Mat, optional): The right image to save. Default to None.
        measures (list): The list containing the measures of the flower

    Returns:
        err (pyzed.sl.ERROR_CODE): The error code if one image is not saved
        idx (int): The index of the point cloud
    """
    
    win.destroy()
    
    root, idx, timestamp, image_L, image_R, measures = writer_input

    name = variety+"_"+str(idx)
                
    if image_L is not None: cv2.imwrite(os.path.join(root.left_img,name+'_L.jpg'), image_L.get_data())
    if image_R is not None: cv2.imwrite(os.path.join(root.right_img,name+'_R.jpg'), image_R.get_data())
       

    with open(os.path.join(root.recap_root, 'list.csv'), 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow([name, timestamp, round(dist,4), err,'SUCCESS' if image_L is not None else 'ERROR', 'SUCCESS' if image_R is not None else 'ERROR', 'SUCCESS' if depth_map is not None else 'ERROR',  idx])
        f.close()

    with open(os.path.join(root.dim_root, 'measures.csv'), 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow([name, timestamp, round(dist,4), measures[0], measures[1],  idx])
        f.close()

    print("all saved\n")

def namer(writer_input):

    """
    Create an interface which is used to collect data bout the flower and its measures.

    Args:
        root (storing_data): The root directory to store the data
        idx (int): The index of the point cloud
        timestamp (int): The timestamp of the point cloud
        image_L_to_save (pyzed.sl.Mat, optional): The left image to save. Default to None.
        image_R_to_save (pyzed.sl.Mat, optional): The right image to save. Default to None.
        measures (list): The list containing the measures of the flower

    Returns:
        None
        However, it calls the file_writer function when one of the button is pressed.
    """

    #Create an instance of the canvas
    win = Tk()

    #Select the title of the window
    win.title("Choose the flower")

    #Define the geometry of the window
    win.geometry("600x700")   

    #Create a label to display the instructions
    instructions = Label(win, text="Choose the flower you want to save")
    instructions.grid(row=0, column=0, columnspan=2, padx = 1, pady = 1)
   
    for idx, key in enumerate(flowers.keys()):
        key_lab = Label(win, text=flowers[key]+": ")
        key_lab.grid(row=idx+1, column=0, padx = 1, pady = 1)  
        key_but = Button(win, text = key, command = lambda key=key: file_writer(key, writer_input, win))
        key_but.grid(row=idx+1, column=1, padx = 1, pady = 1)
    
    win.mainloop()

def handler(signal_received, frame):
    cam.disable_recording()
    cam.close()
    sys.exit(0)

signal(SIGINT, handler)

def main(base_root):
    """if not sys.argv or len(sys.argv) != 2:
        print("Only the path of the output SVO file should be passed as argument.")
        exit(1)"""

    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.depth_mode = sl.DEPTH_MODE.NONE

    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    #path_output = sys.argv[1]
    path_output = os.path.join(base_root, 'svo_file.svo')
    recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.H264)
    err = cam.enable_recording(recording_param)

    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        exit(1)

    runtime = sl.RuntimeParameters()
    print("SVO is Recording, use Ctrl-C to stop.")
    frames_recorded = 0

    while True:
        if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS :
            frames_recorded += 1
            print("Frame count: " + str(frames_recorded), end="\r")

if __name__ == "__main__":
    base_root = '/media/jetson/TDTF_sd/Data/SVO'
    main(base_root)