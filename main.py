import customtkinter as ctk
import tkinter.messagebox as tkmb
from db_connection import *
from admin import admin_page
from student import student_page
from unidecode import unidecode
import time
import cv2
import face_recognition
import numpy as np

first_reg_no = 0

def login_form():
    global user_entry_fn, user_entry_ln, user_pass, checkbox_s, checkbox_a, root_main, frame_login

    root_main = ctk.CTk()
    root_main.geometry("500x550")
    root_main.minsize(height=550, width=500)
    root_main.title("Library Management System")
    
    label = ctk.CTkLabel(root_main, text="Welcome to \"Gheorghe Asachi\" Library of Iasi", font=('Comic Sans MS',18))
    label.pack(pady=20)

    frame_login = ctk.CTkFrame(master=root_main) 
    frame_login.pack(pady=20,padx=40,fill='both',expand=True) 

    label = ctk.CTkLabel(master=frame_login,text='LOGIN') 
    label.pack(pady=12,padx=10)

    user_entry_fn= ctk.CTkEntry(master=frame_login,placeholder_text="First Name") 
    user_entry_fn.pack(pady=12,padx=10) 

    user_entry_ln= ctk.CTkEntry(master=frame_login,placeholder_text="Last Name") 
    user_entry_ln.pack(pady=12,padx=10) 

    user_pass= ctk.CTkEntry(master=frame_login,placeholder_text="Password",show="*") 
    user_pass.pack(pady=12,padx=10)

    check_var_s = ctk.StringVar(value="on")
    checkbox_s = ctk.CTkCheckBox(master=frame_login, text='Student', onvalue="on", offvalue="off", variable=check_var_s, command=Chbx_s) 
    checkbox_s.pack(pady=12,padx=10)

    checkbox_a = ctk.CTkCheckBox(master=frame_login, text='Admin', onvalue="on", offvalue="off", command=Chbx_a) 
    checkbox_a.pack(pady=12,padx=10)

    button1 = ctk.CTkButton(master=frame_login, text='Login', command = Login, font=("Helvetica", 15))
    button1.pack(pady=12,padx=10)
    
    button2 = ctk.CTkButton(master=frame_login, command = face_rec_form, text="Face Recognition Login", cursor="hand2", width=200, height=35, fg_color="#003380", hover_color="#002966", font=("Helvetica", 15))
    button2.pack(pady=12,padx=10)
    
    root_main.protocol("WM_DELETE_WINDOW", close)
    root_main.mainloop()


