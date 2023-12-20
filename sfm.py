# SFM : Not used at the moment 

import cv2
import numpy as np

# Initialize ORB detector
orb = cv2.ORB_create()

# Create BFMatcher (Brute Force Matcher)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Initialize camera matrix (you need to provide your camera matrix)
K = np.array([[fx, 0, cx],
              [0, fy, cy],
              [0, 0, 1]])

# Initialize empty map
points_3d = np.empty((0, 3))
points_2d = np.empty((0, 2))

# Capture video frames
cap = cv2.VideoCapture('your_video.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detect ORB keypoints and descriptors
    kp, des = orb.detectAndCompute(frame, None)

    # Match features with the previous frame
    matches = bf.match(des_prev, des)
    
    # Extract matched keypoints
    pts1 = np.float32([kp_prev[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    pts2 = np.float32([kp[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Estimate essential matrix
    E, mask = cv2.findEssentialMat(pts2, pts1, K)

    # Recover pose
    _, R, t, mask = cv2.recoverPose(E, pts2, pts1, K)

    # Triangulate points
    points_4d = cv2.triangulatePoints(np.eye(3), np.hstack((R, t)), pts1.T, pts2.T)
    points_4d /= points_4d[3, :]

    # Filter out points with negative depth
    mask_positive_depth = (points_4d[2, :] > 0) & (mask.flatten() == 1)

    # Update the 3D map
    points_3d = np.vstack((points_3d, points_4d[:3, mask_positive_depth].T))
    points_2d = np.vstack((points_2d, pts2[mask_positive_depth].reshape(-1, 2)))

    # Update previous frame
    kp_prev, des_prev = kp, des

# Visualize the 3D map (optional)
# ...

# Release the video capture object
cap.release()
