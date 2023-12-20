import cv2
import numpy as np
import os

def detect_checkerboard(image_path):
    # Check if the image file exists
    if not os.path.isfile(image_path):
        print(f"Error: The specified image file '{image_path}' does not exist.")
        return

    # Load the image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Define the checkerboard size (number of inner corners)
    checkerboard_size = (13, 8)  # You can adjust this based on your checkerboard pattern

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)

    if ret:
        # Draw corners on the image
        cv2.drawChessboardCorners(img, checkerboard_size, corners, ret)

        # Save the image with drawn corners
        output_path = image_path.replace('.jpg', '_output.jpg')  # Modify the filename as needed
        cv2.imwrite(output_path, img)

        print(f"Checkerboard pattern detected. Output saved to: {output_path}")
    else:
        print("Checkerboard pattern not found in the image.")

if __name__ == "__main__":
    # Specify the path to your image
    #input_image_path = "C:\\Users\\naik\\ownCloud\\Chimp_work\\image_calib.jpg"
    
    input_image_path = "D:\\Uganda_Calib\\Test_Calib_1\\774.0.jpg"
    # Call the function to detect and draw on the checkerboard pattern
    detect_checkerboard(input_image_path)