def Login():
    
    err=0
    if not user_entry_fn.get() and not user_entry_ln.get() and not user_pass.get():
        tkmb.showerror(title="ERROR",message="Please complete the form!!")
        err=1
    elif user_entry_fn.get() and not user_entry_ln.get() and not user_pass.get():
        tkmb.showerror(title="ERROR",message="Please complete the \"Last Name\" and the \"Password\"!!")
        err=1
    elif not user_entry_fn.get() and user_entry_ln.get() and not user_pass.get():
        tkmb.showerror(title="ERROR",message="Please complete the \"First Name\" and the \"Password\"!!")
        err=1
    elif not user_entry_fn.get() and not user_entry_ln.get() and user_pass.get():
        tkmb.showerror(title="ERROR",message="Please complete the \"First Name\" and the \"Last Name\"!!")
        err=1
    elif user_entry_fn.get() and user_entry_ln.get() and not user_pass.get():
        tkmb.showerror(title="ERROR",message="Please complete the \"Password\"!!")
        err=1
    elif user_entry_fn.get() and not user_entry_ln.get() and user_pass.get():
        tkmb.showerror(title="ERROR",message="Please complete the \"Last name\"!!")
        err=1
    elif not user_entry_fn.get() and user_entry_ln.get() and user_pass.get():
        tkmb.showerror(title="ERROR",message="Please complete the \"First name\"!!")
        err=1
    elif checkbox_s.get() == "off" and checkbox_a.get() == "off":
        tkmb.showerror(title="ERROR",message="Please check a box!!")
        err=1
    
    find = 0
    if checkbox_s.get() == "on" and checkbox_a.get() == "off":
        cursor_s=conn.cursor()
        cursor_s.execute("select * from students where f_name = '" + user_entry_fn.get() + "' and l_name = '" + user_entry_ln.get() + "' and password = '" + user_pass.get() + "'")
        for i in cursor_s:
            if user_entry_fn.get() == i[1] and user_entry_ln.get() == i[2] and user_pass.get() == i[3] and checkbox_s.get() == "on" and checkbox_a.get() == "off":
                find = 1
                root_main.withdraw()
                student_page(i[1], i[2], i[4])
            elif user_entry_fn.get() == i[1] and user_entry_ln.get() == i[2] and user_pass.get() == i[3] and checkbox_s.get() == "off" and checkbox_a.get() == "on" and err==0:
                tkmb.showerror(title="ERROR",message="You are not an admin!!!")
                err=1
            elif (user_entry_fn.get() != i[1] and user_entry_ln.get() == i[2] and user_pass.get() == i[3] and err==0) or (user_entry_fn.get() == i[1] and user_entry_ln.get() != i[2] and user_pass.get() == i[3] and err==0) or (user_entry_fn.get() == i[1] and user_entry_ln.get() == i[2] and user_pass.get() != i[3] and err==0):
                tkmb.showerror(title="ERROR",message="Incorect data!!!")
                err=1
        cursor_s.close()
    elif checkbox_s.get() == "off" and checkbox_a.get() == "on":
        cursor_a=conn.cursor()
        cursor_a.execute("select * from admins where f_name = '" + user_entry_fn.get() + "' and l_name = '" + user_entry_ln.get() + "' and password = '" + user_pass.get() + "'")
        for i in cursor_a:
            if user_entry_fn.get() == i[1] and user_entry_ln.get() == i[2] and user_pass.get() == i[3] and checkbox_s.get() == "off" and checkbox_a.get() == "on":
                find = 1
                root_main.withdraw()
                admin_page(i[0], i[1], i[2])
            elif user_entry_fn.get() == i[1] and user_entry_ln.get() == i[2] and user_pass.get() == i[3] and checkbox_s.get() == "on" and checkbox_a.get() == "off" and err==0:
                tkmb.showerror(title="ERROR",message="You are not a student!!!")
                err=1
            elif (user_entry_fn.get() != i[1] and user_entry_ln.get() == i[2] and user_pass.get() == i[3] and err==0) or (user_entry_fn.get() == i[1] and user_entry_ln.get() != i[2] and user_pass.get() == i[3] and err==0) or (user_entry_fn.get() == i[1] and user_entry_ln.get() == i[2] and user_pass.get() != i[3] and err==0):
                tkmb.showerror(title="ERROR",message="Incorect data!!!")
                err=1
        cursor_a.close()
        
    if find==0 and err==0:
        tkmb.showerror(title="ERROR",message="DATA NOT FOUND!!!")
    
    
def Chbx_s():
    if checkbox_s.get() == "on":
        checkbox_a.deselect()

        
def Chbx_a():
    if checkbox_a.get() == "on":
        checkbox_s.deselect()
        
        
def face_rec_form():
    global checkbox_student, checkbox_admin, frame_face_rec, face_rec_btn, student_reg_no
    
    if user_entry_fn.winfo_ismapped():
        frame_login.pack_forget()
        
    frame_face_rec = ctk.CTkFrame(master=root_main)
    frame_face_rec.pack(pady=20,padx=40,fill='both',expand=True)
    
    back_btn = ctk.CTkButton(master=frame_face_rec, text="Back", command=back_button, width=60, height=20, fg_color="#29a329", hover_color="#248f24", cursor="hand2", font=("Helvetica", 12))
    back_btn.pack(pady=15,padx=15,side="top", anchor="w")
    
    checkbox_student = ctk.CTkCheckBox(master=frame_face_rec, text='Student', onvalue="on", offvalue="off", command = Checkbx_s) 
    checkbox_student.pack(pady=15,padx=15,side="top")
    
    student_reg_no= ctk.CTkEntry(master=frame_face_rec, placeholder_text="Registration Number") 
    student_reg_no.pack(pady=(0, 15),padx=15,side="top")

    checkbox_admin = ctk.CTkCheckBox(master=frame_face_rec, text='Admin', onvalue="on", offvalue="off", command = Checkbx_a) 
    checkbox_admin.pack(pady=15,padx=15,side="top")

    face_rec_btn = ctk.CTkButton(master=frame_face_rec, command=check_data, text="Scan Face", fg_color="#0073e6", hover_color="#0066cc", cursor="hand2", font=("Helvetica", 15))
    face_rec_btn.pack(pady=12, padx=10, side="top")
    
    
