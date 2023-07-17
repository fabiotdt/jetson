import pyzed.sl as sl
import os
import viewer as gl
import math
import numpy as np
import sys
import csv
import cv2
import matplotlib.pyplot as plt

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

def file_writer(idx, timestamp, point_cloud_to_save, image_L_to_save=None, image_R_to_save=None):

    """
    Generate a csv file containing information about the retrieved data. Write the point cloud to a file and save the images.

    Args:
        idx (int): The index of the point cloud
        timestamp (int): The timestamp of the point cloud
        point_cloud_to_save (pyzed.sl.Mat): The point cloud to save
        image_L_to_save (pyzed.sl.Mat, optional): The left image to save. Default to None.
        image_R_to_save (pyzed.sl.Mat, optional): The right image to save. Default to None.

    Returns:
        err (pyzed.sl.ERROR_CODE): The error code if the point cloud was not saved
        idx (int): The index of the point cloud
    """
    
    name= "test_"+str(idx)

    with open('list.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow([name, timestamp, idx])
        f.close()
                
    err = point_cloud_to_save.write(name+'.ply')
    
    if image_L_to_save is not None: cv2.imwrite(name+'_L.jpg', image_L_to_save.get_data())
    if image_R_to_save is not None: cv2.imwrite(name+'_R.jpg', image_R_to_save.get_data())    
    
    idx+=1

    return err, idx


def compute_centre(res, point_cloud):

    """Calcualte depth of the centre point of the image

    Args:
        image (pyzed.sl.Mat): The image to compute the depth of
        point_cloud (pyzed.sl.Mat): The point cloud corresponding to the image

    Returns:
        None
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
    sys.stdout.flush()

def main():
    
    """Main function to run the ZED camera
    """

    init, runtime_parameters = params()

    zed = sl.Camera()
    status = zed.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()
    
    res = sl.Resolution()
    res.width = 720
    res.height = 404
    
    print("Running Sensing ... Press 'Esc' to quit\nPress 's' to save the point cloud\n")

    i = 0
    camera_model = zed.get_camera_information().camera_model
    viewer = gl.GLViewer()
    viewer.init(1 , sys.argv,  camera_model, res)

    point_cloud = sl.Mat(res.width, res.height, sl.MAT_TYPE.F32_C4, sl.MEM.CPU) # ALIGNED WITH LEFT IMAGE
    #point_cloud = sl.Mat(res.width, res.height, sl.MAT_TYPE.F32_C4, sl.MEM.CPU) # ALIGNED WITH RIGHT IMAGE
    depth = sl.Mat() # ALIGNED WITH LEFT IMAGE
    image_L = sl.Mat()
    image_R = sl.Mat()
    
    if 'list.csv' not in os.listdir():
        with open('list.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(["filename", "timestamp", "index"])
            f.close()
    elif 'list.csv' in os.listdir() and os.stat('list.csv').st_size == 0:
        with open('list.csv', 'r', encoding='UTF8') as f:
            final_line = f.readlines()[-1]
            i = int(final_line.split(',')[-1]) + 1 
            f.close()

    while viewer.is_available():
        
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA,sl.MEM.CPU, res)
            zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
            zed.retrieve_image(image_L, sl.VIEW.LEFT)
            zed.retrieve_image(image_R, sl.VIEW.RIGHT)
            
            viewer.updateData(point_cloud)
            
            #cv2.imshow("image_R", image_R.get_data())
        
            if(viewer.save_data == True):
                compute_centre(res, point_cloud)
                point_cloud_to_save = sl.Mat()
                depth_to_save = sl.Mat()
                image_L_to_save = sl.Mat()
                image_R_to_save = sl.Mat()

                zed.retrieve_measure(point_cloud_to_save, sl.MEASURE.XYZRGBA, sl.MEM.CPU)
                zed.retrieve_image(image_L_to_save, sl.VIEW.LEFT)
                zed.retrieve_image(image_R_to_save, sl.VIEW.RIGHT)
                """zed.retrieve_measure(depth_to_save, sl.MEASURE.DEPTH, sl.MEM.CPU)
                zed.retrieve_image(image_L_to_save, sl.VIEW.LEFT, sl.MEM.CPU)
                zed.retrieve_image(image_R_to_save, sl.VIEW.RIGHT, sl.MEM.CPU)"""

                cv2.imshow("image_L", image_L_to_save.get_data())

                timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT)  # Get the timestamp at the time the image was captured
                err, i = file_writer(i, timestamp.get_milliseconds(), image_L_to_save, image_R_to_save)

                if(err == sl.ERROR_CODE.SUCCESS):
                    print("point cloud saved\n")
                else:
                    print("the point cloud has not been saved\n")
                viewer.save_data = False

    viewer.exit()
    zed.close()

if __name__ == "__main__":
    main()