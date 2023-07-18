from tkinter import filedialog
from tkinter import *
import time
import sqlite3
import matplotlib.pyplot as plt
import shutil
from tkinter import messagebox
from firebase_admin import db
from PIL import ImageTk, Image
from fpdf import FPDF
from datetime import datetime
import cv2
import face_recognition
import pickle
import sys
from io import BytesIO
import firebase_admin
from firebase_admin import credentials, storage
import os
import random
import string
import subprocess
import pygame
import pygame.camera
import argparse
token = None
email = None
parser = argparse.ArgumentParser()
parser.add_argument("--email", help="User's email")
parser.add_argument("--token", help="User's token")
args = parser.parse_args()
if args.email and args.token:
        email = args.email
        token = args.token
def generate_session_token(length=16):
        characters = string.ascii_letters + string.digits
        session_token = ''.join(random.choice(characters) for _ in range(length))
        return session_token
token1 = generate_session_token(16)
def camera():
    f1.destroy()
    messagebox.showinfo('Notice' ,'To close the face check window, please press Esc')
    command = [resource_path("main.exe"), "--token1", token1]
    subprocess.run(command)

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# Initialize the Firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate(resource_path("serviceaccountkey.json"))
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://faceattendance-e1faf-default-rtdb.firebaseio.com/Workers/0",
        'storageBucket': "faceattendance-e1faf.appspot.com"
    })

# ==========================add worker===========================

def train():

    folderPath = resource_path('Resources')
    pathList = os.listdir(folderPath)
    print(pathList)
    imgList = []
    workerId = []

    bucket = storage.bucket()

    for path in pathList:
        img = cv2.imread(os.path.join(folderPath, path))
        imgList.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        workerId.append(os.path.splitext(path)[0])

        fileName = f'{"Resources"}/{path}'
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

    with open(resource_path("EncodeFile.p"), 'wb') as file:
        pickle.dump(encodeListKnownWithIds, file)
    print("File Saved")

    # Upload EncodeFile.p to Firebase storage bucket
    encodeFileBlob = bucket.blob('EncodeFile.p')
    encodeFileBlob.upload_from_filename('EncodeFile.p')
    print("EncodeFile.p uploaded to Firebase storage bucket.")
    f1.destroy()
    firebase_admin.delete_app(firebase_admin.get_app())
    print("Firebase app closed.")

def clear():
    FirstName.set("")
    Idworker.set("")
    Year.set("")
    picture_name.set("")
    Idworker1.set("")

