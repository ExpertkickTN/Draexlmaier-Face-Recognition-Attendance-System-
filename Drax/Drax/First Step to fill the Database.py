import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

if not firebase_admin._apps:
    # Initialize the Firebase app
    cred = credentials.Certificate("serviceaccountkey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://faceattendance-e1faf-default-rtdb.firebaseio.com/"
    })

ref = db.reference('Workers')

data = {
    "321654":
        {
            "name": "Flen ben flen",
            "starting_year": 2017,
            "total_attendance": 7,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "852741":
        {
            "name": "Flen ben flen",
            "starting_year": 2017,
            "total_attendance": 7,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)