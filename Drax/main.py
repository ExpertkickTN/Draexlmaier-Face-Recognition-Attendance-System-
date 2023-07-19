import pickle
import numpy as np
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
import yagmail
import sys
import winsound


token1 = None
for i in range(len(sys.argv)):
    if sys.argv[i] == "--token1" and i < len(sys.argv) - 1:
        token1 = sys.argv[i + 1]
        break
def play_sound():
    # The frequency and duration determine the sound played
    frequency = 1000  # Frequency in Hz (440 Hz is the musical note A4)
    duration = 1000  # Duration in milliseconds (1 second)
    winsound.Beep(frequency, duration)
def send_email(image_path):
    # Your email credentials
    email_sender = 'draxlmaierit@gmail.com'
    email_password = 'sbacgnrfkiodzgjy'

    # Compose the email
    subject = 'Alert: Unknown Person Detected'
    contents = 'The code could not recognize the face in the image.'
    attachments = [image_path]  # Attach the image of the unknown person

    # Send the email
    yag = yagmail.SMTP(email_sender, email_password)
    yag.send(to=email_sender, subject=subject, contents=contents, attachments=attachments)
    yag.close()


cred = credentials.Certificate("serviceaccountkey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-e1faf-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendance-e1faf.appspot.com"
})

bucket = storage.bucket()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # if you have a second camera, set the first parameter as 1
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

with open('EncodeFile.p', 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)

encodeListKnown, workerId = encodeListKnownWithIds
print("Encode File Loaded")

face_detected_count = 0
id = -1
known_face_encodings = []  # Track known face encodings

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

                # Increment the face_detected_count when a face is detected
                face_detected_count += 1

                if face_detected_count <= 10:
                    workerInfo = db.reference(f'Workers/{id}').get()


                # Check if the same face has been detected 1 or more times
                if face_detected_count > 1:
                    if workerInfo is not None:
                        datetimeObject = datetime.strptime(workerInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                        (w, h), _ = cv2.getTextSize(workerInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (bbox[2] - w) // 2
                        cv2.putText(frame, '[' + str(workerInfo['name'] + ' ' + str(id) + ']'),
                                    (bbox[0] + offset, bbox[1] - 20),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 1)
                        if  datetimeObject.date() == datetime.today().date():
                            print('already checked',workerInfo['name'])
                        else:
                            print(workerInfo)
                            ref = db.reference(f'Workers/{id}')
                            play_sound()
                            workerInfo['total_attendance'] += 1
                            ref.update({
                                'total_attendance': workerInfo['total_attendance'],
                                'last_attendance_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                    face_detected_count = 0  # Reset the face_detected_count after updating the attendance

            else:
                unknown_encoding = encodeFace
                matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
                if not any(matches):  # Unknown face
                    image_path = 'Unknown/unknown_person.jpg'  # Set the path where the image will be saved
                    cv2.imwrite(image_path, frame)  # Save the frame as an image
                    send_email(image_path)

                    known_face_encodings.append(unknown_encoding)

                if face_detected_count >= 20:
                    face_detected_count = 0
                    workerInfo = []

    else:
        face_detected_count = 0


    def check_interface(token1):
        if token1 is None:
            return True

        else:
            return True

    cv2.imshow("Face Attendance", frame)
    if check_interface(token1) == False:
        cap.release()
        cv2.destroyAllWindows()
        firebase_admin.delete_app(firebase_admin.get_app())
        sys.exit(1)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()
firebase_admin.delete_app(firebase_admin.get_app())