def savepdf():
    if not firebase_admin._apps:
        # Initialize the Firebase app
        cred2 = credentials.Certificate(resource_path("serviceaccountkey.json"))
        firebase_admin.initialize_app(cred2, {
            'databaseURL': "https://faceattendance-e1faf-default-rtdb.firebaseio.com/"
        })

    workers_ref = db.reference('Workers')
    workers_data = workers_ref.get()

    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()

    # Add header with logo, location, and date
    pdf.set_font("Arial", "B", 12)
    pdf.image(resource_path("assets/drax.png"), x=10, y=10, w=40)
    pdf.cell(0, 10, "DRÄXLMAIER Jammel", ln=True, align='C')
    pdf.cell(0, 10, f"Date: {datetime.today().strftime('%Y-%m-%d')}", ln=True, align='C')
    pdf.ln(20)

    # Set up table headers
    pdf.set_font("Arial", "B", 12)
    pdf.cell(70, 10, "ID", border=1)
    pdf.cell(50, 10, "Name", border=1)
    pdf.cell(60, 10, "Last Attendance Time", border=1)
    pdf.ln()

    # Add data to the table
    pdf.set_font("Arial", "", 12)
    if workers_data:
        for worker_id, worker_data in workers_data.items():
            datetimeObject = datetime.strptime(worker_data['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
            if datetimeObject.date() == datetime.today().date():  # Check if last attendance time is today
                pdf.cell(70, 10, worker_id, border=1)
                pdf.cell(50, 10, worker_data['name'], border=1)
                pdf.cell(60, 10, worker_data['last_attendance_time'], border=1)
                pdf.ln()

    # Save the PDF file
    pdf.output(resource_path("Reports/Attendance List Today.pdf"))
    messagebox.showinfo('Success', "Export completed successfully")
    f1.destroy()



def get_last_attendees_names():
    if not firebase_admin._apps:
        # Initialize the Firebase app
        cred = credentials.Certificate(resource_path("serviceaccountkey.json"))
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://faceattendance-e1faf-default-rtdb.firebaseio.com/"
        })

    ref = db.reference("Workers")
    worker_data = ref.get()

    last_attendees_names = []
    if worker_data:
        sorted_workers = sorted(worker_data.items(), key=lambda x: datetime.strptime(x[1].get('last_attendance_time', "0000-00-00 00:00:00"), "%Y-%m-%d %H:%M:%S"), reverse=True)
        current_time = datetime.now()
        for worker_id, worker_info in sorted_workers:
            attendance_time = datetime.strptime(worker_info.get('last_attendance_time', "0000-00-00 00:00:00"), "%Y-%m-%d %H:%M:%S")
            if attendance_time < current_time:
                last_attendees_names.append(worker_info['name'])
                if len(last_attendees_names) == 3:
                    break

    return last_attendees_names

def get_attendance_counts():
    if not firebase_admin._apps:
        # Initialize the Firebase app
        cred = credentials.Certificate(resource_path("serviceaccountkey.json"))
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://faceattendance-e1faf-default-rtdb.firebaseio.com/"
        })

    # Get a reference to the "Workers" node in your Firebase database
    ref = db.reference("Workers")

    # Initialize variables
    total = 0
    on_time = 0
    late = 0
    absent = 0

    # Retrieve worker data from Firebase
    worker_data = ref.get()

    if worker_data:
        # Iterate over the workers
        for worker_id, worker_info in worker_data.items():
            total += 1

            # Check if the worker has a last_attendance_time field
            if "last_attendance_time" in worker_info:
                last_attendance_time_str = worker_info["last_attendance_time"]

                # Convert last_attendance_time to a datetime object
                last_attendance_time = datetime.strptime(last_attendance_time_str, "%Y-%m-%d %H:%M:%S")

                # Check if last_attendance_time is equal to 8:00 am
                if last_attendance_time.time() <= datetime.strptime("8:00 am", "%I:%M %p").time() and last_attendance_time.date() == datetime.now().date():
                    on_time += 1
                # Check if last_attendance_time is greater than 8:00 am
                elif last_attendance_time.time() > datetime.strptime("8:00 am", "%I:%M %p").time() and last_attendance_time.date() == datetime.now().date():
                    late += 1

            # Check if last_attendance_time is not on the current date
            if last_attendance_time.date() != datetime.now().date():
                absent += 1
    return total, on_time, late, absent

# Call the function and retrieve the variables

def check_id(id):
    if len(id) < 8 or not id.isdigit():
        return False
    else:
        return True
def open_file():
    global picture_name  # Declare picture_name as a global variable
    USER_INP = emailName_entry.get()
    file_path = filedialog.askopenfilename()
    destination_directory = resource_path("Resources")

    file_name = os.path.basename(file_path)  # Extract the file name from the path
    file_name_with_extension = USER_INP + os.path.splitext(file_name)[1]
    destination_path = os.path.join(destination_directory, file_name_with_extension)

    # Store the file name in a StringVar
    picture_name = StringVar()
    picture_name.set(file_name)

    # Copying
    shutil.copy(file_path, destination_path)

    picture_name_label = Label(file_label, textvariable=picture_name, bg="#0F6470", fg="#FFFFFF",
                               font=("yu gothic ui SemiBold", 10), anchor="w" )
    picture_name_label.place(x=10, y=12 , width=300)

