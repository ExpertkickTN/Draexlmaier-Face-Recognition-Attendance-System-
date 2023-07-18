import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials, storage

# Initialize the Firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceaccountkey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://faceattendance-e1faf-default-rtdb.firebaseio.com/Workers/0",
        'storageBucket': "faceattendance-e1faf.appspot.com"
    })

# Import workers' images
folderPath = 'Resources'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
workerId = []

bucket = storage.bucket()

for path in pathList:
    img = cv2.imread(os.path.join(folderPath, path))
    imgList.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    workerId.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(workerId)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, workerId]
print("Encoding Complete")

with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)
print("File Saved")

# Upload EncodeFile.p to Firebase storage bucket
encodeFileBlob = bucket.blob('EncodeFile.p')
encodeFileBlob.upload_from_filename('EncodeFile.p')
print("EncodeFile.p uploaded to Firebase storage bucket.")