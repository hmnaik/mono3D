import cv2
import numpy as np
import argparse
import os

def detect_and_save_frame(video_path, output_video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video is opened successfully
    if not cap.isOpened():
        print(f"Error: Unable to open video file '{video_path}'")
        return

    frame_number = 0

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Break the loop if the video is finished
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Define the checkerboard size (number of inner corners)
        checkerboard_size = (13, 8)  # You can adjust this based on your checkerboard pattern

        # Set the size of the checkerboard squares in millimeters
        square_size_mm = 30.0
        # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)
        objp *= square_size_mm

        # Arrays to store object points and image points from all images
        obj_points = []  # 3D points in real world space
        img_points = []  # 2D points in image plane

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)
        totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        
        print(f"Frame number: {frame_number}")
        
        if ret:
            # Draw corners on the frame
            cv2.drawChessboardCorners(frame, checkerboard_size, corners, ret)

            # Save the frame with drawn corners
            output_file_name = f"frame_{frame_number}_output.jpg"  # Modify the filename as needed
            output = os.path.join( output_video_path, output_file_name) 
            cv2.imwrite(output, frame)
            print(f"Checkerboard pattern detected in frame {frame_number}. Frame saved to: {output}")
            #nextFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            frame_number = frame_number + 5000
            if frame_number < totalFrames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            continue
        else:
            frame_number = frame_number+ 100 
            if frame_number < totalFrames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            continue
            
    print("Finished all the frames.")
    # Release the video capture object
    cap.release()


def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="A simple script with argparse")

    # Add optional argument for input file
    parser.add_argument('--input', '-i', help='Input file path')

    # Add optional argument for output file
    parser.add_argument('--output', '-o', help='Output file path')

    # Parse command-line arguments
    args = parser.parse_args()

    # Perform some operation (for demonstration, just copying input to output)
    if args.input and args.output:
        try:
            os.path.exists(args.input)
            input_video_path = args.input
            output_video_path = args.output
        except FileNotFoundError:
            print("File not found. Please check the file paths.")
    else:
        print("Please provide both input and output file paths.")

    # Specify the path to your video file
    #input_video_path = "D:\\Uganda_Calib\\output_trimmed_video.MP4"

    # Call the function to detect and save frames with checkerboard pattern
    detect_and_save_frame(input_video_path, output_video_path)



if __name__ == "__main__":
    main()
