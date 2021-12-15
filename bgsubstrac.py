from __future__ import print_function
import cv2 as cv

#Initial
backSub = cv.createBackgroundSubtractorMOG2()
backSub.setVarThreshold(100)
capture = cv.VideoCapture('videojalan.mp4')
jml_car=0
hold=0

if not capture.isOpened():
    print('Unable to open: ' + args.input)
    exit(0)

while True:
    ret, frame = capture.read()
    if frame is None:
        break

    fgMask = backSub.apply(frame)
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    
    #Crop Gambar
    crop=fgMask[150:350, 180:380]
    for i in range (0,100):
        for j in range (100,i,-1):
            crop[i, 100-j] = 0

    #Hitung Blob
    output=cv.connectedComponentsWithStats(crop,8,cv.CV_32S)
    (jml_label, label, stats, centroid)=output
    jml_blob=0

    #Menghitung Kendaraan
    for i in range(0,jml_label) :
        if stats[i,cv.CC_STAT_AREA]>350 :
            jml_blob = jml_blob+1
    if hold==0 and jml_blob>2 :
        jml_car = jml_car+1
        hold = 1
    elif hold==1 and jml_blob<=1 :
        hold = 0
        
    #hasil    
    cv.imshow('Frame', frame)
    cv.imshow('crop', crop)
    print("Jumlah Blob=",jml_blob)
    print("Jumlah Kendaraan=",jml_car)
    
    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
