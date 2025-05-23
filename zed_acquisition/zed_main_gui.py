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
    'ager' : 'agerato',
    'bocl' : 'bocche_leone',
    'bego' : 'begonie',
    'marg' : 'margherite',
    'cale' : 'calendule',
    'borr' : 'borraggine',
    'fior' : 'fiordaliso',
    'dagr' : 'dalie_grandi',
    'dapi' : 'dalie_picole',
    'garo' : 'garofani',
    'fucs' : 'fucsie',
    'impa' : 'impatients',
    'gera' : 'geranei',
    'prim' : 'primule',
    'rose' : 'rose',
    'taget' : 'tagete',
    'vipo' : 'violette_piccole',
    'viga' : 'violette_grandi'
    }

class storing_data():
    def __init__(self, base_root):
        #self.base_root = '/media/jetson/Volume/Data'
        
        self.left_img = os.path.join(base_root, 'left_image')
        self.right_img = os.path.join(base_root, 'right_image')
        self.depth_img = os.path.join(base_root, 'depth')
        self.point_cloud = os.path.join(base_root, 'point_cloud')
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
    init_params.depth_mode = sl.DEPTH_MODE.NEURAL  # Use NEURAL depth mode, (Available: NONE, PERFORMANCE, NONE, ULTRA, NEURAL) 
    init_params.coordinate_units = sl.UNIT.METER  # Use millimiter units (for depth measurements, available METER, CENTIMITERS, INCH, FOOT) millimeters does not work
    
    init_params.depth_maximum_distance = 10
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP # Standard coordinate system
    init_params.camera_resolution = sl.RESOLUTION.HD720 # Image Resolution (HD2K, HD1080, HD720, SVGA, VGA)
    init_params.camera_fps = 30

    # Create and set RuntimeParameters after opening the camera
    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.confidence_threshold = 100
    runtime_parameters.texture_confidence_threshold = 100

    return init_params, runtime_parameters