def take_and_save_picture():
    messagebox.showinfo("Notice","Click enter to take a picture")
    pygame.init()
    gameDisplay = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    icon_path = resource_path("assets/iconcamera.png")  # Replace with the path to your icon file
    icon_image = pygame.image.load(icon_path)
    pygame.display.set_icon(icon_image)
    pygame.camera.init()
    cam = pygame.camera.Camera(0, (1280, 720))
    pygame.display.set_caption("Camera")  # Set the window caption as "Camera"
    cam.start()
    USER_INP = emailName_entry.get()
    if USER_INP =='':
        cam.stop()
        pygame.quit()
        messagebox.showerror("Error", "You must fill in all of the fields")
    else:
        capturing = False
        save_path = resource_path(("Resources/"+str(USER_INP)+".png"))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cam.stop()
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    folder_name = os.path.dirname(save_path)
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)
                    img = cam.get_image()
                    pygame.image.save(img, save_path)
                    capturing = True

            if capturing:
                break

            img = cam.get_image()
            gameDisplay.blit(img, (0, 0))
            pygame.display.update()

        cam.stop()
        pygame.quit()
        messagebox.showinfo("Success", "Picture Saved")




def submit_del():
    if not firebase_admin._apps:
        # Initialize the Firebase app
        cred = credentials.Certificate(resource_path("serviceaccountkey.json"))
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://faceattendance-e1faf-default-rtdb.firebaseio.com/",
            'storageBucket': "faceattendance-e1faf.appspot.com"
        })

    if delete_entry.get() == "":
        messagebox.showerror('Error', "You must enter the worker's ID")
    else:
        worker_id = delete_entry.get()
        ref = db.reference('Workers')

        # Check if the worker exists in the database
        if ref.child(worker_id).get() is None:
            messagebox.showerror('Error', "Invalid ID Number")
        else:
            # Delete the worker from the database
            ref.child(worker_id).delete()
            bucket = storage.bucket()
            folder_name = 'Resources/'
            blobs = bucket.list_blobs(prefix=folder_name)
            # Find the image with the given worker ID
            for blob in bucket.list_blobs():
                if blob.name.endswith(worker_id + ".png") or blob.name.endswith(worker_id + ".jpg"):
                    blob.delete()
                    print(f"Image {blob.name} deleted successfully.")
                    # Delete the picture from the project folder
                    picture_path = os.path.join(resource_path('Resources'), worker_id + ".png")
                    if os.path.exists(picture_path):
                        os.remove(picture_path)
                        print(f"Image {worker_id}.png deleted from the project folder.")
                    picture_path = os.path.join(resource_path('Resources'), worker_id + ".jpg")
                    if os.path.exists(picture_path):
                        os.remove(picture_path)
                        print(f"Image {worker_id}.jpg deleted from the project folder.")
                    break

            messagebox.showinfo('Notice', "Worker deleted successfully, the window will freeze for about a minute to train the system correctly")
            train()
            clear()
            messagebox.showinfo('Success', "The system's training is complete. Thank you for your patience")
