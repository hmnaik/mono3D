# This is useful for selection of the right images for calibration

# The current implementation is to save the images 

# It could be manipulated later to detect the checkerboard and detect the calibration and then allow the user to select or not. 


import cv2
import os 
import glob

# Define input path
# output_trimmed_video.MP4"
video_path = "D:\\Uganda_Calib\\"

video_files = glob.glob(os.path.join(video_path,"*.mp4"))

video_files = ["D:\\Uganda_Calib\\Test_Calib_1.MP4"]

dir_name = video_path

for file in video_files:
    print(f" Processing file:{file}")

    fileName = os.path.basename(file)
    fileName = fileName.split(".")[0]

    output_path = os.path.join(dir_name,fileName)
    output_path = os.path.abspath(output_path)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    ## Read video
    cap = cv2.VideoCapture(file)

    startLogging = False
    totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(f" Total frames : {totalFrames}")

    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == False:
            break

        # Display functions
        cv2.namedWindow("Test", cv2.WINDOW_NORMAL)
        cv2.imshow("Test",frame)

        # Get current frame no
        frame_no = cap.get(cv2.CAP_PROP_POS_FRAMES)
        #print(f"Frame : {frame_no}")

        # Start saving images if logging is enable
        if startLogging:
            imagePath = os.path.join(output_path, str(frame_no) + ".jpg")
            print(f"Image path:{imagePath}")
            cv2.imwrite( imagePath, frame )
            startLogging = False

        # Keyboard control
        k = cv2.waitKey(10)
        if k == ord('q'): #
            break

        if k == ord("s"):
            if startLogging:
                print ( "Logger Deactivated ")
                startLogging = False
            else:
                print("Logger Activated")
                startLogging = True

        if k == ord("j"): # Jumps 1000 Frames
            nextFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            newFrame = nextFrame + 1000
            if newFrame < totalFrames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, newFrame)
            continue

    cap.release()
    cv2.destroyAllWindows()


