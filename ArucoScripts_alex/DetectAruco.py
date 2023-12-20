"""Test detect aruco QR code"""

import cv2
from cv2 import aruco
import numpy as np
import sys
import pickle

def draw_axis(img, R, t, K, dist):
    # unit is mm
    # rotV, _ = cv2.Rodrigues(R)
    points = np.float32([[20, 0, 0], [0, 20, 0], [0, 0, 20], [0, 0, 0]]).reshape(-1, 3)
    axisPoints, _ = cv2.projectPoints(points, R, t, K, dist)
    # import ipdb;ipdb.set_trace()

    Points = [(round(pt.ravel()[0]), round(pt.ravel()[1])) for pt in axisPoints]

    img = cv2.line(img, Points[3],  Points[0], (255,0,0), 10)
    img = cv2.line(img, Points[3],  Points[1], (0,255,0), 10)
    img = cv2.line(img, Points[3],  Points[2], (0,0,255), 10)
    return img

def CheckCodeDetection(aruco_dict,VidName):
    

    #read vid:
    cv2.namedWindow("Window", cv2.WINDOW_NORMAL)

    cap = cv2.VideoCapture(VidName)
    imsize = (int(cap.get(3)), int(cap.get(4)))

    counter=0
    cap.set(cv2.CAP_PROP_POS_FRAMES,counter) #Start reading frames from first flash
    # out = cv2.VideoWriter(filename="QRCode_Sample.mp4", apiPreference=cv2.CAP_FFMPEG, fourcc=cv2.VideoWriter_fourcc(*'mp4v'), fps=30, frameSize = imsize)
    # import ipdb;ipdb.set_trace()
    while(cap.isOpened()):
        print(counter)
        ret, frame = cap.read()
        if ret==True:
            ###Try change contast:
            alpha = 2
            beta = 0
            # frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # frame = gray.copy()



            corners,ids,_ = cv2.aruco.detectMarkers(gray,aruco_dict) #Detect aruco markers
            # import ipdb;ipdb.set_trace()
            
            for x in range(len(corners)):
                (topLeft, topRight, bottomRight, bottomLeft) = corners[x].tolist()[0]
                topRight = (round(topRight[0]), round(topRight[1]))
                bottomRight = (round(bottomRight[0]), round(bottomRight[1]))
                bottomLeft = (round(bottomLeft[0]), round(bottomLeft[1]))
                topLeft = (round(topLeft[0]), round(topLeft[1]))

                cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
                # cv2.putText(frame, str(ids[x][0]),
                #     (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                #     0.5, (0, 255, 0), 2)
                
                cv2.putText(frame, "TL",
                    (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
                cv2.putText(frame, "TR",
                    (topRight[0], topRight[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
                cv2.putText(frame, "BL",
                    (bottomLeft[0], bottomLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
                cv2.putText(frame, "BR",
                    (bottomRight[0], bottomRight[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
                
                #pose estimation
                ##Temp read an intrinsic file
                # cameraMatrix = np.identity(3)
                # distCoef = np.zeros(5)
                retCal, cameraMatrix, distCoef, rvecs, tvecs,pVErr,NewCamMat,roi= pickle.load(open("/media/alexchan/Extreme SSD/SampleDatasets/SiberianJays/Fieldwork2023/CalibrationTest/Data/Cam1_Intrinsic.p","rb"))


                rvec,tvec, ObjPoints = cv2.aruco.estimatePoseSingleMarkers(corners, 80 , cameraMatrix, distCoef)
                # import ipdb;ipdb.set_trace()
                for x in range(rvec.shape[0]):
                    Subrvec = rvec[x].ravel().reshape(3,1)
                    Subtvec = tvec[x].ravel().reshape(3,1)

                    # frame = draw_axis(frame, Subrvec, Subtvec, cameraMatrix,distCoef)
                    frame = cv2.drawFrameAxes(frame,cameraMatrix,distCoef,Subrvec,Subtvec,15,10)


                # try:
                #     frame = draw_axis(frame, rvec, tvec, cameraMatrix)
                #     # frame = cv2.drawFrameAxes(frame,cameraMatrix,distCoef,rvec,tvec, 0.01)
                # except:
                #     print("wow")



                
            cv2.imshow('Window',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            counter +=1
            # out.write(frame)
        else:
            break
    # out.release()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    VidPath = "/home/alexchan/Documents/MAAP3D-Greti/C0010.MP4"
    # VidPath = "/media/alexchan/Extreme SSD/SampleDatasets/QR_box.MP4"

    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)
    CheckCodeDetection(aruco_dict,VidPath)
