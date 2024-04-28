import cv2
import numpy as np
import urllib.request
import pyttsx3
import torch
from mss import mss

sct = mss()
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
url = 'http://192.168.137.160/cam-hi.jpg'
cap = cv2.VideoCapture(url)

engine = pyttsx3.init()

model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

while True:
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    im = cv2.imdecode(imgnp, -1)
    im=cv2.flip(im,0)
    sucess, img = cap.read()
    
    results = model(im)

    found_knife= False
    found_alcohol= False
    found_indecent= False
    found_gun= False
    found_cigarette= False
    found_blood= False

    for result in results.xyxy:
        labels = result[:, -1].numpy()
        bboxes = result[:, :4].numpy()
        confs = result[:, 4].numpy()

        for label, bbox, conf in zip(labels, bboxes, confs):
            label = int(label)
            x1, y1, x2, y2 = [int(val) for val in bbox]

            if model.names[label] == 'knife':
                found_knife = True
            elif model.names[label] == 'alcohol':
                found_alcohol = True
            elif model.names[label] == 'indecent':
                found_indecent = True
            elif model.names[label] == 'gun':
                found_gun = True
            elif model.names[label] == 'cigarette':
                found_cigarette = True
            elif model.names[label] == 'blood':
                found_blood = True
                

    if found_knife:
        engine.say("Alert! Knife Detected!")
        print("Alert! Knife Detected!")
        engine.runAndWait()

    elif found_alcohol:
        engine.say("Alert! Alcohol Detected!")
        engine.runAndWait()

    elif found_indecent:
        engine.say("Alert! Indecent Gesture Detected!")
        engine.runAndWait()
    
    elif found_gun:
        engine.say("Alert! Gun Detected!")
        engine.runAndWait()
    
    elif found_cigarette:
        engine.say("Alert! Cigarette Detected!")
        engine.runAndWait()
    
    elif found_blood:
        engine.say("Alert! Blood Detected!")
        engine.runAndWait()

    cv2.imshow('Image', im)
    cv2.waitKey(1)