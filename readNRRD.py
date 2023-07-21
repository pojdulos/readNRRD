import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import json


SRC_ROOT = 'd:/darekp/PDDCA/'
DST_ROOT = 'output/'
REGION_DATA_FILE = 'via_region_data.json'

# True  - tworzy oddzielny podkatalog dla każdego modelu z własnym plikiem via_region_data.json
# False - zapisuje wszystko jak leci do DST_ROOT i tworzy jeden wspólny plik via_region_data.json
SEPARATE_SAMPLES = True

IMG_FORMAT = '.jpg' # mozna zapisywac do dowolnego formatu obsługiwanego przez cv2.imwrite()

# ZUUUUO: zmienna globalna ;-)
imgPrefix = '' # wartosć jest modyfikowana w funkcji processSample()


def getImgFileName(i):
    return f"{imgPrefix}_{i:03d}{IMG_FORMAT}"

def convertToJPG(srcFile, dstFolder):
    image = sitk.ReadImage(srcFile)
    image_array = sitk.GetArrayFromImage(image)

    if not os.path.exists(dstFolder):
       os.makedirs(dstFolder)

    for i in range(image_array.shape[0]):
        imgFile = getImgFileName(i)
        cv2.imwrite(os.path.join(dstFolder,imgFile), image_array[i, :, :])

def plotImage(image,contours):
    plt.imshow(image, cmap='gray', vmin=0, vmax=255 )

    for contour in contours:
        xs = [v[0][0] for v in contour]
        ys = [v[0][1] for v in contour]
        plt.plot(xs,ys,linewidth=1)
    plt.show()
    
def getRegionsObject(contours):
    cnt = 0
    result = {}
    for contour in contours:
        xs = [v[0][0] for v in contour]
        ys = [v[0][1] for v in contour]

        result[str(cnt)] = {
            'shape_attributes': {
                'name': "polygon",
                'all_points_x': np.array(xs).tolist(),
                'all_points_y': np.array(ys).tolist()
            },
            'region_attributes': {}
        }
        cnt += 1
    return result
    

def dumpRegionData(srcFile, dstFolder):
    image = sitk.ReadImage(srcFile)
    image_array = sitk.GetArrayFromImage(image)

    if not os.path.exists(dstFolder):
       os.makedirs(dstFolder)

    jsonFilePath = os.path.join(dstFolder, REGION_DATA_FILE)
    
    if SEPARATE_SAMPLES:
        jsonObject = {}
    else:   
        try:
            with open(jsonFilePath, "r") as file:
                jsonObject = json.load(file)
        except FileNotFoundError:
            jsonObject = {}

    for i in range(image_array.shape[0]):
        contours, _ = cv2.findContours(image_array[i, :, :], cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        imgFile = getImgFileName(i)
        imgFilePath = os.path.join(dstFolder,imgFile)
        imgFileSize = os.path.getsize(imgFilePath)

        jsonObject[f"{imgFile}{imgFileSize}"] = {
            'fileref': "",
            'size': imgFileSize,
            'filename': imgFile,
            'base64_img_data': "",
            'file_attributes': {},
            'regions': getRegionsObject(contours)
        }

        # opcjonalnie można sobie wyswietlić plastry z naniesionymi konturami
        # (jeli są), uwaga: mocno spowalnia działanie
        #plotImage(cv2.imread(imgFilePath,cv2.IMREAD_GRAYSCALE),contours)

    with open(jsonFilePath, "w") as file:
        json.dump(jsonObject, file)#, indent=2)
    

def processSample(sample):
    global imgPrefix
    
    srcFile = os.path.join(SRC_ROOT, sample, "img.nrrd")
    mandibleFile = os.path.join(SRC_ROOT, sample, "structures", "Mandible.nrrd")

    # przetwarzam tylko te modele w których jest wysegmentowana zuchwa
    if os.path.exists(srcFile) and os.path.exists(mandibleFile):
        imgPrefix = f"img{sample}"
        
        if SEPARATE_SAMPLES:
            dstDir = os.path.join(DST_ROOT, sample)
        else:
            dstDir = DST_ROOT
        
        convertToJPG(srcFile, dstDir)
        dumpRegionData(mandibleFile, dstDir)
    
    
def main():
    if not SEPARATE_SAMPLES:
        try:
            os.remove(os.path.join(DST_ROOT, REGION_DATA_FILE))
        except FileNotFoundError:
            pass

    for (dirpath, dirnames, filenames) in os.walk(SRC_ROOT):
        for sample in dirnames: #[0:3]:
            processSample(sample)
    

if __name__ == "__main__":
    main()
