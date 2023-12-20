# Aruco calibration : Not can be done 

import cv2
import cv2.aruco as aruco
import numpy as np
from tqdm import tqdm

def calibrate_camera(video_path, output_file):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video is opened successfully
    if not cap.isOpened():
        print(f"Error: Unable to open video file '{video_path}'")
        return

    aruco_dict = aruco.Dictionary(aruco.DICT_6X6_250,43)
    parameters = aruco.DetectorParameters()

    all_corners = []
    all_ids = []

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for _ in tqdm(range(total_frames), desc="Processing frames"):
        # Read a frame from the video
        ret, frame = cap.read()

        # Break the loop if the video is finished
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect ArUco markers
        corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
            all_corners.append(corners)
            all_ids.append(ids)

    # Release the video capture object
    cap.release()

    # Perform camera calibration
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    calibration_flags = cv2.CALIB_FIX_PRINCIPAL_POINT + cv2.CALIB_FIX_ASPECT_RATIO + cv2.CALIB_ZERO_TANGENT_DIST

    _, camera_matrix, dist_coeffs, _, _ = cv2.aruco.calibrateCameraAruco(
        all_corners, all_ids, aruco_dict, (gray.shape[1], gray.shape[0]), None, None,
        criteria=criteria, flags=calibration_flags
    )

    # Save the calibration parameters
    np.savez(output_file, camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)
    print(f"Camera calibration parameters saved to {output_file}")

if __name__ == "__main__":
    # Specify the path to your video file
    input_video_path = "calibration_sequence.mp4"

    # Specify the output file for calibration parameters
    output_calibration_file = "calibration_parameters.npz"

    # Call the function to calibrate the camera using ArUco markers
    calibrate_camera(input_video_path, output_calibration_file)
