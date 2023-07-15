import sqlite3
import re
from tkinter import *
from tkinter import messagebox
import random
import string
AccountSystem = Tk()
AccountSystem.rowconfigure(0, weight=1)
AccountSystem.columnconfigure(0, weight=1)
height = 650
width = 1240
AccountSystem.geometry('985x585')
AccountSystem.title('Face Recognition Attendance Management System')
#AccountSystem.iconbitmap("assets/ico.ico")
sign_in = Frame(AccountSystem)
sign_up = Frame(AccountSystem)
pass_forgot = Frame(AccountSystem)

for frame in (sign_up, sign_in, pass_forgot):
    frame.grid(row=0, column=0, sticky='nsew')

def clear():
        LastName.set("")
        FirstName.set("")
        Password.set("")
        ConfirmPassword.set("")
        Email.set("")
        Emailfor.set("")


def forgot_password():

    # Generate a random password
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # Connect to the database
    connection = sqlite3.connect("Database/AccountSystem.db")
    cursor = connection.cursor()

    # Check if the email exists in the AccountDB table
    cursor.execute("SELECT * FROM AccountDB WHERE Email = ?", (emailfor_entry.get(),))
    result = cursor.fetchone()

    if result:
        # Insert the email and new password into the PASSFORGOT table
        cursor.execute("INSERT INTO PASSFORGOT (Email, NewPassword) VALUES (?, ?)", (emailfor_entry.get(), new_password))
        connection.commit()
        connection.close()
        messagebox.showinfo('Success', 'Password reset successful. Please check your email for the new password.')
        clear()
    else:
        messagebox.showerror('Error', 'Invalid email. Please enter a valid email address.')

def loginpage():
    AccountSystem.destroy()
    import interface


def show_frame(frame):
    frame.tkraise()

show_frame(sign_up)
# ==========================signup page ==========================================
FirstName = StringVar()
LastName = StringVar()
Email = StringVar()
Emailfor = StringVar()
Password = StringVar()
ConfirmPassword = StringVar()



# ================Background Image ====================
backgroundImage = PhotoImage(file="assets\\image_1.png")
bg_image = Label(
    sign_up,
    image=backgroundImage,
    bg="#525561"
)
bg_image.place(x=-5, y=-10)

# ================ Header Text Left ====================
headerText_image_left = PhotoImage(file="assets\\work-icon.png")
headerText_image_label1 = Label(
    bg_image,
    image=headerText_image_left,
    bg="#272A37"
)
headerText_image_label1.place(x=60, y=45)

headerText1 = Label(
    bg_image,
    text="DRÄXLMAIER",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
headerText1.place(x=110, y=45)

# ================ Header Text Right ====================


headerText2 = Label(
    bg_image,
    anchor="nw",
    text="Attendance System",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 20 * -1),
    bg="#2c2e3a"
)
headerText2.place(x=732, y=300)

# ================ CREATE ACCOUNT HEADER ====================
createAccount_header = Label(
    bg_image,
    text="Create New Account",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 28 * -1),
    bg="#272A37"
)
createAccount_header.place(x=75, y=121)

# ================ ALREADY HAVE AN ACCOUNT TEXT ====================
text = Label(
    bg_image,
    text="Already have an account ?",
    fg="#FFFFFF",
    font=("yu gothic ui Regular", 15 * -1),
    bg="#272A37"
)
text.place(x=75, y=187)

# ================ GO TO LOGIN ====================
switchLogin = Button(
    bg_image,
    text="Login",
    fg="#206DB4",
    font=("yu gothic ui Bold", 15 * -1),
    bg="#272A37",
    bd=0,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff",
    command=lambda: show_frame(sign_in)
)
switchLogin.place(x=250, y=183, width=50, height=35)

# ================ First Name Section ====================
firstName_image = PhotoImage(file="assets\\input_img.png")
firstName_image_Label = Label(
    bg_image,
    image=firstName_image,
    bg="#272A37"
)
firstName_image_Label.place(x=80, y=242)

