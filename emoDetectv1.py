# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:55:43 2021

@author: Ram
"""

import cv2

import tensorflow as tf

import os

tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(0)

import numpy as np

emo_model = tf.keras.models.load_model("SuccessModelv1")

face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

UPLOAD_FOLDER_IMAGE = "UserImage"


def emotion(path):

    #read image
    image = cv2.imread(os.path.join(UPLOAD_FOLDER_IMAGE, path))

    #Gray scales image 
    converted_image= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Detects face
    faces_detected = face_haar_cascade.detectMultiScale(converted_image)
    
    #for the last face found
    isFace = False
    noFace = 0
    predictions = [[0,0,0,0,0,0,0]]
    
    for (x,y,w,h) in faces_detected:
        isFace = True
        noFace += 1
        roi_gray=converted_image[y:y+w,x:x+h]
        roi_gray=cv2.resize(roi_gray,(48,48))
        image_pixels = tf.keras.preprocessing.image.img_to_array(roi_gray)
        image_pixels = np.expand_dims(image_pixels, axis = 0)
        image_pixels /= 255
        predictions[0] += emo_model.predict(image_pixels)[0]

    if isFace == False:
        return {"isFace":False}
    #prediction
    predictions[0] /= noFace

    max_index = np.argmax(predictions[0])

    #labelling
    emotion_detection = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    emotion_prediction = emotion_detection[max_index]

    mini = min(predictions[0])
    maxi = max(predictions[0])

    for j,i in enumerate(predictions[0]):
        print(predictions[0][j],end="\t")
        predictions[0][j] = round(( ( i - mini ) / (maxi-mini) )  * 100,2)
        print(predictions[0][j])

    sum=0

    for i in range(0,len(predictions[0])):
        sum += predictions[0][i]     
    print(predictions[0],sum)
 

    for i in range(0,len(predictions[0])):
        predictions[0][i]=round((predictions[0][i]/sum)*100,2) 


    print(predictions[0],sum)
    return {"isFace":isFace,"noFace":noFace,"predictions":predictions[0].tolist(),"emotion":emotion_prediction}


if __name__ == '__main__':

    print(emotion("test-happy6.jpg"))