def submit():
    if not firebase_admin._apps:
        # Initialize the Firebase app
        cred = credentials.Certificate(resource_path("serviceaccountkey.json"))
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://faceattendance-e1faf-default-rtdb.firebaseio.com/"
        })

    if firstName_entry.get() == "" or emailName_entry.get() == "" or year_entry.get() == "":
        messagebox.showerror('Error', "You must fill in all of the fields")

    elif check_id((emailName_entry.get())) == TRUE:
        ref = db.reference('Workers')
        new_worker = {
            "name": firstName_entry.get(),
            "starting_year": int(year_entry.get()),
            "total_attendance": 0,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
        ref.child(emailName_entry.get()).update(new_worker)
        messagebox.showinfo('Notice', "New worker uploaded successfully, the window will freeze for about a minute to train the system correctly")
        train()
        clear()
        messagebox.showinfo('Success', "The system's training is complete. Thank you for your patience")
    else:
        messagebox.showerror('Error', "Invalide ID Number")

def check_login(token):
    if token is None:
        return False
    else:
        return True
admin = Tk()
if check_login(token)==False:
    # User is not logged in, display an error message and exit
    admin.destroy()
    sys.exit(1)

admin.rowconfigure(0, weight=1)
admin.columnconfigure(0, weight=1)
height = 650
width = 1240
x = (admin.winfo_screenwidth() // 2) - (width // 2)
y = (admin.winfo_screenheight() // 4) - (height // 4)
admin.geometry('985x585')
admin.title('Dashboard')
admin.configure(bg="#262a35")


addw = Frame(admin)
delw = Frame(admin)
nothing = Frame(admin)
for frame in (delw, nothing, addw):
    frame.grid(row=0, column=0, sticky='nsew')


def show_frame(frame):
    frame.tkraise()

def toggle_win():
    global f1
    global img2
    show_frame(nothing)


    def bttn(x, y, text, bcolor, fcolor, cmd):
        def on_entera(e):
            myButton1['background'] = bcolor  # ffcc66
            myButton1['foreground'] = '#FFFFFF'  # 000d33

        def on_leavea(e):
            myButton1['background'] = fcolor
            myButton1['foreground'] = '#262626'
        myButton1 = Button(f1, text=text,
                           width=65,
                           height=2,
                           fg='#262626',
                           border=0,
                           bg=fcolor,
                           activeforeground='#FFFFFF',
                           activebackground=bcolor,
                           cursor="hand2",
                           compound=LEFT,  # Place the icon on the left side of the text
                           command=cmd)
        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x, y=y)

    f1 = Frame(admin, width=260, height=500, bg='#FFFFFF')
    f1.place(x=0, y=0)
    bttn(-130, 80, 'A T T E N D E N C E   L I S T', '#000000', '#FFFFFF', lambda: list())
    bttn(-112, 117, 'A T T E N D E N C E   R E P O R T S', '#000000', '#FFFFFF', lambda: savepdf())
    bttn(-148, 154, 'E N R O L L M E N T', '#000000', '#FFFFFF', lambda: show_frame(addw))
    bttn(-136, 191, 'D I S E N R O L L M E N T', '#000000', '#FFFFFF', lambda: show_frame(delw))
    bttn(-145, 228, 'F A C E  C H E C K  ID', '#000000', '#FFFFFF', lambda:camera())
    bttn(-170, 464, 'L O G  O U T', '#000000', '#FFFFFF', lambda: logout())

    def dele():
        f1.destroy()
    img2 = ImageTk.PhotoImage(Image.open(resource_path("assets/icon close.png")))

    Button(f1,
           width=20,
           height=20,
           image=img2,
           border=0,
           cursor="hand2",
           command=dele,
           bg='#FFFFFF',
           activebackground='#FFFFFF').place(x=4, y=1)

#==========================delete worker===============================
Idworker1 = StringVar()

backgroundImage2 = PhotoImage(file=resource_path("assets\\image_2.png"))
bg_image2 = Label(
    delw,
    image=backgroundImage2,
    bg="#525561"
)
bg_image2.place(x=-5, y=-10)
img4 = ImageTk.PhotoImage(Image.open(resource_path("assets/openmenu.png")))
Button(delw, image=img4,
       command=toggle_win,
       border=0,
       cursor="hand2",
       bg='#0097ac',
       activebackground='#0097ac').place(x=4, y=1)
deleteworker_header = Label(
    bg_image2,
    text="Employee Disenrollment",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 28 * -1),
    bg="#0097AC"
)
deleteworker_header.place(x=75, y=121)

# ================ NOT A MEMBER TEXT ====================
deleteworkerText = Label(
    bg_image2,
    text="Please enter the worker's ID you would like to delete :  ",
    fg="#FFFFFF",
    font=("yu gothic ui Regular", 15 * -1),
    bg="#0097AC"
)
deleteworkerText.place(x=75, y=187)

delete_image = PhotoImage(file=resource_path("assets\\email.png"))
delete_image_Label = Label(
    bg_image2,
    image=delete_image,
    bg="#0097AC"
)
delete_image_Label.place(x=80, y=230)

delete_text = Label(
    delete_image_Label,
    text="Registration Number",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#0F6470"
)
delete_text.place(x=25, y=0)

delete_icon = PhotoImage(file=resource_path("assets\\id-card.png"))
delete_icon_Label = Label(
    delete_image_Label,
    image=delete_icon,
    bg="#0F6470"
)
delete_icon_Label.place(x=370, y=15)

delete_entry = Entry(
    delete_image_Label,
    bd=0,
    bg="#0F6470",
    fg='#FFFFFF',
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=Idworker1
)
delete_entry.place(x=8, y=21, width=354, height=20)
submitfor_buttonImage = PhotoImage(file=resource_path("assets\\submit.png"))
submitdel_button = Button(
    bg_image2,
    image=submitfor_buttonImage,
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    bg="#0097AC",
    activebackground="#0097AC",
    cursor="hand2",
    command=lambda: submit_del()
)
submitdel_button.place(x=120, y=300, width=333, height=65)
#=======================================================
headerText_image_left = PhotoImage(file=resource_path("assets\\work-icon.png"))
headerText_image_label2 = Label(
    bg_image2,
    image=headerText_image_left,
    bg="#0097AC"
)
headerText_image_label2.place(x=60, y=45)

headerText1 = Label(
    bg_image2,
    text="DRÄXLMAIER",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#0097AC"
)
headerText1.place(x=110, y=45)


# ======variables======
FirstName = StringVar()
Idworker = StringVar()
Year = StringVar()
picture_name = StringVar()


backgroundImage1 = PhotoImage(file=resource_path("assets\\image_1.png"))
bg_image = Label(
    addw,
    image=backgroundImage1,
    bg="#525561"
)
bg_image.place(x=-5, y=-10)


headerText_image_label1 = Label(
    bg_image,
    image=headerText_image_left,
    bg="#0097AC"
)
headerText_image_label1.place(x=60, y=45)

headerText1 = Label(
    bg_image,
    text="DRÄXLMAIER",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#0097AC"
)
headerText1.place(x=110, y=45)


createAccount_header = Label(
    bg_image,
    text="Employee Enrollment",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 28 * -1),
    bg="#0097AC"
)
createAccount_header.place(x=75, y=121)
addworkerText = Label(
    bg_image,
    text="Please fill in the employee details : ",
    fg="#FFFFFF",
    font=("yu gothic ui Regular", 15 * -1),
    bg="#0097AC"
)
addworkerText.place(x=75, y=187)