firstName_text = Label(
    firstName_image_Label,
    text="First name",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
firstName_text.place(x=25, y=0)

firstName_icon = PhotoImage(file="assets\\name_icon.png")
firstName_icon_Label = Label(
    firstName_image_Label,
    image=firstName_icon,
    bg="#3D404B"
)
firstName_icon_Label.place(x=159, y=15)

firstName_entry = Entry(
    firstName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    fg='#FFFFFF',
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=FirstName
)
firstName_entry.place(x=8, y=17, width=140, height=27)

# ================ Last Name Section ====================
lastName_image = PhotoImage(file="assets\\input_img.png")
lastName_image_Label = Label(
    bg_image,
    image=lastName_image,
    bg="#272A37"
)
lastName_image_Label.place(x=293, y=242)

lastName_text = Label(
    lastName_image_Label,
    text="Last name",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
lastName_text.place(x=25, y=0)

lastName_icon = PhotoImage(file="assets\\name_icon.png")
lastName_icon_Label = Label(
    lastName_image_Label,
    image=lastName_icon,
    bg="#3D404B"
)
lastName_icon_Label.place(x=159, y=15)

lastName_entry = Entry(
    lastName_image_Label,
    bd=0,
    fg='#FFFFFF',
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=LastName
)
lastName_entry.place(x=8, y=17, width=140, height=27)

# ================ Email Name Section ====================
emailName_image = PhotoImage(file="assets\\email.png")
emailName_image_Label = Label(
    bg_image,
    image=emailName_image,
    bg="#272A37"
)
emailName_image_Label.place(x=80, y=311)

emailName_text = Label(
    emailName_image_Label,
    text="Email ",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
emailName_text.place(x=25, y=0)

emailName_icon = PhotoImage(file="assets\\email-icon.png")
emailName_icon_Label = Label(
    emailName_image_Label,
    image=emailName_icon,
    bg="#3D404B"
)
emailName_icon_Label.place(x=370, y=15)

emailName_entry = Entry(
    emailName_image_Label,
    bd=0,
    bg="#3D404B",
    fg='#FFFFFF',
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=Email
)
emailName_entry.place(x=8, y=17, width=354, height=27)

# ================ Password Name Section ====================
passwordName_image = PhotoImage(file="assets\\input_img.png")
passwordName_image_Label = Label(
    bg_image,
    image=passwordName_image,
    bg="#272A37"
)
passwordName_image_Label.place(x=80, y=380)

passwordName_text = Label(
    passwordName_image_Label,
    text="Password",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
passwordName_text.place(x=25, y=0)

passwordName_icon = PhotoImage(file="assets\\pass-icon.png")
passwordName_icon_Label = Label(
    passwordName_image_Label,
    image=passwordName_icon,
    bg="#3D404B"
)
passwordName_icon_Label.place(x=159, y=15)

passwordName_entry = Entry(
    passwordName_image_Label,
    bd=0,
    bg="#3D404B",
    fg='#FFFFFF',
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    show='.',
    textvariable=Password

)
passwordName_entry.place(x=8, y=17, width=140, height=27)

# ================ Confirm Password Name Section ====================
confirm_passwordName_image = PhotoImage(file="assets\\input_img.png")
confirm_passwordName_image_Label = Label(
    bg_image,
    image=confirm_passwordName_image,
    bg="#272A37"
)
confirm_passwordName_image_Label.place(x=293, y=380)

confirm_passwordName_text = Label(
    confirm_passwordName_image_Label,
    text="Confirm Password",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
confirm_passwordName_text.place(x=25, y=0)

confirm_passwordName_icon = PhotoImage(file="assets\\pass-icon.png")
confirm_passwordName_icon_Label = Label(
    confirm_passwordName_image_Label,
    image=confirm_passwordName_icon,
    bg="#3D404B"
)
confirm_passwordName_icon_Label.place(x=159, y=15)

confirm_passwordName_entry = Entry(
    confirm_passwordName_image_Label,
    bd=0,
    bg="#3D404B",
    fg='#FFFFFF',
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    show='.',
    textvariable=ConfirmPassword
)
confirm_passwordName_entry.place(x=8, y=17, width=140, height=27)

# =============== Submit Button ====================
submit_buttonImage = PhotoImage(
    file="assets\\button_1.png")
submit_button = Button(
    bg_image,
    image=submit_buttonImage,
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    activebackground="#272A37",
    cursor="hand2",
    command=lambda: signup()
)
submit_button.place(x=130, y=460, width=333, height=65)

# ================ Header Text Down ====================

headerText3 = Label(
    bg_image,
    text="",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
headerText3.place(x=700, y=530)




def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False


# ==================Data base connection ==================
def signup():
    if firstName_entry.get() == "" or lastName_entry.get() == "" or passwordName_entry.get() == "" or emailName_entry. \
            get() == "" or confirm_passwordName_entry.get() == "":
        messagebox.showerror('Error', "You must fill in all of the fields")

    elif passwordName_entry.get() != confirm_passwordName_entry.get():
        messagebox.showerror('Error', "Password and confirm password doesn't match")
    else:
        if (validate_email(emailName_entry.get()) == False):
            messagebox.showerror('Error', "Please enter a valid email address")
        else:
            try:
                connection = sqlite3.connect("Database/AccountSystem.db")
                cur = connection.cursor()
                find_user = 'SELECT * From AccountDB WHERE Email = ?'
                cur.execute(find_user, [(emailName_entry.get())])
                result = cur.fetchall()
                if result:
                    messagebox.showerror('Error', "User already registered")
                else:
                    cur.execute("INSERT INTO AccountDB(FirstName, LastName, Email, Password) VALUES(?,?,?,?)",
                                (firstName_entry.get(), lastName_entry.get(), emailName_entry.get(),
                                 passwordName_entry.get()))
                    connection.commit()
                    connection.close()
                    clear()
                    messagebox.showinfo('Success', "New account created successfully")
                    show_frame(sign_in)

            except Exception as es:
                messagebox.showerror('Error', "Something went wrong try again later")


# ========================== sign_in page ==========================================
email = StringVar()
password = StringVar()
sign_in.configure(bg="#525561")
# ===============Background Image ====================
Login_backgroundImage = PhotoImage(file="assets\\image_1.png")
bg_imageLogin = Label(
    sign_in,
    image=Login_backgroundImage,
    bg="#525561"
)
bg_imageLogin.place(x=-5, y=-10)

# ================ Header Text Left ====================
Login_headerText_image_left = PhotoImage(file="assets\\work-icon.png")
Login_headerText_image_label1 = Label(
    bg_imageLogin,
    image=Login_headerText_image_left,
    bg="#272A37"
)
Login_headerText_image_label1.place(x=60, y=45)

Login_headerText1 = Label(
    bg_imageLogin,
    text="DRÄXLMAIER",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
Login_headerText1.place(x=110, y=45)

Login_headerText2 = Label(
    bg_imageLogin,
    anchor="nw",
    text="Attendance System",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 20 * -1),
    bg="#2c2e3a"
)

Login_headerText2.place(x=732, y=300)

# ================ LOGIN TO ACCOUNT HEADER ====================
loginAccount_header = Label(
    bg_imageLogin,
    text="Login To Continue",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 28 * -1),
    bg="#272A37"
)
loginAccount_header.place(x=75, y=121)

# ================ NOT A MEMBER TEXT ====================
loginText = Label(
    bg_imageLogin,
    text="Don't have an account ?",
    fg="#FFFFFF",
    font=("yu gothic ui Regular", 15 * -1),
    bg="#272A37"
)
loginText.place(x=75, y=187)

# ================ GO TO SIGN UP ====================
switchSignup = Button(
    bg_imageLogin,
    text="Sign Up",
    fg="#206DB4",
    font=("yu gothic ui Bold", 15 * -1),
    bg="#272A37",
    bd=0,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff",
    command=lambda: show_frame(sign_up)
)
switchSignup.place(x=235, y=183, width=70, height=35)

# ================ Email Name Section ====================
Login_emailName_image = PhotoImage(file="assets\\email.png")
Login_emailName_image_Label = Label(
    bg_imageLogin,
    image=Login_emailName_image,
    bg="#272A37"
)
Login_emailName_image_Label.place(x=76, y=242)

Login_emailName_text = Label(
    Login_emailName_image_Label,
    text="Email",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
Login_emailName_text.place(x=25, y=0)

Login_emailName_icon = PhotoImage(file="assets\\email-icon.png")
Login_emailName_icon_Label = Label(
    Login_emailName_image_Label,
    image=Login_emailName_icon,
    bg="#3D404B"
)
Login_emailName_icon_Label.place(x=370, y=15)

Login_emailName_entry = Entry(
    Login_emailName_image_Label,
    bd=0,
    bg="#3D404B",
    fg='#FFFFFF',
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=email
)
Login_emailName_entry.place(x=8, y=17, width=354, height=27)

# ================ Password Name Section ====================
Login_passwordName_image = PhotoImage(file="assets\\email.png")
Login_passwordName_image_Label = Label(
    bg_imageLogin,
    image=Login_passwordName_image,
    bg="#272A37"
)
Login_passwordName_image_Label.place(x=80, y=330)

Login_passwordName_text = Label(
    Login_passwordName_image_Label,
    text="Password",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
Login_passwordName_text.place(x=25, y=0)

Login_passwordName_icon = PhotoImage(file="assets\\pass-icon.png")
Login_passwordName_icon_Label = Label(
    Login_passwordName_image_Label,
    image=Login_passwordName_icon,
    bg="#3D404B"
)
Login_passwordName_icon_Label.place(x=370, y=15)

Login_passwordName_entry = Entry(
    Login_passwordName_image_Label,
    bd=0,
    bg="#3D404B",
    fg='#FFFFFF',
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    show='.',
    textvariable=password
)
Login_passwordName_entry.place(x=8, y=17, width=354, height=27)

# =============== Submit Button ====================
Login_button_image_1 = PhotoImage(
    file="assets\\button_2.png")
Login_button_1 = Button(
    bg_imageLogin,
    image=Login_button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: login(),
    relief="flat",
    activebackground="#272A37",
    cursor="hand2",

)
Login_button_1.place(x=120, y=445, width=333, height=65)


# =====data base login=================================
def clear_login():
    email.set("")
    password.set("")


def login():
    if Login_emailName_entry.get() == "" or Login_passwordName_entry.get() == "":
        messagebox.showerror('Error', "All Fields Are Required")
    else:
        try:
            connection = sqlite3.connect("./Database/AccountSystem.db")
            cur = connection.cursor()
            find_user = 'SELECT * From AccountDB WHERE Email = ? and Password = ? '
            cur.execute(find_user, [(Login_emailName_entry.get()), Login_passwordName_entry.get()])

            result = cur.fetchall()
            if result:
                clear_login()
                messagebox.showinfo('Success', "Logged in Successfully")
                loginpage()
            else:
                messagebox.showerror('Error', "Sorry can't login, please try again")
            connection.commit()
            connection.close()
            clear()
        except Exception as es:
            print(es)
            messagebox.showerror('Error', "Something Wrong Try Again Later")


# ================ Forgot Password ====================
forgotPassword = Button(
    bg_imageLogin,
    text="Forgot Password ?",
    fg="#206DB4",
    font=("yu gothic ui Bold", 15 * -1),
    bg="#272A37",
    bd=0,
    activebackground="#272A37",
    activeforeground="#ffffff",
    cursor="hand2",
    command=lambda: show_frame(pass_forgot)
)
forgotPassword.place(x=210, y=400, width=150, height=35)

#=============================== forgot ==============
emailfor = StringVar()
pass_forgot.configure(bg="#525561")

forgot_backgroundImage = PhotoImage(file="assets\\image_1.png")
bg_imageforgot = Label(
    pass_forgot,
    image=forgot_backgroundImage,
    bg="#525561"
)
bg_imageforgot.place(x=-5, y=-10)
# ================ Header Text Left ====================
for_headerText_image_left = PhotoImage(file="assets\\work-icon.png")
for_headerText_image_label1 = Label(
    bg_imageforgot,
    image=for_headerText_image_left,
    bg="#272A37"
)
for_headerText_image_label1.place(x=60, y=45)

for_headerText1 = Label(
    bg_imageforgot,
    text="DRÄXLMAIER",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
for_headerText1.place(x=110, y=45)

for_headerText2 = Label(
    bg_imageforgot,
    anchor="nw",
    text="Attendance System",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 20 * -1),
    bg="#2c2e3a"
)

for_headerText2.place(x=732, y=300)

# ================ Forgot ACCOUNT HEADER ====================
forAccount_header = Label(
    bg_imageforgot,
    text="Forgot your password",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 28 * -1),
    bg="#272A37"
)
forAccount_header.place(x=75, y=121)

# ================ NOT A MEMBER TEXT ====================
forloginText = Label(
    bg_imageforgot,
    text="Please entre the email you'd like your new password sent to : ",
    fg="#FFFFFF",
    font=("yu gothic ui Regular", 15 * -1),
    bg="#272A37"
)
forloginText.place(x=75, y=187)
forloginText2 = Label(
    bg_imageforgot,
    text="Back to ",
    fg="#FFFFFF",
    font=("yu gothic ui Regular", 15 * -1),
    bg="#272A37"
)
forloginText2.place(x=225, y=380)
# ================ GO TO SIGN UP ====================
forswitchSignup = Button(
    bg_imageforgot,
    text="Sign Up",
    fg="#206DB4",
    font=("yu gothic ui Bold", 15 * -1),
    bg="#272A37",
    bd=0,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff",
    command=lambda: show_frame(sign_up)
)
forswitchSignup.place(x=278, y=376, width=70, height=35)


emailfor_image = PhotoImage(file="assets\\email.png")
emailfor_image_Label = Label(
    bg_imageforgot,
    image=emailfor_image,
    bg="#272A37"
)
emailfor_image_Label.place(x=80, y=230)

emailfor_text = Label(
    emailfor_image_Label,
    text="Email ",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
emailfor_text.place(x=25, y=0)

emailfor_icon = PhotoImage(file="assets\\email-icon.png")
emailfor_icon_Label = Label(
    emailfor_image_Label,
    image=emailName_icon,
    bg="#3D404B"
)
emailfor_icon_Label.place(x=370, y=15)

emailfor_entry = Entry(
    emailfor_image_Label,
    bd=0,
    bg="#3D404B",
    fg='#FFFFFF',
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=Emailfor
)
emailfor_entry.place(x=8, y=17, width=354, height=27)
submitfor_buttonImage = PhotoImage(file="assets\\submit.png")
submitfor_button = Button(
    bg_imageforgot,
    image=submitfor_buttonImage,
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    activebackground="#272A37",
    cursor="hand2",
    command=lambda: forgot_password()
)
submitfor_button.place(x=120, y=300, width=333, height=65)
AccountSystem.resizable(False, False)
AccountSystem.mainloop()
