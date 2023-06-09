import sys

sys.argv = ['']
del sys
from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Age and Gender Detection")
w = Label(root, text="Age and gender detection", background='black', foreground='white', font='22')
w.pack()
T = Text(root, height=20, width=100)
T.pack()

import cv2
import math
import argparse


def close_window():
    if messagebox.askokcancel("Camera Access Permission", "Do you want to open your camera"):
        def highlightFace(net, frame, conf_threshold=0.7):
            frameOpencvDnn = frame.copy()
            frameHeight = frameOpencvDnn.shape[0]
            frameWidth = frameOpencvDnn.shape[1]
            blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

            net.setInput(blob)
            detections = net.forward()
            faceBoxes = []
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > conf_threshold:
                    x1 = int(detections[0, 0, i, 3] * frameWidth)
                    y1 = int(detections[0, 0, i, 4] * frameHeight)
                    x2 = int(detections[0, 0, i, 5] * frameWidth)
                    y2 = int(detections[0, 0, i, 6] * frameHeight)
                    faceBoxes.append([x1, y1, x2, y2])
                    cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
            return frameOpencvDnn, faceBoxes

        parser = argparse.ArgumentParser()
        parser.add_argument('--image')

        args = parser.parse_args()

        faceProto = "opencv_face_detector.pbtxt"
        faceModel = "opencv_face_detector_uint8.pb"
        ageProto = "age_deploy.prototxt"
        ageModel = "age_net.caffemodel"
        genderProto = "gender_deploy.prototxt"
        genderModel = "gender_net.caffemodel"

        MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
        genderList = ['Male', 'Female']

        faceNet = cv2.dnn.readNet(faceModel, faceProto)
        ageNet = cv2.dnn.readNet(ageModel, ageProto)
        genderNet = cv2.dnn.readNet(genderModel, genderProto)
        # video = cv2.imread('girl1.png')
        video = cv2.VideoCapture(args.image if args.image else 0)
        padding = 20
        while cv2.waitKey(1) < 0:
            hasFrame, frame = video.read()
            if not hasFrame:
                cv2.waitKey()
                break

            resultImg, faceBoxes = highlightFace(faceNet, frame)
            if not faceBoxes:
                print("No face detected")

            for faceBox in faceBoxes:
                face = frame[max(0, faceBox[1] - padding):
                             min(faceBox[3] + padding, frame.shape[0] - 1), max(0, faceBox[0] - padding)
                                                                            :min(faceBox[2] + padding,
                                                                                 frame.shape[1] - 1)]
                blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                genderNet.setInput(blob)
                genderPreds = genderNet.forward()
                gender = genderList[genderPreds[0].argmax()]
                print(f'Gender: {gender}')

                ageNet.setInput(blob)
                agePreds = ageNet.forward()
                age = ageList[agePreds[0].argmax()]
                print(f'Age: {age[1:-1]} years')

                cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow("Detecting age and gender", resultImg)


btn1 = Button(root, text="Video Capture", command=close_window, background='maroon', foreground='white', font='24')
btn1.pack(pady=20)


def high():
    def highlightFace(net, frame, conf_threshold=0.7):
        frameOpencvDnn = frame.copy()
        frameHeight = frameOpencvDnn.shape[0]
        frameWidth = frameOpencvDnn.shape[1]
        blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

        net.setInput(blob)
        detections = net.forward()
        faceBoxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                faceBoxes.append([x1, y1, x2, y2])
                cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
        return frameOpencvDnn, faceBoxes

    parser = argparse.ArgumentParser()
    parser.add_argument('--image')

    args = parser.parse_args()

    faceProto = "opencv_face_detector.pbtxt"
    faceModel = "opencv_face_detector_uint8.pb"
    ageProto = "age_deploy.prototxt"
    ageModel = "age_net.caffemodel"
    genderProto = "gender_deploy.prototxt"
    genderModel = "gender_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList = ['Male', 'Female']

    faceNet = cv2.dnn.readNet(faceModel, faceProto)
    ageNet = cv2.dnn.readNet(ageModel, ageProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)
    # video = cv2.imread('girl1.jpg')
    # video=input("Enter Your Image")
    v = input("Enter your image name")

    video = cv2.VideoCapture(v)

    # video=cv2.VideoCapture(args.image if args.image else 0)
    padding = 20
    while cv2.waitKey(1) < 0:
        hasFrame, frame = video.read()
        if not hasFrame:
            cv2.waitKey()
            break

        resultImg, faceBoxes = highlightFace(faceNet, frame)
        if not faceBoxes:
            print("No face detected")

        for faceBox in faceBoxes:
            face = frame[max(0, faceBox[1] - padding):
                         min(faceBox[3] + padding, frame.shape[0] - 1), max(0, faceBox[0] - padding)
                                                                        :min(faceBox[2] + padding, frame.shape[1] - 1)]

            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]

            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            age = ageList[agePreds[0].argmax()]

            cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("Detecting age and gender", resultImg)


T.insert(END,
         '1. Upload Your image then age and gender will be detected                                           2. Or Give access your camera then age and gender will be detected')
exit_button = Button(root, text="Upload Image", command=high, background='maroon', foreground='white', font='24')
exit_button.pack(pady=20)
mainloop()