def Checkbx_s():
    if checkbox_student.get() == "on":
        checkbox_admin.deselect()


def Checkbx_a():
    if checkbox_admin.get() == "on":
        checkbox_student.deselect()
  
            
def check_data():
    if checkbox_student.get() == "off" and checkbox_admin.get() == "off":
        tkmb.showerror(title="Error", message="Check a box!")
    elif checkbox_student.get() == "on" and not student_reg_no.get() or not student_reg_no.get().isdigit():
        student_reg_no.configure(placeholder_text_color="red", text_color="red")
        student_reg_no.after(2000, lambda: student_reg_no.configure(placeholder_text_color="#737373", text_color="white"))
    elif checkbox_student.get() == "on" and student_reg_no.get():
        face_recognition_func("student")
    elif checkbox_admin.get() == "on":
        face_recognition_func("admin")
    
    
def face_recognition_func(person):
    admin_search = False
    student_search = False
    cursor = conn.cursor()
    
    if person == "admin":
        cursor.execute("select f_name, l_name, ID, picture from admins")
        admin_search = True
    elif person == "student":
        cursor.execute("select f_name, l_name, registration_number, picture from students where registration_number=" + student_reg_no.get())
        student_search = True
    
    student_face_encodings = []
    ids_reg_nums = []
    names = []

    for row in cursor:
        picture_np = np.frombuffer(row[3], np.uint8)
        picture = cv2.imdecode(picture_np, cv2.IMREAD_COLOR)
        encoding = face_recognition.face_encodings(picture)[0]

        student_face_encodings.append(encoding)
        ids_reg_nums.append(row[2])
        person_name = unidecode(row[1])+" "+unidecode(row[0])
        names.append(person_name)

    video_capture = cv2.VideoCapture(0)

    face_found = False
    start_time = None
    name_found = False
    start_time = time.time()

    while True:
        ret, frame = video_capture.read()

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        if len(face_locations) != 0:
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(student_face_encodings, face_encoding)
                    
                for match, id_reg_no, name in zip(matches, ids_reg_nums, names):
                    if match and face_found == False:
                        id_or_reg_no = id_reg_no
                        name_found = name
                        face_found = True
            
            if name_found != False:            
                cv2.putText(frame, name_found, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, "Not Found", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('Video', frame)
            
        if time.time() - start_time > 4:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    cursor.close()
    
    if name_found != False:
        name_split = name_found.split(" ", 1)
    
    if admin_search == True and name_found != False:
        root_main.withdraw()
        admin_page(id_or_reg_no, name_split[1], name_split[0])
    elif student_search == True and name_found != False:
        root_main.withdraw()
        student_page(name_split[1], name_split[0], id_or_reg_no)
    
    
def back_button():
    if frame_face_rec.winfo_ismapped():
        frame_face_rec.pack_forget()
        frame_login.pack(pady=20,padx=40,fill='both',expand=True)
        if user_entry_fn.get():
            user_entry_fn.delete(0, "end")
        if user_entry_ln.get():
            user_entry_ln.delete(0, "end")
        if user_pass.get():
            user_pass.delete(0, "end")

    
def close():
    if tkmb.askokcancel("Quit", "Do you want to quit?"):
        conn.close()
        tunnel.stop()
        root_main.destroy()
        exit()

if __name__=="__main__":
    login_form()
