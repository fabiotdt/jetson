import sys
import pyzed.sl as sl

# Create a ZED camera object
zed = sl.Camera()

# Set configuration parameters
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD1080
init_params.camera_fps = 30

err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
    exit()


# Get camera information (serial number)
zed_serial = zed.get_camera_information().serial_number
print("Hello! This is my serial number: {}".format(zed_serial))

# Grab an image
runtime_parameters = sl.RuntimeParameters()

# Capture 50 frames and stop
i = 0
image = sl.Mat()
runtime_parameters = sl.RuntimeParameters()
while i < 50:
    # Grab an image, a RuntimeParameters object must be given to grab()
    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        # A new image is available if grab() returns ERROR_CODE.SUCCESS
        zed.retrieve_image(image, sl.VIEW.LEFT) # Get the left image
        timestamp = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE)  # Get the image timestamp
        print("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(image.get_width(), image.get_height(), timestamp.get_milliseconds()))
        i = i + 1

# Create a ZED camera
zed = sl.Camera()
init_params = sl.InitParameters()
init_params.sdk_verbose = True # Enable verbose logging
init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE # Set the depth mode to performance (fastest)
init_params.coordinate_units = sl.UNIT.MILLIMETER  # Use millimeter units

# Open the camera
err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
    print("Error {}, exit program".format(err)) # Display the error
    exit()

# Close the camera
zed.close()
