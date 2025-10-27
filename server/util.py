import base64
import json
import numpy as np
import cv2
import joblib
from wavelet import w2d
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
parent_path = Path(__file__).resolve().parent.parent
__class_name_to_number = {}
__class_number_to_name = {}
__model = None

def load_saved_artifacts():
    ''' Load saved model artifacts'''
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name
    with open(parent_path / "model/class_dictionary.json", "r") as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v:k for k,v in __class_name_to_number.items()}
    global __model
    if __model is None:
        with open(parent_path / "model/trained_model.pkl", "rb") as f:
            __model = joblib.load(f)
    print("loading saved artifacts...done")

def classify_image(image_base64_data, file_path=None):
    ''' Classify the image'''
    imgs = get_cropped_image_if_2_eyes(file_path, image_base64_data)
    result = []
    for img in imgs:
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img, 'db1', 5)
        scalled_img_har = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((scalled_raw_img.reshape(32 * 32 * 3, 1), scalled_img_har.reshape(32 * 32, 1)))
        len_image_array = 32*32*3 + 32*32
        final = combined_img.reshape(1,len_image_array).astype(float)
        result.append({
            'class': __class_number_to_name[__model.predict(final)[0]],
            'class_probability': np.around(__model.predict_proba(final)*100,2).tolist()[0],
            'class_dictionary': __class_name_to_number
        })

    return result



def get_b64_image_for_virat():
    ''' Get the base64 string for virat image'''
    BASE_DIR = Path(__file__).resolve().parent  # .../Image_classification/server
    #print(BASE_DIR)
    with open(BASE_DIR / 'test_image/virat.txt') as f:
        return f.read()


def get_cv2_image_from_base64_string(b64str):
    ''' Convert a base64 string to a cv2 image'''
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_cropped_image_if_2_eyes(image_path, image_base64_data):
    ''' Crop the image if it has 2 eyes visible in image'''

    print(BASE_DIR)
    face_path = parent_path / "model" / "opencv" / "haarcascades" / "haarcascade_frontalface_default.xml"
    eye_path = parent_path / "model" / "opencv" / "haarcascades" / "haarcascade_eye.xml"
    face_cascade = cv2.CascadeClassifier(str(face_path))
    eye_cascade = cv2.CascadeClassifier(str(eye_path))
    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []
    for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if len(eyes) >= 2:
                cropped_faces.append(roi_color)
    return cropped_faces

if __name__ == "__main__":
    print('intialise......')
    load_saved_artifacts()
    print(classify_image(get_b64_image_for_virat()))