def file_writer(variety, writer_input, win):

    """
    Generate a csv file containing information about the retrieved data. Write the point cloud to a file and save the images.

    Args:
        root (storing_data): The root directory to store the data
        idx (int): The index of the point cloud
        timestamp (int): The timestamp of the point cloud
        point_cloud_to_save (pyzed.sl.Mat): The point cloud to save
        image_L_to_save (pyzed.sl.Mat, optional): The left image to save. Default to None.
        image_R_to_save (pyzed.sl.Mat, optional): The right image to save. Default to None.
        depth_map (pyzed.sl.Mat, optional): The depth map to save. Default to None.

    Returns:
        err (pyzed.sl.ERROR_CODE): The error code if the point cloud was not saved
        idx (int): The index of the point cloud
    """
    
    win.destroy()
    
    root, idx, timestamp, dist, point_cloud, image_L, image_R, depth_map = writer_input

    name = variety+"_"+str(idx)
                
    err = point_cloud.write(os.path.join(root.point_cloud,name+'.ply'))
    #if depth_map is not None: save = depth_map.write(os.path.join(root.depth_img,name + '.png'))
    if depth_map is not None: cv2.imwrite(os.path.join(root.depth_img,name+'.png'), depth_map.get_data())

    if image_L is not None: cv2.imwrite(os.path.join(root.left_img,name+'_L.jpg'), image_L.get_data())
    if image_R is not None: cv2.imwrite(os.path.join(root.right_img,name+'_R.jpg'), image_R.get_data())
       

    with open(os.path.join(root.recap_root, 'list.csv'), 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow([name, timestamp, round(dist,4), err,'SUCCESS' if image_L is not None else 'ERROR', 'SUCCESS' if image_R is not None else 'ERROR', 'SUCCESS' if depth_map is not None else 'ERROR',  idx])
        f.close()

    if(err == sl.ERROR_CODE.SUCCESS):
        print("all saved\n")
    else:
        print("the point cloud OR the depth map has NOT been saved\n")


def namer(writer_input):

    """Create a GUI to select the flower variety to save.

    Args:
        root (storing_data): The root directory to store the data
        idx (int): The index of the point cloud
        timestamp (int): The timestamp of the point cloud
        point_cloud_to_save (pyzed.sl.Mat): The point cloud to save
        image_L_to_save (pyzed.sl.Mat, optional): The left image to save. Default to None.
        image_R_to_save (pyzed.sl.Mat, optional): The right image to save. Default to None.

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

def compute_centre(res, point_cloud):

    """Calcualte depth of the centre point of the image.
    This depth point will be printed to the terminal.

    Args:
        image (pyzed.sl.Mat): The image to compute the depth of
        point_cloud (pyzed.sl.Mat): The point cloud corresponding to the image

    Returns:
        distance (float): The distance of the centre point of the image
    """
    
    # Get the centre point of the image
    x = round(res.width / 2)
    y = round(res.height / 2)
    err, point_cloud_value = point_cloud.get_value(x, y)

    # Compute the distance of this centre point via Euclidean distance
    distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +
                                point_cloud_value[1] * point_cloud_value[1] +
                                point_cloud_value[2] * point_cloud_value[2])

    if not np.isnan(distance) and not np.isinf(distance):
        print("Distance to Camera at ({}, {}) (image center): {:.2f} m".format(x, y, distance), end="\n")
    else:
        print("Can't estimate distance at this position.")
        print("Your camera is probably too close to the scene, please move it backwards.\n")
    #sys.stdout.flush()

    return distance

def displayer(zed, viewer, point_cloud, res, image_L, image_R):

    """Display the data stream (let and right image, depth point cloud) from the ZED camera

    Args:
        zed (pyzed.sl.Camera): The ZED camera
        viewer (pyzed.gl.GLViewer): The viewer to display the point cloud as Gl object
        image_L (pyzed.sl.Mat): The left image to display
        image_R (pyzed.sl.Mat): The right image to display
        point_cloud (pyzed.sl.Mat): The point cloud to display
        res (pyzed.sl.Resolution): The resolution of the data stream

    Returns:
        None
    """

    # Retrieve resolution from the screen where the data stream is displayed
    sc_w = int(glutGet(GLUT_SCREEN_WIDTH))
    sc_h = int(glutGet(GLUT_SCREEN_HEIGHT))

    # Retrieve the left image, right image, point cloud
    zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA,sl.MEM.CPU, res)
    #zed.retrieve_measure(depth, sl.MEASURE.DEPTH)

    # Create a window to display the left image
    #if 'image_L' is not None:
    zed.retrieve_image(image_L, sl.VIEW.LEFT)
    cv2.namedWindow("LEFT_IMAGES", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("LEFT_IMAGES", int(sc_w*0.24), int(sc_h*0.4))
    cv2.moveWindow("LEFT_IMAGES", int(sc_w*0.52), int(sc_h*0.55))
    cv2.imshow("LEFT_IMAGES", image_L.get_data())
    cv2.waitKey(1)
    # Create a window to display the right image
    #if 'image_R' is not None:
    zed.retrieve_image(image_R, sl.VIEW.RIGHT)
    cv2.namedWindow("RIGHT_IMAGES", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("RIGHT_IMAGES", int(sc_w*0.24), int(sc_h*0.4))
    cv2.moveWindow("RIGHT_IMAGES", int(sc_w*0.85), int(sc_h*0.55))
    cv2.imshow("RIGHT_IMAGES", image_R.get_data())
    cv2.waitKey(1)

    viewer.updateData(point_cloud)


def main():
    
    """Main function to run the ZED camera
    """

    #main_root = '/media/jetson/Volume/Data'
    #main_root = '/home/jetson/Documents/Fabio/Data'
    main_root = '/media/jetson/TDTF_sd/Data'
    
    root = storing_data(main_root)

    init, runtime_parameters = params()

    zed = sl.Camera()
    status = zed.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()
    
    # Set resolution for the data caputred by the ZED camera
    res = sl.Resolution()
    res.width = zed.get_camera_information().camera_configuration.resolution.width
    res.height = zed.get_camera_information().camera_configuration.resolution.height
    
    print("Running Sensing ... Press 'Esc' to quit\nPress 's' to save the point cloud\n")

    i = 0
    camera_model = zed.get_camera_information().camera_model
    viewer = gl.GLViewer()
    viewer.init(1 , sys.argv,  camera_model, res)

    point_cloud = sl.Mat(res.width, res.height, sl.MAT_TYPE.F32_C4, sl.MEM.CPU) # ALIGNED WITH LEFT IMAGE
    #depth = sl.Mat() # ALIGNED WITH LEFT IMAGE
    image_L = sl.Mat(res.width, res.height, sl.MAT_TYPE.U8_C4)
    image_R = sl.Mat(res.width, res.height, sl.MAT_TYPE.U8_C4)
    
    if 'list.csv' not in os.listdir(root.recap_root):
        with open(os.path.join(root.recap_root, 'list.csv'), 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(["filename","timestamp", "centre_depth", "point_cloud", "left_image", "right_image", "depth_map"  "index"])
            f.close()
    else:
        with open(os.path.join(root.recap_root, 'list.csv'), 'r', encoding='UTF8') as f:
            final_line = f.readlines()[-1]
            previous = final_line.split(',')[-1]
            f.close()
            if previous == 'index\n':
                i = 0
            else:
                i = int(previous) + 1

    while viewer.is_available():
        
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            
            displayer(zed, viewer, point_cloud, res, image_L, image_R)

        if(viewer.save_data == True):

            dist = compute_centre(res, point_cloud)

            point_cloud_to_save = sl.Mat()
            depth_to_save = sl.Mat()
            image_L_to_save = sl.Mat()
            image_R_to_save = sl.Mat()

            zed.retrieve_measure(point_cloud_to_save, sl.MEASURE.XYZRGBA, sl.MEM.CPU)
            #zed.retrieve_measure(depth_to_save, sl.MEASURE.DEPTH, sl.MEM.CPU)
            zed.retrieve_image(depth_to_save, sl.VIEW.DEPTH)

            zed.retrieve_image(image_L_to_save, sl.VIEW.LEFT)
            zed.retrieve_image(image_R_to_save, sl.VIEW.RIGHT)

            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT)  # Get the timestamp at the time the image was captured

            writer_input = [root, i, timestamp.get_milliseconds(),  dist, point_cloud_to_save, image_L_to_save, image_R_to_save, depth_to_save]
            
            namer(writer_input)
            
            i += 1

            viewer.save_data = False

    cv2.destroyAllWindows()
    viewer.exit()
    zed.close()

if __name__ == "__main__":
    main()