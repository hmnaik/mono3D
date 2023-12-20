#!/usr/bin/env python3

"""Check calibration board detection"""

import configparser
import cv2
from cv2 import aruco
import numpy as np
import scipy.stats as st
from tqdm import tqdm
import pickle
import sys



def CheckBoard(aruco_dict,board,VidName):


    #read vid:
    cv2.namedWindow("Window", cv2.WINDOW_NORMAL)

    cap = cv2.VideoCapture(VidName)
    counter=1350
    cap.set(cv2.CAP_PROP_POS_FRAMES,counter) #Start reading frames from first flash

    while(cap.isOpened()):
        print(counter)
        ret, frame = cap.read()
        if ret==True:
            
            # frame = cv2.flip(frame, 1)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            corners,ids,_ = cv2.aruco.detectMarkers(gray,aruco_dict) #Detect aruco markers
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

            if len(corners) >10:
                #Get subpixel detection for corners
                # for corner in corners:
                #     cv2.cornerSubPix(gray, corner, winSize = (3,3),zeroZone = (-1,-1),
                #     criteria = criteria)
                #interpolate markers
                response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
                markerCorners=corners,
                markerIds=ids,
                image=gray,
                board=board,
                minMarkers=1)
                # import ipdb;ipdb.set_trace()

                
                # print(charuco_corners)

                ###Temp, draw markers
                frame = aruco.drawDetectedCornersCharuco(
                image=gray,
                charucoCorners=charuco_corners,
                charucoIds=charuco_ids)


            cv2.imshow('Window',frame)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
            
            counter +=1
    cv2.destroyAllWindows()


# argv = [0,0,0]
# argv[1] = "Trials/ExtrinsicSandbox_Videos/SecondTest/C0004.MP4"
# argv[2] = "Config_Template.ini"


def main():
    VidName = "/media/alexchan/Elements/Vienna_Data/10202023/OutsideMeshTest/Videos/Cam1_C0040.MP4"

    CalibBoardDict = {
    "widthNum": 5,
    "lengthNum" : 10,
    "squareLen" : 55,
    "arucoLen" : 43,
    "ArucoDict" : aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    }


    # imsize = (int(config["basic"]["ImageLength"]),int(config["basic"]["ImageWidth"]))
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    board = aruco.CharucoBoard_create(int(CalibBoardDict["widthNum"]),
                                        int(CalibBoardDict["lengthNum"]),
                                        float(CalibBoardDict["squareLen"]),
                                        float(CalibBoardDict["arucoLen"]),aruco_dict)
    # imboard = board.draw((3023, 3779))
    # cv2.imwrite("Board.jpg",imboard)


    CheckBoard(aruco_dict,board,VidName)



if __name__ == "__main__":
	main()