firstName_image = PhotoImage(file=resource_path("assets\\email.png"))
firstName_image_Label = Label(
    bg_image,
    image=firstName_image,
    bg="#0097AC"
)
firstName_image_Label.place(x=80, y=220)

firstName_text = Label(
    firstName_image_Label,
    text="Full Name",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#0F6470"
)
firstName_text.place(x=25, y=0)

firstName_icon = PhotoImage(file=resource_path("assets\\name_icon.png"))
firstName_icon_Label = Label(
    firstName_image_Label,
    image=firstName_icon,
    bg="#0F6470"
)
firstName_icon_Label.place(x=370, y=15)

firstName_entry = Entry(
    firstName_image_Label,
    bd=0,
    bg="#0F6470",
    highlightthickness=0,
    fg='#FFFFFF',
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=FirstName
)
firstName_entry.place(x=8, y=21, width=354, height=20)

emailName_image = PhotoImage(file=resource_path("assets\\email.png"))
emailName_image_Label = Label(
    bg_image,
    image=emailName_image,
    bg="#0097AC"
)
emailName_image_Label.place(x=80, y=285)

emailName_text = Label(
    emailName_image_Label,
    text="Registration Number",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#0F6470"
)
emailName_text.place(x=25, y=0)

emailName_icon = PhotoImage(file=resource_path("assets\\id-card.png"))
emailName_icon_Label = Label(
    emailName_image_Label,
    image=emailName_icon,
    bg="#0F6470"
)
emailName_icon_Label.place(x=370, y=15)

