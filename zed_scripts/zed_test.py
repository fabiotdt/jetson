import pyzed.sl as sl
import viewer as gl
import math
import numpy as np
import sys

def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.NEURAL  # Use NEURAL depth mode, (Available: NONE, PERFORMANCE, NONE, ULTRA, NEURAL) 
    init_params.coordinate_units = sl.UNIT.MILLIMETER  # Use millimiter units (for depth measurements, available METER, CENTIMITERS, INCH, FOOT)
    
    #init_params.depth_maximum_distance = 100
    init_params.coordinate_system=sl.COORDINATE_SYSTEM.IMAGE # Standard coordinate system
    init_params.camera_resolution = sl.RESOLUTION.HD720 # Image Resolution (HD2K, HD1080, HD720, SVGA, VGA)
    init_params.camera_fps = 30

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Create and set RuntimeParameters after opening the camera
    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.confidence_threshold = 100
    runtime_parameters.texture_confidence_threshold = 100

    # Capture 150 images and depth, then stop
    image_L = sl.Mat()
    image_R = sl.Mat()
    depth_L = sl.Mat()
    point_cloud_L = sl.Mat()

    mirror_ref = sl.Transform()
    mirror_ref.set_translation(sl.Translation(2.75,4.0,0))
    tr_np = mirror_ref.m
        
    camera_model = zed.get_camera_information().camera_model
    res = sl.Resolution()
    res.width = image_L.get_width()
    res.height = image_L.get_height()
    
    # Create OpenGL viewer
    viewer = gl.GLViewer()
    viewer.init(1, sys.argv, camera_model, res)
        
    while viewer.is_available():
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_measure(point_cloud_L, sl.MEASURE.XYZRGBA,sl.MEM.CPU, res)
            viewer.updateData(point_cloud_L)
            if(viewer.save_data == True):
                point_cloud_to_save = sl.Mat()
                zed.retrieve_measure(point_cloud_to_save, sl.MEASURE.XYZRGBA, sl.MEM.CPU)
                err = point_cloud_to_save.write('test.ply')
                if(err == sl.ERROR_CODE.SUCCESS):
                    print("point cloud saved")
                else:
                    print("the point cloud has not been saved")
                viewer.save_data = False
    viewer.exit()

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()