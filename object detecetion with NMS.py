# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 23:31:58 2021

@author: Joel
"""

import cv2
import numpy as np


thres = 0.45 # Threshold to detect object
nms_threshold = 0.2
#img = cv2.imread('lena.png')

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150) # britness


classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')


configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)



while True:
    success, img = cap.read()
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    #print(classIds,bbox)
    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1,-1)[0])
    confs = list(map(float,confs))
    
    indices = cv2.dnn.NMSBoxes(bbox,confs,thres,nms_threshold)
    #print(indices)
    
    for i in indices:
        
        i = i[0]
        box = bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]
        cv2.rectangle(img, (x,y),(x+w,h+y), color=(0, 255, 0), thickness=2)
        cv2.putText(img,classNames[classIds[i][0]-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    
    
    
   
    
# =============================================================================
#     if len(classIds) != 0:
#             for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
#                 cv2.rectangle(img,box,color=(0,255,0),thickness=2)
#                 cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
#                             cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
#                 cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
#                             cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
#                 
# =============================================================================
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