emailName_entry = Entry(
    emailName_image_Label,
    bd=0,
    bg="#0F6470",
    fg='#FFFFFF',
    justify='left',
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=Idworker
)
emailName_entry.place(x=8, y=21, width=354, height=20)

year_image = PhotoImage(file=resource_path("assets\\email.png"))
year_image_Label = Label(
    bg_image,
    image=year_image,
    bg="#0097AC"
)
year_image_Label.place(x=80, y=350)

year_text = Label(
    year_image_Label,
    text="Starting Year",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#0F6470"
)
year_text.place(x=25, y=0)

year_icon = PhotoImage(file=resource_path("assets\\date.png"))
year_icon_Label = Label(
    year_image_Label,
    image=year_icon,
    bg="#0F6470"
)
year_icon_Label.place(x=370, y=15)

year_entry = Entry(
    year_image_Label,
    bd=0,
    bg="#0F6470",
    fg='#FFFFFF',
    justify='left',
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=Year
)
year_entry.place(x=8, y=21, width=354, height=20)

file_image = PhotoImage(file=resource_path("assets\\email.png"))
file_label = Label(
    bg_image,
    image=file_image,
    bg="#0097AC"
)
file_label.place(x=80, y=415)

iconfolder = PhotoImage(file=resource_path("assets\\folder.png"))
iconcamera = PhotoImage(file=resource_path("assets\\camera.png"))
filefol = Button(
    file_label,
    image=iconfolder,
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    bg="#0F6470",
    activebackground="#0F6470",
    cursor="hand2",
    command=lambda: open_file()
)
filefol.place(x=370, y=15)
camerafol = Button(
    file_label,
    image=iconcamera,
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    bg="#0F6470",
    activebackground="#0F6470",
    cursor="hand2",
    command=lambda: take_and_save_picture()
)
camerafol.place(x=330, y=15)

submit_buttonImage = PhotoImage(file=resource_path("assets\\submit.png"))
submit_button = Button(
    bg_image,
    image=submit_buttonImage,
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    bg="#0097AC",
    activebackground="#0097AC",
    cursor="hand2",
    command=lambda: submit()
)
submit_button.place(x=120, y=485, width=333, height=65)


img3 = ImageTk.PhotoImage(Image.open(resource_path("assets/openmenu.png")))
Button(addw, image=img3,
       command=toggle_win,
       border=0,
       cursor='hand2',
       bg='#0097AC',
       activebackground='#0097AC').place(x=4, y=1)


# ================================================

backgroundImage = PhotoImage(file=resource_path("assets\\image_2.png"))
bg_image = Label(
    nothing,
    image=backgroundImage,
    bg="#525561"
)
# ================================================
bg_image.place(x=-5, y=-10)

def create_lastattendance_labels():
    last_attendees_names = get_last_attendees_names()
    work1_text.config(text=str(last_attendees_names[0]))
    work2_text.config(text=str(last_attendees_names[1]))
    work3_text.config(text=str(last_attendees_names[2]))
    nothing.after(10000, create_lastattendance_labels)
def create_attendance_labels():
    total_count, on_time_count, late_count, absent_count = get_attendance_counts()

    totalcal_text.config(text=str(total_count))
    ontimecal_text.config(text=str(on_time_count))
    latecal_text.config(text=str(late_count))
    abscal_text.config(text=str(absent_count))

    nothing.after(10000, create_attendance_labels)


