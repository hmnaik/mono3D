# The file detects the acu code in the image and prints things on it 

import cv2
import numpy as np
from os import path

# Function to detect ArUco markers in a frame
def detect_aruco_markers(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Load the predefined dictionary
    aruco_dict = cv2.aruco.Dictionary(cv2.aruco.DICT_6X6_50,80)

    # Initialize the ArUco parameters
    parameters = cv2.aruco.DetectorParameters()

    # Detect markers in the image
    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Draw the detected markers on the image
    frame_markers = cv2.aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    return frame_markers

# Open the video file
file_path = 'D:\\Science_Projects\\Siberian jay annotated dataset\\Aruco\\output_trimmed_video.mp4'

if path.exists(file_path):

    cap = cv2.VideoCapture(file_path)  # Replace 'your_video.mp4' with the path to your video file
    cv2.namedWindow('ArUco Marker Detection', cv2.WINDOW_NORMAL)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect ArUco markers in the frame
        frame_markers = detect_aruco_markers(frame)
        
        # Display the frame with detected markers
        cv2.imshow('ArUco Marker Detection', frame_markers)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

else:
    print("File not found.")