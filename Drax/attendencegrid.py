from tkinter import *
import tkinter as tk
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

def change(emp):
    emp.configure(bg="green")

def update_attendance_status():
    workers = []

    # Fetch worker information from the database
    worker_data = db.reference('Workers').get()

    row = -1
    col = 0

    for worker_id, worker_info in worker_data.items():
        try:
            worker = tk.Label(att, text=worker_info['name'], bg="red", fg="white", font=("yu gothic ui SemiBold", 13))
            worker.grid(row=row+1, column=col, ipadx=10, ipady=10, sticky="nsew")
            worker.id = worker_id
            workers.append(worker)

            datetimeObject = datetime.strptime(worker_info['last_attendance_time'], "%Y-%m-%d %H:%M:%S")

            if datetimeObject.date() == datetime.today().date():
                change(worker)
            else:
                worker.configure(bg="red")

            col += 1

            if col % 4 == 0:
                row += 1
                col = 0

        except ValueError:
            print(f"Invalid column index: {worker_id}")

    # Configure grid weights
    for i in range(row+2):
        att.grid_rowconfigure(i, weight=1)
    for j in range(4):
        att.grid_columnconfigure(j, weight=1)

    # Schedule the next update after a certain interval (e.g., 1 minute)
    att.after(5000, update_attendance_status)


att = Tk()
att.title('Attendance List')

# Get screen dimensions
screen_width = att.winfo_screenwidth()
screen_height = att.winfo_screenheight()

# Set window dimensions and position
width = 1400
height = 730
x = (screen_width - width) // 2
y = (screen_height - height) // 4
att.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Initialize Firebase app
cred = credentials.Certificate("serviceaccountkey.json")
firebase_admin.initialize_app(cred, name='attendance-app', options={
    'databaseURL': "https://faceattendance-e1faf-default-rtdb.firebaseio.com/Workers/0",
    'storageBucket': "faceattendance-e1faf.appspot.com"
})

update_attendance_status()

# Delete Firebase app when Tkinter window is closed
def on_closing():
    firebase_admin.delete_app(firebase_admin.get_app(name='attendance-app'))
    att.destroy()

att.protocol("WM_DELETE_WINDOW", on_closing)
att.resizable(False, False)
att.mainloop()