# Create the labels initially
last_image = PhotoImage(file=resource_path("assets\\Component.png"))
total_image = PhotoImage(file=resource_path("assets\\total.png"))
late_image = PhotoImage(file=resource_path("assets\\late.png"))
abs_image = PhotoImage(file=resource_path("assets\\absent.png"))
ontime_image = PhotoImage(file=resource_path("assets\\ontime.png"))


graph_Label = Label(nothing, bg="#0097AC")
graph_Label.place(x=70, y=280)
def graph():
    def get_attendance_data():
        if not firebase_admin._apps:
            cred = credentials.Certificate(resource_path("serviceaccountkey.json"))
            firebase_admin.initialize_app(cred, {
                'databaseURL': "https://faceattendance-e1faf-default-rtdb.firebaseio.com/Workers/0",
                'storageBucket': "faceattendance-e1faf.appspot.com"
            })

        current_date = datetime.now().date().isoformat()

        workers_ref = db.reference('Workers')
        workers_data = workers_ref.get()

        attendance_count = 0
        total_employees = 0

        if workers_data:
            for worker_id, worker_data in workers_data.items():
                attendance_time = worker_data.get('last_attendance_time')
                if attendance_time:
                    date = attendance_time.split()[0]
                    if date == current_date:
                        attendance_count += 1
                total_employees += 1

        attendance_percentage = (attendance_count / total_employees) * 100
        absenteeism_percentage = 100 - attendance_percentage
        return attendance_percentage, absenteeism_percentage

    plt.close('all')
    attendance_percentage, absenteeism_percentage = get_attendance_data()

    fig = plt.figure(figsize=(4, 3), dpi=100, facecolor="#0097AC")
    ax = fig.add_subplot(111)
    ax.set_facecolor("#f7fafc")
    ax.pie(
        [absenteeism_percentage, attendance_percentage],
        autopct=lambda p: '{:.1f}%'.format(attendance_percentage) if p == 1 else '',
        colors=['#084F59', '#0F6470'],
        startangle=90,
        wedgeprops={'linewidth': 0.5},
        textprops={'color': 'white', 'fontsize': 9, 'family': 'Ubuntu'}
    )
    ax.axis('equal')

    # Convert the figure to a BytesIO object
    image_stream = BytesIO()
    fig.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Load the image from the BytesIO object
    graph_image = Image.open(image_stream)
    graph_image = ImageTk.PhotoImage(graph_image)

    # Update the label with the new graph image
    graph_Label.configure(image=graph_image)
    graph_Label.image = graph_image

    # Schedule the next update after 10 seconds
    nothing.after(10000, graph)
    return graph_image

# Create the label to display the graph image


def update_graph():
    graph_image = graph()
    graph_Label.configure(image=graph_image)
    graph_Label.image = graph_image

graph_Label.configure(image='')
update_graph()

todaytime_text = Label(nothing, text='',fg="#FFFFFF", bg="#0097AC", font=("yu gothic ui SemiBold", 14 * -1))
todaytime_text.place(x=700, y=250)
def update_time():
    current_time = str(time.strftime("%H:%M:%S %d %B %Y"))
    todaytime_text.config(text=current_time)
    nothing.after(1000, update_time)  # Update every 1000ms (1 second)
update_time()

# Create the label and display the graph image
datetoday = PhotoImage(file=resource_path("assets\\datetime.png"))
today_Label = Label(nothing, image=datetoday, bg="#0097AC")
today_Label.place(x=810, y=25)

