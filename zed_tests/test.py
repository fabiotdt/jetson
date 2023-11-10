import cv2
import os
import numpy

# Use the correct device index for the ZED camera
cap = cv2.VideoCapture(2)  # Replace X with the correct device index "/dev/input/event19"
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)  # 1280
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    #print(frame.shape)
    if not ret:
        print("Error: Could not read frame.")
        break

    # Process the frame as needed
    left_right_image = numpy.split(frame, 2, axis=1)
    cv2.imshow("frame", frame)
    cv2.imshow("right", left_right_image[0])
    cv2.imshow("left", left_right_image[1])


    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
