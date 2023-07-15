import pickle
import numpy as np
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceaccountkey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-e1faf-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendance-e1faf.appspot.com"
})

bucket = storage.bucket()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # if you have a second camera, set the first parameter as 1
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

with open('EncodeFile.p', 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)

encodeListKnown, workerId = encodeListKnownWithIds
print("Encode File Loaded")

counter = 0
id = -1

while True:
    ret, frame = cap.read()
    imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = (x1, y1, x2 - x1, y2 - y1)
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (128, 128, 128), 2)
                id = workerId[matchIndex]

                if counter == 0:
                    cv2.imshow("Face Attendance", frame)
                    cv2.waitKey(1)
                    counter = 1

                if counter <= 10:
                    workerInfo = db.reference(f'Workers/{id}').get()
                    print(workerInfo)
                if workerInfo is not None:
                    datetimeObject = datetime.strptime(workerInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()

                    if secondsElapsed > 30:
                        ref = db.reference(f'Workers/{id}')
                        workerInfo['total_attendance'] += 1
                        ref.update({
                            'total_attendance': workerInfo['total_attendance'],
                            'last_attendance_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })

                    (w, h), _ = cv2.getTextSize(workerInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (bbox[2] - w) // 2
                    cv2.putText(frame, '['+str(workerInfo['name']+' '+str(id)+']'), (bbox[0] + offset, bbox[1] - 20),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 1)

                counter += 1

                if counter >= 20:
                    counter = 0
                    workerInfo = []

    else:
        counter = 0

    cv2.imshow("Face Attendance", frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()
firebase_admin.delete_app(firebase_admin.get_app())