todaycal_text = Label(today_Label, text='',fg="#FFFFFF", font=("yu gothic ui SemiBold", 13 * -1), bg="#0F6470")
todaycal_text.place(x=37, y=8)
def user():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(resource_path("Database/AccountSystem.db"))  # Replace "your_database_file.db" with your database file path

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Execute the SQL query to fetch the first name and last name of the user with the given ID
        cursor.execute("SELECT FirstName, LastName FROM AccountDB WHERE Email = ?", (email,))
        result = cursor.fetchone()

        if result:
            # If the user exists, return their first name and last name
            todaycal_text.configure(text=result)
        else:
            # If the user does not exist, return a default value (e.g., "Unknown User")
            return "Unknown", "User"
    except sqlite3.Error as e:
        print("Error accessing the database:", e)
        return "Unknown", "User"
    finally:
        # Close the database connection
        conn.close()

user()

last_Label = Label(nothing, image=last_image, bg="#0097AC")
last_Label.place(x=500, y=355)
#==================================images===============================

total_Label = Label(nothing, image=total_image, bg="#0097AC")
total_Label.place(x=95, y=40)

ontime_Label = Label(nothing, image=ontime_image, bg="#0097AC")
ontime_Label.place(x=300, y=40)

abs_Label = Label(nothing, image=abs_image, bg="#0097AC")
abs_Label.place(x=300, y=178)

late_Label = Label(nothing, image=late_image, bg="#0097AC")
late_Label.place(x=95, y=178)


totalcal_text = Label(total_Label, text="", fg="#FFFFFF", font=("yu gothic ui SemiBold", 20 * -1), bg="#0F6470")
totalcal_text.place(x=83, y=30)

ontimecal_text = Label(ontime_Label, text="", fg="#FFFFFF", font=("yu gothic ui SemiBold", 20 * -1), bg="#0F6470")
ontimecal_text.place(x=83, y=30)

latecal_text = Label(late_Label, text="", fg="#FFFFFF", font=("yu gothic ui SemiBold", 20 * -1), bg="#0F6470")
latecal_text.place(x=83, y=30)


abscal_text = Label(abs_Label, text="", fg="#FFFFFF", font=("yu gothic ui SemiBold", 20 * -1), bg="#0F6470")
abscal_text.place(x=83, y=30)
create_attendance_labels()

work1_text = Label(last_Label, text="", fg="#FFFFFF", font=("yu gothic ui SemiBold", 12 * -1), bg="#0F6470")
work1_text.place(x=45, y=52)
work2_text = Label(last_Label, text="", fg="#FFFFFF", font=("yu gothic ui SemiBold", 12 * -1), bg="#0F6470")
work2_text.place(x=45, y=84)
work3_text = Label(last_Label, text="", fg="#FFFFFF", font=("yu gothic ui SemiBold", 12 * -1), bg="#0F6470")
work3_text.place(x=45, y=116)


create_lastattendance_labels()

def list():
    f1.destroy()
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
                worker =Label(att, text=worker_info['name'], bg="red", fg="white",
                                  font=("yu gothic ui SemiBold", 13))
                worker.grid(row=row + 1, column=col, ipadx=10, ipady=10, sticky="nsew")
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
        for i in range(row + 2):
            att.grid_rowconfigure(i, weight=1)
        for j in range(4):
            att.grid_columnconfigure(j, weight=1)

        # Schedule the next update after a certain interval (e.g., 1 minute)
        att.after(5000, update_attendance_status)
    global att
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
    cred = credentials.Certificate(resource_path("serviceaccountkey.json"))
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

def add():
    f1.destroy()
    addw.tkraise()

def logout():
        admin.destroy()
        if att.winfo_exists():
            att.destroy()


# Create a Button
img1 = ImageTk.PhotoImage(Image.open(resource_path("assets/openmenu.png")))
Button(nothing, image=img1,
       command=toggle_win,
       border=0,
       bg='#0097ac',
       cursor="hand2",
       activebackground='#0097ac').place(x=4, y=1)




#icon = PhotoImage(file='assets/d.png')
#admin.iconphoto(False, icon)
# ================================================
admin.resizable(False, False)
admin.mainloop()
