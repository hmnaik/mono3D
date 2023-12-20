"""Read mp file for mocap measured qrcode cube"""
import pickle
import os


def GetDict(MPFilePath,PointNames):
    
    file = open(MPFilePath)
    lines = [line.rstrip('\n') for line in file]
    points = []
    # Read point information from the file
    for line in lines:
        pointInfo = line.split("=")
        if (len(pointInfo) == 2):
            points.append(float(pointInfo[1]))

    OutDict = {}
    ObjCounter = 0
    # Store pattern information as list
    for i in range(0, len(points), 3):
        pt = [points[i], points[i + 1], points[i + 2]]
        OutDict[PointNames[ObjCounter]] = pt
        ObjCounter += 1

    return OutDict


if __name__ == "__main__":
    MPFilePath = "/media/alexchan/Extreme SSD/ExtrinsicSandbox/WorshopVids/SmallQR.mp"
    OutPath = "/media/alexchan/Extreme SSD/ExtrinsicSandbox/WorshopVids"
    PointNames = []
    for qrcode in range(6):
        for corner in ["TL","TR","BL","BR"]:
            PointNames.append("%s_%s"%(qrcode,corner))


    OutDict = GetDict(MPFilePath,PointNames)
    print(OutDict)
    
    ObjectDict = {"Pattern" : "Cube",
                  "ObjectPointDict" : OutDict}
    
    ObjectName = os.path.basename(MPFilePath).split(".")[0]

    pickle.dump(ObjectDict,open(os.path.join(OutPath, "%s.p"%ObjectName), "wb"))