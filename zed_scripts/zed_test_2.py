import pyzed.sl as sl
import viewer as gl
import math
import numpy as np
import sys


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

def writer(idx = None):
    
    name= "test_"+str(idx)+".ply"
    idx+=1



    return name, idx


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
        print("Distance to Camera at ({}, {}) (image center): {:.2f} m".format(x, y, distance), end="\r")
    else:
        print("Can't estimate distance at this position.")
        print("Your camera is probably too close to the scene, please move it backwards.\n")
    sys.stdout.flush()

def displayer(zed, res):
    
    """Display the point cloud from the ZED camera

    Args:
        zed (pyzed.sl.Camera): The ZED camera
        res (pyzed.sl.Resolution): The resolution of the image

    Returns:
        None
    """
    
    print("Running Sensing ... Press 'Esc' to quit\nPress 's' to save the point cloud")

    i = 0
    camera_model = zed.get_camera_information().camera_model
    viewer = gl.GLViewer()
    viewer.init(1 , sys.argv,  camera_model, res)

    point_cloud = sl.Mat(res.width, res.height, sl.MAT_TYPE.F32_C4, sl.MEM.CPU)

    while viewer.is_available():
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA,sl.MEM.CPU, res)
            compute_centre(res, point_cloud)
            viewer.updateData(point_cloud)
            if(viewer.save_data == True):
                point_cloud_to_save = sl.Mat();
                zed.retrieve_measure(point_cloud_to_save, sl.MEASURE.XYZRGBA, sl.MEM.CPU)
                name, i = writer(i)
                err = point_cloud_to_save.write(name)
                if(err == sl.ERROR_CODE.SUCCESS):
                    print("point cloud saved")
                else:
                    print("the point cloud has not been saved")
                viewer.save_data = False
    viewer.exit()
    zed.close()

def main():

    init, runtime = params()

    zed = sl.Camera()
    status = zed.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()
    
    res = sl.Resolution()
    res.width = 720
    res.height = 404

    displayer(zed, res)

    """camera_model = zed.get_camera_information().camera_model
    viewer = gl.GLViewer()
   
    mage_L = sl.Mat()
    image_R = sl.Mat()
    depth_L = sl.Mat()
    point_cloud_L = sl.Mat()"""

    """res = sl.Resolution()
    res.width = image_L.get_width()
    res.height = image_L.get_height()"""

if __name__ == "__main__":
    main()