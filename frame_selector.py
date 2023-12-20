import cv2
import os 
import glob

# Define input path
video_path = "D:\\MELA\\TestVideo_MOT"

video_files = glob.glob(os.path.join(video_path,"*.mp4"))

video_files = ["calib_no_audio.mp4"]

#video_path = "D:\\Siberian Jay\\jays on food.mp4"
dir_name = video_path
# Define image output path
#img_path = "D:\\Test Images\\v2i\\"

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


