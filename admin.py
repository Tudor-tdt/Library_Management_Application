import customtkinter as ctk
import tkinter.messagebox as tkmb
from db_connection import *
from PIL import Image, ImageTk
import tkinter as Tk
import io
from datetime import datetime

first_input = 0
buttons_list = []
user_searches = []
new_image = 0

def admin_page(id, l_name, f_name):
    
    global root_admin

    root_admin = ctk.CTkToplevel() 
    root_admin.geometry("1300x750")
    root_admin.minsize(width=root_admin.winfo_screenwidth(), height=root_admin.winfo_screenheight())
    root_admin.title("Library Management System - ADMIN")
    iconpath = ImageTk.PhotoImage(file = "books3.ico")
    root_admin.wm_iconbitmap()
    root_admin.after(300, lambda: root_admin.iconphoto(False, iconpath))
    
    global user_entry_frame
    user_entry_frame = ctk.CTkFrame(master = root_admin, height=50, fg_color="#242424")
    user_entry_frame.pack(pady=(15, 0), padx=15, fill="both")
    
    global back_btn
    back_btn = ctk.CTkButton(master=user_entry_frame, text="Back", width=85, fg_color="#29a329", hover_color="#248f24", cursor="hand2", font=("Helvetica", 15), command=back_button)
    
    global logout_btn
    logout_btn = ctk.CTkButton(master=user_entry_frame, text="Logout", width=85, fg_color="#ff0000", hover_color="#e60000", cursor="hand2", font=("Helvetica", 15), command=main_login)
    logout_btn.grid(row=0, column=0, sticky="w", padx=15, pady=15)
    
    img_new_book = Image.open("add_new_book.ico")
    img_new_book = img_new_book.resize((25, 25))
    img_new_book = ImageTk.PhotoImage(img_new_book)
    new_book_btn = ctk.CTkButton(master=user_entry_frame, text="New Book", image=img_new_book, command=new_book, compound="right", width=125, fg_color="#006080", hover_color="#004d66", cursor="hand2", font=("Helvetica", 15))
    new_book_btn.grid(row=0, column=1, sticky="w", padx=15, pady=15)
    
    img_search_student = Image.open("user_icon77.ico")
    img_search_student = img_search_student.resize((50, 50))
    img_search_student = ImageTk.PhotoImage(img_search_student)
    search_student_btn = Tk.Button(master=user_entry_frame, image = img_search_student, command=lambda: button_search(search_student_btn, search_book_btn), borderwidth=0, bg="#242424", activebackground="#242424", cursor="hand2")
    search_student_btn.grid(row=0, column=1, sticky="e", padx=15, pady=15)
    
    global user_entry_search1
    user_entry_search1 = ctk.CTkEntry(master=user_entry_frame, placeholder_text="Search for a book...", width=300) 
    user_entry_search1.grid(row=0, column=2, sticky="w", padx=15, pady=15)
    user_entry_search1.bind('<KeyRelease>', show_book_search)
    
    global user_entry_search2
    user_entry_search2 = ctk.CTkEntry(master=user_entry_frame, placeholder_text="Search for a student...", width=300)
    user_entry_search2.bind('<KeyRelease>', show_student_search)
    
    img_search_book = Image.open("book33.ico")
    img_search_book = img_search_book.resize((50, 50))
    img_search_book = ImageTk.PhotoImage(img_search_book)
    search_book_btn = Tk.Button(master=user_entry_frame, image = img_search_book, command=lambda: button_search(search_student_btn, search_book_btn), state="disabled", borderwidth=0, bg="#242424", activebackground="#242424")
    search_book_btn.grid(row=0, column=3, sticky="w", padx=15, pady=15)
    
    label_name = ctk.CTkLabel(master=user_entry_frame, text = l_name + " " + f_name, font=('Helvetica',16))
    label_name.grid(row=0, column=4, sticky="e", padx=3, pady=15)
    
    user_img = Image.open("user_icon23.ico")
    user_img = user_img.resize((50, 50))
    user_img = ImageTk.PhotoImage(user_img)
    user_btn = Tk.Button(master=user_entry_frame, image = user_img, command=lambda: user_menu(id), borderwidth=0, bg="#242424", activebackground="#242424", cursor="hand2")
    user_btn.grid(row=0, column=5, sticky="e", padx=15, pady=15)
    
    user_entry_frame.grid_columnconfigure(1, weight=1)
    user_entry_frame.grid_columnconfigure(3, weight=1)

    global frame_first_page
    frame_first_page = ctk.CTkFrame(master=root_admin)
    frame_first_page.pack(pady=15, padx=15, fill="both", expand=True)
    
    no_copies=0
    cursor_total_books = conn.cursor()
    cursor_total_books.execute("select no_copies from books")
    for i in cursor_total_books:
        no_copies=no_copies+i[0]
    label_total_books = ctk.CTkLabel(master=frame_first_page, text="TOTAL BOOKS:\n"+str(no_copies), font=("Helvetica", 26))
    label_total_books.grid(row=0, column=0, columnspan=2, padx=15, pady=15)
    cursor_total_books.close()
    
    cursor_borrowed_books = conn.cursor()
    cursor_borrowed_books.execute("select count(ISBN_book) from borrowing_history where return_date='0000-00-00 00:00:00'")
    result_borrowed_books = cursor_borrowed_books.fetchone()
    label_borrowed_books = ctk.CTkLabel(master=frame_first_page, text="BORROWED BOOKS:\n"+str(result_borrowed_books[0]), font=("Helvetica", 26))
    label_borrowed_books.grid(row=0, column=1, columnspan=2, padx=15, pady=15)
    cursor_borrowed_books.close()
    
    borrowing_history_label = ctk.CTkLabel(master=frame_first_page, text="Borrowing History:", font=("Helvetica", 22))
    borrowing_history_label.grid(row=1, column=0, padx=15, pady=15, sticky="w")
    
    frame_books_history = ctk.CTkScrollableFrame(master=frame_first_page, width=500)
    frame_books_history.grid(row=3, column=0, columnspan=3, padx=15, pady=15, sticky="nsew")
    
    button_all_borrowed = ctk.CTkButton(master=frame_first_page, text="All borrowed books", font=("Helvetica", 18), cursor="arrow", state="disabled", command=lambda: all_borrowed_books(button_borrowed_today, button_all_borrowed, button_borrowed_yesterday, frame_books_history))
    button_all_borrowed.grid(row=2, column=0, padx=15, pady=15, sticky="nsew")
    
    button_borrowed_today = ctk.CTkButton(master=frame_first_page, text="Books to be returned", font=("Helvetica", 18), cursor="hand2", command=lambda: books_to_be_returned(button_borrowed_today, button_all_borrowed, button_borrowed_yesterday, frame_books_history))
    button_borrowed_today.grid(row=2, column=1, padx=15, pady=15, sticky="nsew")
    
    button_borrowed_yesterday = ctk.CTkButton(master=frame_first_page, text="Borrowed today", font=("Helvetica", 18), cursor="hand2", command=lambda: borrowed_today(button_borrowed_today, button_all_borrowed, button_borrowed_yesterday, frame_books_history))
    button_borrowed_yesterday.grid(row=2, column=2, padx=15, pady=15, sticky="nsew")
    
    all_borrowed_books(button_borrowed_today, button_all_borrowed, button_borrowed_yesterday, frame_books_history)
    
    frame_first_page.grid_columnconfigure(0, weight=1)
    frame_first_page.grid_columnconfigure(1, weight=1)
    frame_first_page.grid_columnconfigure(2, weight=1)
    frame_first_page.grid_rowconfigure(3, weight=1)
    
    global frame_student_info, frame_show_books_details, zero_found, frame_show_search_buttons, frame_user_menu, frame_new_book
    frame_student_info = ctk.CTkScrollableFrame(master=root_admin, fg_color="#292929")
    frame_show_books_details = ctk.CTkScrollableFrame(master=root_admin, fg_color="#292929")
    frame_show_search_buttons = ctk.CTkFrame(master=root_admin, width=450, fg_color="#292929")
    zero_found = ctk.CTkLabel(master=root_admin, text="No Found", font=("Helvetica", 30))
    frame_user_menu = ctk.CTkFrame(master=root_admin, fg_color="#292929")
    frame_new_book = ctk.CTkScrollableFrame(master=root_admin, fg_color="#292929")
    
    root_admin.protocol("WM_DELETE_WINDOW", close)
    root_admin.mainloop()
    

def all_borrowed_books(button_borrowed_today, button_all_borrowed, button_borrowed_yesterday, frame_books_history):
    button_all_borrowed.configure(state="disabled", cursor="arrow")
    button_borrowed_today.configure(state="normal", cursor="hand2")
    button_borrowed_yesterday.configure(state="normal", cursor="hand2")
        
    frame_books_history.destroy()
    frame_books_history = ctk.CTkScrollableFrame(master=frame_first_page, width=500)
    frame_books_history.grid(row=3, column=0, columnspan=3, padx=15, pady=15, sticky="nsew")
    
    student_name_label = ctk.CTkLabel(master=frame_books_history, text="STUDENT", font=("Helvetica", 15, "bold"))
    student_name_label.grid(row=0, column=0, padx=15, pady=15)
    title_label = ctk.CTkLabel(master=frame_books_history, text="TITLE", font=("Helvetica", 15, "bold"))
    title_label.grid(row=0, column=1, padx=15, pady=15)
    author_label = ctk.CTkLabel(master=frame_books_history, text="AUTHOR", font=("Helvetica", 15, "bold"))
    author_label.grid(row=0, column=2, padx=15, pady=15)
    borrow_date_label = ctk.CTkLabel(master=frame_books_history, text="BORROW DATE", font=("Helvetica", 15, "bold"))
    borrow_date_label.grid(row=0, column=3, padx=15, pady=15)
    return_date_label = ctk.CTkLabel(master=frame_books_history, text="RETURN DATE", font=("Helvetica", 15, "bold"))
    return_date_label.grid(row=0, column=4, padx=15, pady=15)
    
    cursor_history = conn.cursor()
    cursor_history.execute("SELECT s.registration_number, s.l_name, s.f_name, b.ISBN, b.title, b.authors, bh.borrow_date, bh.return_date FROM borrowing_history bh JOIN students s ON bh.student = s.registration_number JOIN books b ON bh.ISBN_book = b.ISBN ORDER BY bh.borrow_date DESC")
    
    stud_info = lambda reg_no: (lambda p: student_info(reg_no))
    book_info = lambda isbn: (lambda p: book_details(isbn))
    
    roww=1
    
    for i in cursor_history:
        history_data1 = ctk.CTkLabel(master=frame_books_history, text=i[1]+" "+i[2]+"  ", cursor="hand2")
        history_data1.grid(row=roww, column=0, padx=15, pady=5)
        history_data1.bind("<Button-1>", stud_info(i[0]))
        
        if len(i[4])>90:
            title=i[4][:87]+"..."
        else:
            title=i[4]
        if len(i[5])>60:
            auth=i[5][:57]+"..."
        else:
            auth=i[5]
        history_data2 = ctk.CTkLabel(master=frame_books_history, text=title, cursor="hand2")
        history_data2.grid(row=roww, column=1, padx=15, pady=5)
        history_data2.bind("<Button-1>", book_info(i[3]))
        history_data3 = ctk.CTkLabel(master=frame_books_history, text=auth)
        history_data3.grid(row=roww, column=2, padx=15, pady=5)
        
        history_data4 = ctk.CTkLabel(master=frame_books_history, text=str(i[6])+"  ")
        history_data4.grid(row=roww, column=3, padx=15, pady=5)
        if i[7]!="0000-00-00 00:00:00":
            date = i[7]
        else:
            date = "te be returned"
        history_data5 = ctk.CTkLabel(master=frame_books_history, text=date)
        history_data5.grid(row=roww, column=4, padx=15, pady=5)
        roww=roww+1
    
    cursor_history.close()
    
    frame_books_history.grid_columnconfigure(0, weight=1)
    frame_books_history.grid_columnconfigure(1, weight=1)
    frame_books_history.grid_columnconfigure(2, weight=1)
    frame_books_history.grid_columnconfigure(3, weight=1)
    frame_books_history.grid_columnconfigure(4, weight=1)
    

def books_to_be_returned(button_borrowed_today, button_all_borrowed, button_borrowed_yesterday, frame_books_history):
    button_borrowed_today.configure(state="disabled", cursor="arrow")
    button_all_borrowed.configure(state="normal", cursor="hand2")
    button_borrowed_yesterday.configure(state="normal", cursor="hand2")
        
    frame_books_history.destroy()
    frame_books_history = ctk.CTkScrollableFrame(master=frame_first_page, width=500)
    frame_books_history.grid(row=3, column=0, columnspan=3, padx=15, pady=15, sticky="nsew")
        
    student_name_label = ctk.CTkLabel(master=frame_books_history, text="STUDENT", font=("Helvetica", 15, "bold"))
    student_name_label.grid(row=0, column=0, padx=15, pady=15)
    title_label = ctk.CTkLabel(master=frame_books_history, text="TITLE", font=("Helvetica", 15, "bold"))
    title_label.grid(row=0, column=1, padx=15, pady=15)
    author_label = ctk.CTkLabel(master=frame_books_history, text="AUTHOR", font=("Helvetica", 15, "bold"))
    author_label.grid(row=0, column=2, padx=15, pady=15)
    borrow_date_label = ctk.CTkLabel(master=frame_books_history, text="BORROW DATE", font=("Helvetica", 15, "bold"))
    borrow_date_label.grid(row=0, column=3, padx=15, pady=15)
    
    stud_info = lambda reg_no: (lambda p: student_info(reg_no))
    book_info = lambda isbn: (lambda p: book_details(isbn))
        
    cursor_to_be_returned = conn.cursor()
    cursor_to_be_returned.execute("SELECT s.registration_number, s.l_name, s.f_name, b.ISBN, b.title, b.authors, bh.borrow_date FROM borrowing_history bh JOIN students s ON bh.student = s.registration_number JOIN books b ON bh.ISBN_book = b.ISBN WHERE return_date='0000-00-00' ORDER BY bh.borrow_date DESC")
    
    roww=1
    for i in cursor_to_be_returned:
        history_data1 = ctk.CTkLabel(master=frame_books_history, text=i[1]+" "+i[2]+"  ", cursor="hand2")
        history_data1.grid(row=roww, column=0, padx=15, pady=5)
        history_data1.bind("<Button-1>", stud_info(i[0]))
        
        if len(i[4])>90:
            title=i[4][:87]+"..."
        else:
            title=i[4]
        if len(i[5])>60:
            auth=i[5][:57]+"..."
        else:
            auth=i[5]
        history_data2 = ctk.CTkLabel(master=frame_books_history, text=title, cursor="hand2")
        history_data2.grid(row=roww, column=1, padx=15, pady=5)
        history_data2.bind("<Button-1>", book_info(i[3]))
        history_data3 = ctk.CTkLabel(master=frame_books_history, text=auth)
        history_data3.grid(row=roww, column=2, padx=15, pady=5)
        
        history_data4 = ctk.CTkLabel(master=frame_books_history, text=str(i[6])+"  ")
        history_data4.grid(row=roww, column=3, padx=15, pady=5)
        roww=roww+1
    cursor_to_be_returned.close()
    
    frame_books_history.grid_columnconfigure(0, weight=1)
    frame_books_history.grid_columnconfigure(1, weight=1)
    frame_books_history.grid_columnconfigure(2, weight=1)
    frame_books_history.grid_columnconfigure(3, weight=1)
    
    
def borrowed_today(button_borrowed_today, button_all_borrowed, button_borrowed_yesterday, frame_books_history):
    button_borrowed_yesterday.configure(state="disabled", cursor="arrow")
    button_borrowed_today.configure(state="normal", cursor="hand2")
    button_all_borrowed.configure(state="normal", cursor="hand2")
        
    frame_books_history.destroy()
    frame_books_history = ctk.CTkScrollableFrame(master=frame_first_page, width=500)
    frame_books_history.grid(row=3, column=0, columnspan=3, padx=15, pady=15, sticky="nsew")
        
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')
    
    student_name_label = ctk.CTkLabel(master=frame_books_history, text="STUDENT", font=("Helvetica", 15, "bold"))
    student_name_label.grid(row=0, column=0, padx=15, pady=15)
    title_label = ctk.CTkLabel(master=frame_books_history, text="TITLE", font=("Helvetica", 15, "bold"))
    title_label.grid(row=0, column=1, padx=15, pady=15)
    author_label = ctk.CTkLabel(master=frame_books_history, text="AUTHOR", font=("Helvetica", 15, "bold"))
    author_label.grid(row=0, column=2, padx=15, pady=15)
    borrow_date_label = ctk.CTkLabel(master=frame_books_history, text="BORROW HOUR", font=("Helvetica", 15, "bold"))
    borrow_date_label.grid(row=0, column=3, padx=15, pady=15)
    
    stud_info = lambda reg_no: (lambda p: student_info(reg_no))
    book_info = lambda isbn: (lambda p: book_details(isbn))
    
    cursor_borrowed_today = conn.cursor()
    cursor_borrowed_today.execute("SELECT s.registration_number, s.l_name, s.f_name, b.ISBN, b.title, b.authors, bh.borrow_date FROM borrowing_history bh JOIN students s ON bh.student = s.registration_number JOIN books b ON bh.ISBN_book = b.ISBN WHERE (lower(borrow_date) LIKE '%"+ str(formatted_date) +"%') ORDER BY bh.borrow_date DESC")
    
    roww=1
    for i in cursor_borrowed_today:
        history_data1 = ctk.CTkLabel(master=frame_books_history, text=i[1]+" "+i[2]+"  ", cursor="hand2")
        history_data1.grid(row=roww, column=0, padx=15, pady=5)
        history_data1.bind("<Button-1>", stud_info(i[0]))
        
        if len(i[4])>90:
            title=i[4][:87]+"..."
        else:
            title=i[4]
        if len(i[5])>60:
            auth=i[5][:57]+"..."
        else:
            auth=i[5]
        history_data2 = ctk.CTkLabel(master=frame_books_history, text=title, cursor="hand2")
        history_data2.grid(row=roww, column=1, padx=15, pady=5)
        history_data2.bind("<Button-1>", book_info(i[3]))
        history_data3 = ctk.CTkLabel(master=frame_books_history, text=auth)
        history_data3.grid(row=roww, column=2, padx=15, pady=5)
        
        history_data4 = ctk.CTkLabel(master=frame_books_history, text=str(i[6])[10:]+"  ")
        history_data4.grid(row=roww, column=3, padx=15, pady=5)
        roww=roww+1
    cursor_borrowed_today.close()
    
    frame_books_history.grid_columnconfigure(0, weight=1)
    frame_books_history.grid_columnconfigure(1, weight=1)
    frame_books_history.grid_columnconfigure(2, weight=1)
    frame_books_history.grid_columnconfigure(3, weight=1)
    
    
def button_search(search_student_btn, search_book_btn):
    global first_input
    if user_entry_search1.winfo_ismapped():
        user_entry_search1.grid_forget()
        user_entry_search2.grid(row=0, column=2, sticky="w", padx=15, pady=15)
        search_student_btn.configure(state="disabled", cursor="arrow")
        search_book_btn.configure(state="normal", cursor="hand2")
    elif user_entry_search2.winfo_ismapped():
        user_entry_search2.grid_forget()
        user_entry_search1.grid(row=0, column=2, sticky="w", padx=15, pady=15)
        search_student_btn.configure(state="normal", cursor="hand2")
        search_book_btn.configure(state="disabled", cursor="arrow")
    if buttons_list:
        buttons_list.clear()
    if user_searches:
        user_searches.clear()
    if first_input == 1:
        first_input = 0


def show_student_search(*args):
    global first_input
    
    if user_entry_search2.get() != "":
        user_searches.append(user_entry_search2.get())
        if user_entry_search2.get() != user_searches[len(user_searches)-2] or len(user_searches) == 1:
            if buttons_list:
                buttons_list.clear()
                
            if zero_found.winfo_ismapped():
                zero_found.pack_forget()
                first_input = 0
                
            if first_input == 0:
                frame_show_search_buttons.pack(pady=15, padx=(15, 0), side="left", fill="both")
                frame_student_info.pack(pady=15, padx=15, side="right", fill="both", expand=True)
                first_input = 1
                
            if frame_show_search_buttons.winfo_children():
                for widget in frame_show_search_buttons.winfo_children():
                    widget.destroy()
                    
            if frame_student_info.winfo_children():
                for widget in frame_student_info.winfo_children():
                    widget.destroy()
                    
            var_students = student_search(user_entry_search2.get())
            student_reg_no = lambda x: (lambda : student_info(x))
            
            if len(var_students) == 0:
                for widget in root_admin.winfo_children():
                    if widget != user_entry_frame:
                        widget.pack_forget()
                zero_found.pack(padx=30, pady=30)
                if logout_btn.winfo_ismapped():
                    logout_btn.grid_forget()
                    back_btn.grid(row=0, column=0, sticky="w", padx=15, pady=15)
            else:
                if zero_found.winfo_ismapped():
                    zero_found.pack_forget()
                for x, y in var_students.items():
                    studentinfo = y.split("GROUP:")
                    
                    button_student_details = ctk.CTkButton(master = frame_show_search_buttons, text = studentinfo[0] + "\nRegistration number: " + str(x) + "     Group: " + studentinfo[1], font=("Courier", 12), anchor="n", corner_radius=10, fg_color="#404040", hover_color="#4d4d4d", width = 350, command = student_reg_no(x))
                    button_student_details.pack(padx = 5, pady = 2)
                    buttons_list.append(x)
                    buttons_list.append(button_student_details)
                
            if frame_show_search_buttons.winfo_children():
                student_info(list(var_students.keys())[0])
                frame_show_search_buttons.winfo_children()[0].configure(state="disabled")
                      
    elif user_entry_search2.get() == "" and first_input == 1:
        if zero_found.winfo_ismapped():
            zero_found.pack_forget()
        frame_show_search_buttons.pack_forget()
        frame_student_info.pack_forget()
        frame_first_page.pack(pady=15, padx=15, fill="both", expand=True)
        first_input = 0
        buttons_list.clear()
        user_searches.clear()
        if back_btn.winfo_ismapped():
            back_btn.grid_forget()
            logout_btn.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        
def student_search(user_input):
    book_dict = {}
    cursor_student=conn.cursor()
    cursor_student.execute("SELECT f_name, l_name, registration_number, student_group FROM students WHERE f_name LIKE '%{}%' OR l_name LIKE '%{}%' OR registration_number LIKE '%{}%' OR student_group LIKE '%{}%' LIMIT 15".format(user_input, user_input, user_input, user_input))
    for i in cursor_student:
        book_dict[i[2]] = i[1] + " " + i[0] + "GROUP:" + i[3]
    return book_dict
        
    
def show_book_search(*args):
    global first_input, button_book_details
    
    if user_entry_search1.get() != "":
        user_searches.append(user_entry_search1.get())
        if user_entry_search1.get() != user_searches[len(user_searches)-2] or len(user_searches) == 1:
            
            if buttons_list:
                buttons_list.clear()
                
            if zero_found.winfo_ismapped():
                zero_found.pack_forget()
                first_input = 0
            
            if first_input == 0:
                frame_show_search_buttons.pack(pady=15, padx=(15, 0), side="left", fill="both")
                frame_show_books_details.pack(pady=15, padx=15, side="right", fill="both", expand=True)
                first_input = 1
                
            if frame_show_search_buttons.winfo_children():
                for widget in frame_show_search_buttons.winfo_children():
                    widget.destroy()
                    
            if frame_show_books_details.winfo_children():
                for widget in frame_show_books_details.winfo_children():
                    widget.destroy()
            
            var_books = book_search(user_entry_search1.get())
            
            book_isbn = lambda x: (lambda : book_details(x))
            
            if len(var_books) == 0:
                for widget in root_admin.winfo_children():
                    if widget != user_entry_frame:
                        widget.pack_forget()
                zero_found.pack(padx=30, pady=30)
                if logout_btn.winfo_ismapped():
                    logout_btn.grid_forget()
                    back_btn.grid(row=0, column=0, sticky="w", padx=15, pady=15)
            else:
                if zero_found.winfo_ismapped():
                    zero_found.pack_forget()
                for x, y in var_books.items():
                    title_authors = y.split("AUTHORS:")
                    if len(title_authors[0]) > 30:
                        title = title_authors[0][:50] + "..."
                    else:
                        title = title_authors[0]
                    if len(title_authors[1]) > 20:
                        authors = title_authors[1][:40] + "..."
                    else:
                        authors = title_authors[1]
                    if "," in title_authors[1]:
                        no_auth = "AUTHORS"
                    else:
                        no_auth = "AUTHOR"
                    
                    button_book_details = ctk.CTkButton(master = frame_show_search_buttons, text = title + "\n" + no_auth + ": " + authors, font=("Courier", 12), anchor="n", corner_radius=10, fg_color="#404040", hover_color="#4d4d4d", width = 450, command = book_isbn(x))
                    button_book_details.pack(padx = 5, pady = 2)
                    buttons_list.append(x)
                    buttons_list.append(button_book_details)
                
            if frame_show_search_buttons.winfo_children():
                book_details(list(var_books.keys())[0])
                frame_show_search_buttons.winfo_children()[0].configure(state="disabled")
                      
    elif user_entry_search1.get() == "" and first_input == 1:
        if zero_found.winfo_ismapped():
            zero_found.pack_forget()
        frame_show_search_buttons.pack_forget()
        frame_show_books_details.pack_forget()
        frame_first_page.pack(pady=15, padx=15, fill="both", expand=True)
        first_input = 0
        buttons_list.clear()
        user_searches.clear()
        if back_btn.winfo_ismapped():
            back_btn.grid_forget()
            logout_btn.grid(row=0, column=0, sticky="w", padx=15, pady=15)
      
        
def book_search(user_input):
    book_dict = {}
    cursor_book=conn.cursor()
    cursor_book.execute("SELECT ISBN, title, authors FROM books WHERE ISBN LIKE '%{}%' OR title LIKE '%{}%' OR authors LIKE '%{}%' LIMIT 15".format(user_input, user_input, user_input))
    for i in cursor_book:
        book_dict[i[0]] = i[1] + "AUTHORS:" + i[2]
    return book_dict
    
    
def book_details(isbn):
    global label_photo, textbox_title, textbox_authors, textbox_publisher, textbox_description
    
    if frame_show_search_buttons.winfo_ismapped():
        disable_book_button(isbn, user_entry_search1.get())
        
    if frame_first_page.winfo_ismapped():
        frame_first_page.pack_forget()
    elif frame_student_info.winfo_ismapped():
        for widget in frame_student_info.winfo_children():
            widget.destroy()
        frame_student_info.pack_forget()
    
    if not back_btn.winfo_ismapped():
        back_btn.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        logout_btn.grid_forget()
    
    frame_show_books_details.pack(pady=15, padx=15, side="right", fill="both", expand=True)
    
    if frame_show_books_details.winfo_children():
        for widget in frame_show_books_details.winfo_children():
            widget.destroy()
            
    stud_info = lambda data, func: (lambda p: close_buttons_frame(data, func))
    
    cursor_book=conn.cursor()
    cursor_book.execute("select * from books where ISBN='" + isbn + "'")
    
    cursor_borrowed_by=conn.cursor()
    cursor_borrowed_by.execute("SELECT s.registration_number, s.f_name, s.l_name, bh.borrow_date, bh.return_date FROM borrowing_history bh JOIN students s ON bh.student = s.registration_number WHERE bh.ISBN_book = '" + isbn + "' ORDER BY bh.borrow_date DESC")
    
    for i in cursor_book:
        img = Image.open(io.BytesIO(i[9]))
        img = img.resize((300, 370))
        book_photo = ImageTk.PhotoImage(img)
        
        label_photo = ctk.CTkLabel(master=frame_show_books_details, image=book_photo, text="")
        label_photo.grid(pady=15, padx=15, row=0, rowspan=4, column=0, columnspan=1, sticky="nw")
        
        label_title = ctk.CTkLabel(master=frame_show_books_details, text = "TITLE:", font=("Courier", 20, "bold"), fg_color="#292929")
        label_title.grid(pady=(15, 0), padx=(15, 0), row=0, column=1, columnspan=1, sticky="ne")
        
        frame_show_books_details.update_idletasks()
        textbox_title=Tk.Text(master=frame_show_books_details, wrap="word", width=int(frame_show_books_details.winfo_width()*0.05), font=("Courier 20"), pady=6, bg="#292929", fg="white", borderwidth=0)
        textbox_title.insert("0.0", i[2])
        textbox_title.bind('<Map>', count_lines)
        textbox_title.grid(pady=(15, 0), padx=(0, 15), row=0, column=2, columnspan=1, sticky="nw")
        
        if i[5] > 1:
            no_auth = "AUTHORS:"
        else:
            no_auth = "AUTHOR:"
        
        label_authors = ctk.CTkLabel(master=frame_show_books_details, text = no_auth, font=("Courier", 20, "bold"))
        label_authors.grid(pady=0, padx=(15, 0), row=1, column=1, columnspan=1, sticky="ne")
        
        textbox_authors = Tk.Text(master=frame_show_books_details, wrap="word", width=int(frame_show_books_details.winfo_width()*0.04)-4, font=("Courier 20"), pady=2, bg="#292929", fg="white", borderwidth=0)
        textbox_authors.grid(pady=0, padx=(0, 15), row=1, column=2, columnspan=1, sticky="nw")
        textbox_authors.insert("0.0", i[4])
        
        label_publisher = ctk.CTkLabel(master=frame_show_books_details, text = "PUBLISHER:", font=("Courier", 20, "bold"))
        label_publisher.grid(pady=0, padx=(15, 0), row=2, column=1, columnspan=1, sticky="ne")
        
        textbox_publisher = Tk.Text(master=frame_show_books_details, wrap="word", width=int(frame_show_books_details.winfo_width()*0.04)-4, font=("Courier 20"), pady=2, bg="#292929", fg="white", borderwidth=0)
        textbox_publisher.grid(pady=0, padx=(0, 15), row=2, column=2, columnspan=1, sticky="nw")
        textbox_publisher.insert("0.0", i[6])
        
        label_isbn = ctk.CTkLabel(master=frame_show_books_details, text = "ISBN:", font=("Courier", 20, "bold"))
        label_isbn.grid(pady=0, padx=(15, 0), row=3, column=1, columnspan=1, sticky="ne")
        
        textbox_isbn = Tk.Text(master=frame_show_books_details, width=15, height=1, font=("Courier 20"), pady=2, bg="#292929", fg="white", borderwidth=0)
        textbox_isbn.grid(pady=0, padx=(0, 15), row=3, column=2, columnspan=1, sticky="nw")
        textbox_isbn.insert("0.0", i[1])
        textbox_isbn.configure(state="disabled")
        
        img_book = ImageTk.PhotoImage(Image.open("book16.ico").resize((30,30)))
        button_modify = ctk.CTkButton(master=frame_show_books_details, text="Modify book details", image=img_book, command=lambda: modify_book(i[0], button_modify, label_photo, book_photo, button_delete, label_publisher, label_isbn, textbox_isbn, textbox_available_copies), font=("Helvetica", 15), width=200, height=40, compound="right", cursor="hand2", fg_color="#000080", hover_color="#000066")
        button_modify.grid(pady=(15, 0), padx=15, row=4, column=0, columnspan=1)
        
        img_delete = ImageTk.PhotoImage(Image.open("delete_book3.png").resize((30,30)))
        button_delete = ctk.CTkButton(master=frame_show_books_details, text="Delete book", image=img_delete, command=lambda: delete_book(isbn), font=("Helvetica", 15), width=200, height=40, compound="right", cursor="hand2", fg_color="#b30000", hover_color="#990000")
        button_delete.grid(pady=15, padx=15, row=5, column=0, columnspan=1)
        
        frame_copies = ctk.CTkFrame(master=frame_show_books_details, fg_color="#292929", border_width=0)
        frame_copies.grid(pady=0, padx=(15, 0), ipady=0, ipadx=0, row=6, column=0)
        
        label_available_copies = ctk.CTkLabel(master=frame_copies, fg_color="#292929", text = "Available copies:", font=("Courier", 20, "bold"))
        label_available_copies.pack(side="left")
        
        textbox_available_copies = Tk.Text(master=frame_copies, width=2, height=1, font=("Courier 20"), pady=2, bg="#292929", fg="white", borderwidth=0)
        textbox_available_copies.pack(side="left")
        textbox_available_copies.insert("0.0", i[8])
        textbox_available_copies.configure(state="disabled")
        
        description_label = ctk.CTkLabel(master=frame_show_books_details, fg_color="#292929", text = "Description:", font=("Courier", 20, "bold"))
        description_label.grid(pady=(20, 15), padx=29, row=7, column=0, sticky="w")
        
        textbox_description =Tk.Text(master=frame_show_books_details, wrap="word", width=int(frame_show_books_details.winfo_width()*0.06), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        textbox_description.grid(pady=(0, 15), padx=15, row=8, column=0, columnspan=3)
        textbox_description.insert("0.0", "      " + i[3])
        
        borrowed_by = ctk.CTkLabel(master=frame_show_books_details, fg_color="#292929", text = "Borrowed by:", font=("Courier", 20, "bold"))
        borrowed_by.grid(pady=(15, 10), padx=(32, 0), row=9, column=0, columnspan=2, sticky="w")
        
        roow=10
        for j in cursor_borrowed_by:
            if str(j[4]) == "0000-00-00 00:00:00":
                return_date = "to be returned"
            elif str(j[4]) != "0000-00-00 00:00:00":
                return_date = str(j[3])
            label_book = ctk.CTkLabel(master=frame_show_books_details, fg_color="#262626", text="NAME: "+j[2]+" "+j[1]+"            Borrow date: "+str(j[3])+"            Return date: "+return_date, font=("Helvetica", 15), cursor="hand2")
            label_book.grid(row=roow, column=0, columnspan=3, sticky="w", padx=(38, 0), pady=4, ipadx=5)
            label_book.bind("<Button-1>", stud_info(j[0], "student_info"))
            roow = roow + 1
    
    frame_show_books_details.grid_columnconfigure(2, weight=2, uniform="group1")
    
    cursor_book.close()


def count_monkeypatch(self, index1, index2, *args):
    args = [self._w, "count"] + ["-" + arg for arg in args] + [index1, index2]

    result = self.tk.call(*args)
    return result

Tk.Text.count = count_monkeypatch

def count_lines(*args):
    textbox_title.configure(state="disabled", height=textbox_title.count("0.0", "end", "displaylines"))
    textbox_authors.configure(state="disabled", height=textbox_authors.count("0.0", "end", "displaylines"))
    textbox_publisher.configure(state="disabled", height=textbox_publisher.count("0.0", "end", "displaylines"))
    textbox_description.configure(state="disabled", height=textbox_description.count("0.0", "end", "displaylines"))


def modify_book(id, button_modify, label_photo, old_photo, button_delete, label_publisher, label_isbn, textbox_isbn, textbox_available_copies):
    global first_input, new_image
    new_image = 0
    cursor_copies = conn.cursor()
    cursor_copies.execute("select no_copies, available_copies from books where ID="+str(id))
    copies = cursor_copies.fetchone()
    cursor_copies.close()
    
    if copies[0] == copies[1]:
        button_delete.destroy()
        checked_img = ImageTk.PhotoImage(Image.open("checked2.ico").resize((30,30)))
        button_modify.configure(text="Save changes", fg_color="#009900", hover_color="#008000", image=checked_img, command=lambda: save_changes(id, textbox_noauthors, textbox_isbn, textbox_available_copies))
        button_modify.grid(pady=15, padx=15, row=4, column=0, columnspan=1)
        label_photo.destroy()
        
        my_canvas = ctk.CTkCanvas(master=frame_show_books_details, width=295, height=365, cursor="hand2")
        my_canvas.grid(pady=15, padx=15, row=0, rowspan=4, column=0, columnspan=1, sticky="nw")
        my_canvas.bind("<Button-1>", lambda p: add_new_image(my_canvas, frame_show_books_details, 0))
        my_canvas.create_image(0,0, image=old_photo, anchor="nw")
        my_canvas.create_text(150, 180, text="Add new image", font=("Helvetica", 28, "bold"), fill="#0000ff")
        my_canvas.create_text(150, 3, text="--------------------------------", font=("Helvetica", 20), fill="#0000ff")
        for line in range(17, 360, 15):
            my_canvas.create_text(5, line, text="|", font=("Helvetica", 10, "bold"), fill="#0000ff")
        for line in range(17, 360, 15):
            my_canvas.create_text(292, line, text="|", font=("Helvetica", 10, "bold"), fill="#0000ff")
        my_canvas.create_text(150, 360, text="--------------------------------", font=("Helvetica", 20), fill="#0000ff")
        
        textbox_title.configure(state="normal", bg="#212121")
        textbox_authors.configure(state="normal", bg="#212121")
        label_noauthors = ctk.CTkLabel(master=frame_show_books_details, text = "Authors Number:", font=("Courier", 20, "bold"))
        label_noauthors.grid(pady=0, padx=(15, 0), row=2, column=1, columnspan=1, sticky="ne")
        
        cursor_noauthors = conn.cursor()
        cursor_noauthors.execute("select no_authors from books where ID="+str(id))
        noauthors = cursor_noauthors.fetchone()
        textbox_noauthors = Tk.Text(master=frame_show_books_details, width=2, height=1, font=("Courier 20"), pady=2, bg="#212121", fg="white", borderwidth=0)
        textbox_noauthors.insert(0.0, noauthors[0])
        textbox_noauthors.grid(pady=0, padx=(0, 15), row=2, column=2, columnspan=1, sticky="nw")
        cursor_noauthors.close()
        
        label_publisher.grid(pady=0, padx=(15, 0), row=3, column=1, columnspan=1, sticky="ne")
        textbox_publisher.configure(state="normal", bg="#212121")
        textbox_publisher.grid(pady=0, padx=(0, 15), row=3, column=2, columnspan=1, sticky="nw")
        label_isbn.grid(pady=0, padx=(15, 0), row=4, column=1, columnspan=1, sticky="ne")
        textbox_isbn.configure(state="normal", bg="#212121")
        textbox_isbn.grid(pady=0, padx=(0, 15), row=4, column=2, columnspan=1, sticky="nw")
        textbox_available_copies.configure(state="normal", bg="#212121")
        textbox_description.configure(state="normal", bg="#212121", height=12)
        
    elif copies[0] > copies[1]:
        tkmb.showinfo(title="Info", message="All books must be returned first!")
            
            
def add_new_image(my_canvas, frame_img, roow):
    global new_image
    f_types = [("Image File",'.jpg .png .jpeg')]
    filename = Tk.filedialog.askopenfilename(multiple=False, filetypes=f_types)
    if filename:
        new_image = 1
        blob_value = open(filename, 'rb').read()
        add_new_image.blob_image = blob_value
        
        img1=Image.open(filename)
        img2=img1.resize((300, 370))
        img2=ImageTk.PhotoImage(img2)
        new_img =Tk.Label(master=frame_img)
        new_img.grid(pady=15, padx=15, row=roow, rowspan=4, column=0, columnspan=1, sticky="nw")
        new_img.image = img2
        my_canvas.destroy()
        new_img['image']=img2
    
    
def save_changes(id, textbox_noauthors, textbox_isbn, textbox_available_copies):
    global new_image
    field_empty = 0
    if len(textbox_title.get(0.0, "end-1c")) == 0:
        field_empty = 1
        textbox_title.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        textbox_title.after(2000, lambda: textbox_title.configure(highlightthickness=0))
    if len(textbox_authors.get(0.0, "end-1c")) == 0:
        field_empty = 1
        textbox_authors.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        textbox_authors.after(2000, lambda: textbox_authors.configure(highlightthickness=0))
    if len(textbox_noauthors.get(0.0, "end-1c")) == 0 or check_type(textbox_noauthors.get(0.0, "end-1c")) == False:
        field_empty = 1
        textbox_noauthors.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        textbox_noauthors.after(2000, lambda: textbox_noauthors.configure(highlightthickness=0))
    if len(textbox_publisher.get(0.0, "end-1c")) == 0:
        field_empty = 1
        textbox_publisher.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        textbox_publisher.after(2000, lambda: textbox_publisher.configure(highlightthickness=0))
    if len(textbox_isbn.get(0.0, "end-1c")) == 0:
        field_empty = 1
        textbox_isbn.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        textbox_isbn.after(2000, lambda: textbox_isbn.configure(highlightthickness=0))
    if len(textbox_available_copies.get(0.0, "end-1c")) == 0 or check_type(textbox_available_copies.get(0.0, "end-1c")) == False:
        field_empty = 1
        textbox_available_copies.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        textbox_available_copies.after(2000, lambda: textbox_available_copies.configure(highlightthickness=0))
    if len(textbox_description.get(0.0, "end-1c")) == 0:
        field_empty = 1
        textbox_description.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        textbox_description.after(2000, lambda: textbox_description.configure(highlightthickness=0))
    
    if field_empty == 0:
        cursor_update=conn.cursor()
        if new_image == 1:
            sql = "UPDATE books SET ISBN=%s, title=%s, description=%s, authors=%s, no_authors="+str(textbox_noauthors.get(0.0, "end-1c")).strip()+", publisher=%s, no_copies="+str(textbox_available_copies.get(0.0, "end-1c")).strip()+", available_copies="+str(textbox_available_copies.get(0.0, "end-1c")).strip()+", picture=%s WHERE ID="+str(id)
            cursor_update.execute(sql, (textbox_isbn.get(0.0, "end-1c").strip(), textbox_title.get(0.0, "end-1c").strip(), textbox_description.get(0.0, "end").strip(), textbox_authors.get(0.0, "end").strip(), textbox_publisher.get(0.0, "end").strip(), add_new_image.blob_image))
        else:
            sql = "UPDATE books SET ISBN=%s, title=%s, description=%s, authors=%s, no_authors="+str(textbox_noauthors.get(0.0, "end-1c")).strip()+", publisher=%s, no_copies="+str(textbox_available_copies.get(0.0, "end-1c")).strip()+", available_copies="+str(textbox_available_copies.get(0.0, "end-1c")).strip()+" WHERE ID="+str(id)
            cursor_update.execute(sql, (textbox_isbn.get(0.0, "end-1c").strip(), textbox_title.get(0.0, "end-1c").strip(), textbox_description.get(0.0, "end-1c").strip(), textbox_authors.get(0.0, "end-1c").strip(), textbox_publisher.get(0.0, "end-1c").strip()))
        
        conn.commit()
        
        tkmb.showinfo(title="Info", message="Book information was updated!")
        back_button()


def check_type(val):
    try:
        float(val)
        return True
    except ValueError:
        return False


def delete_book(isbn):
    global first_input
    cursor_copies = conn.cursor()
    cursor_copies.execute("select no_copies, available_copies from books where ISBN='"+isbn+"'")
    copies = cursor_copies.fetchone()
    cursor_copies.close()
    
    if copies[0] == copies[1] and tkmb.askyesno(title="Delete Book", message="Are you sure you want to delete this book?"):
        tkmb.showinfo(title="Info", message="Book was deleted!")
        back_button()
        
        cursor_delete = conn.cursor()
        cursor_delete.execute("DELETE FROM books WHERE ISBN='"+isbn+"'")
        conn.commit()
        cursor_delete.close()
        
        cursor_delete_history = conn.cursor()
        cursor_delete_history.execute("DELETE FROM borrowing_history WHERE ISBN_book='"+isbn+"'")
        conn.commit()
        cursor_delete_history.close()
        
    elif copies[0] > copies[1]:
        tkmb.showinfo(title="Info", message="All books must be returned first!")
   

def disable_book_button(isbn, user_input_search):
    if user_input_search != "" and first_input == 1 and len(buttons_list)>2:
        for widget in frame_show_search_buttons.winfo_children():
            if widget.cget("state") == "disabled":
                widget.configure(state="normal")
                break
        for i in range(0, len(buttons_list)-1, 2):
            if buttons_list[i] == isbn:
                frame_show_search_buttons.winfo_children()[int(i/2)].configure(state="disabled")
                        
                        
def disable_student_button(reg_no, user_input_search):
    if user_input_search != "" and first_input == 1 and len(buttons_list)>2:
        for widget in frame_show_search_buttons.winfo_children():
            if widget.cget("state") == "disabled":
                widget.configure(state="normal")
                break
        for i in range(0, len(buttons_list)-1, 2):
            if buttons_list[i] == reg_no:
                frame_show_search_buttons.winfo_children()[int(i/2)].configure(state="disabled")
    

def student_info(reg_no):
    global first_input
    frame_student_info.pack(padx=15, pady=15, side="right", fill="both", expand=True)
    
    if frame_student_info.winfo_children():
        for widget in frame_student_info.winfo_children():
            widget.destroy()
    
    if not back_btn.winfo_ismapped():
        back_btn.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        logout_btn.grid_forget()
        
    toggle = 0
    
    if frame_show_search_buttons.winfo_ismapped():
        disable_student_button(reg_no, user_entry_search2.get())
    
    if frame_first_page.winfo_ismapped():
        frame_first_page.pack_forget()
    elif frame_show_books_details.winfo_ismapped():
        for widget in frame_show_books_details.winfo_children():
            widget.destroy()
        frame_show_books_details.pack_forget()
    
    cursor_history = conn.cursor()
    cursor_history.execute("SELECT b.ISBN, b.title, b.authors, bh.borrow_date, bh.return_date FROM borrowing_history bh JOIN books b ON bh.ISBN_book = b.ISBN WHERE bh.student = "+ str(reg_no) +" ORDER BY bh.borrow_date DESC")
    
    cursor_s=conn.cursor()
    cursor_s.execute("select * from students where registration_number=" + str(reg_no))
    
    for i in cursor_s:
        img = Image.open(io.BytesIO(i[10]))
        img = img.resize((300, 370))
        image_s = ImageTk.PhotoImage(img)
        
        label_image_s = ctk.CTkLabel(master=frame_student_info, text="", image=image_s)
        label_image_s.grid(row=1, column=0, rowspan=5, sticky="w", padx=(40, 30), pady=(30, 15))
        
        last_name = Tk.Text(master=frame_student_info, height=1, width=11+len(i[2]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        last_name.grid(row=1, column=1, sticky="w", padx=0, pady=(30, 15))
        last_name.insert("end", "Last name: " + i[2])
        last_name.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        last_name.tag_add("tag_bold_txt", 1.0, 1.11)
        last_name.configure(state="disabled")
        
        first_name = Tk.Text(master=frame_student_info, height=1, width=12+len(i[1]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        first_name.grid(row=2, column=1, sticky="w", padx=0, pady=15)
        first_name.insert("end", "First name: " + i[1])
        first_name.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        first_name.tag_add("tag_bold_txt", 1.0, 1.12)
        first_name.configure(state="disabled")
        
        group = Tk.Text(master=frame_student_info, height=1, width=7+len(i[5]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        group.grid(row=3, column=1, sticky="w", padx=0, pady=15)
        group.insert("end", "Group: " + i[5])
        group.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        group.tag_add("tag_bold_txt", 1.0, 1.7)
        group.configure(state="disabled")
        
        if first_input == 1:
            prog_of_study = Tk.Text(master=frame_student_info, height=1, width=20+len(i[6]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
            prog_of_study.grid(row=4, column=1, columnspan=1, sticky="w", padx=0, pady=15)
            study = i[6].split(" ")
            prog_of_study.insert("end", "Programme of Study: ")
            word_count = 0
            for word in study:
                prog_of_study.insert("end", word + " ")
                word_count = word_count + 1
                if word_count == 3 and len(study)>3:
                    prog_of_study.insert("end", "\n                    ")
                    prog_of_study.configure(height=2)
            prog_of_study.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
            prog_of_study.tag_add("tag_bold_txt", 1.0, 1.19)
            prog_of_study.configure(state="disabled")
        else:
            prog_of_study = Tk.Text(master=frame_student_info, height=1, width=20+len(i[6]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
            prog_of_study.grid(row=4, column=1, columnspan=1, sticky="w", padx=0, pady=15)
            prog_of_study.insert("end", "Programme of Study: " + i[6])
            prog_of_study.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
            prog_of_study.tag_add("tag_bold_txt", 1.0, 1.19)
            prog_of_study.configure(state="disabled")
        
        registration_number = Tk.Text(master=frame_student_info, height=1, width=21+len(str(i[4])), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        registration_number.grid(row=5, column=1, sticky="w", padx=0, pady=15)
        registration_number.insert("end", "Registration number: " + str(i[4]))
        registration_number.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        registration_number.tag_add("tag_bold_txt", 1.0, 1.21)
        registration_number.configure(state="disabled")
        
        if first_input == 1:
            email = Tk.Text(master=frame_student_info, height=1, width=41+len(i[8])+len(str(i[9]))+len(str(i[7])), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
            email.grid(row=6, column=0, columnspan=2, sticky="w", padx=(40, 30), pady=15)
            email.insert("end", "E-mail: " + i[8] + "   Telephone: 0" + str(i[9]) + "   Date of Birth: " + str(i[7]))
            email.tag_configure("tag_one_txt", font=("Courier 20 bold"))
            email.tag_add("tag_one_txt", 1.0, 1.8)
            email.tag_configure("tag_two_txt", font=("Courier 20 bold"))
            email.tag_add("tag_two_txt", "1."+str(11+len(i[8])), "1."+str(12+len(i[8])+11))
            email.tag_configure("tag_three_txt", font=("Courier 20 bold"))
            email.tag_add("tag_three_txt", "1." + str(26+len(i[8])+len(str(i[9]))), "1."+ str(40+len(i[8])+len(str(i[9]))))
            email.configure(state="disabled")
        else:
            email = Tk.Text(master=frame_student_info, height=1, width=51+len(i[8])+len(str(i[9]))+len(str(i[7])), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
            email.grid(row=6, column=0, columnspan=2, sticky="w", padx=(40, 30), pady=15)
            email.insert("end", "E-mail: " + i[8] + "        Telephone: 0" + str(i[9]) + "        Date of Birth: " + str(i[7]))
            email.tag_configure("tag_one_txt", font=("Courier 20 bold"))
            email.tag_add("tag_one_txt", 1.0, 1.8)
            email.tag_configure("tag_two_txt", font=("Courier 20 bold"))
            email.tag_add("tag_two_txt", "1."+str(16+len(i[8])), "1."+str(16+len(i[8])+11))
            email.tag_configure("tag_three_txt", font=("Courier 20 bold"))
            email.tag_add("tag_three_txt", "1." + str(36+len(i[8])+len(str(i[9]))), "1."+ str(51+len(i[8])+len(str(i[9]))))
            email.configure(state="disabled")
        
        frame_user_psw = ctk.CTkFrame(master=frame_student_info, fg_color="#292929")
        frame_user_psw.grid(row=7, column=0, columnspan=2, padx=32, pady=15, sticky="w")
        
        paswrd = Tk.Text(master=frame_user_psw, height=1, width=10+len(i[3]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        paswrd.grid(row=0, column=0)
        paswrd.insert("end", "Password: " + "*" * len(i[3]))
        paswrd.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        paswrd.tag_add("tag_bold_txt", 1.0, 1.9)
        paswrd.configure(state="disabled")
        
        eye_img = Image.open("eye_open4.png")
        eye_img = eye_img.resize((40, 30))
        eye_img = ImageTk.PhotoImage(eye_img)
        eye_open = Tk.Button(master=frame_user_psw, image = eye_img, command=lambda: toggle_pswd(frame_user_psw, paswrd, i[3], eye_open, toggle), borderwidth=0, bg="#292929", activebackground="#292929", cursor="hand2")
        eye_open.image = eye_img
        eye_open.grid(row=0, column=1, padx=(10, 0))
        
        books_borrwoed = ctk.CTkLabel(master=frame_student_info, text="Borrowing history:", font=("Courier", 20, "bold"), text_color="white")
        books_borrwoed.grid(row=8, column=0, sticky="w", padx=34, pady=(15, 15))
        
        book_isbn = lambda data, func: (lambda p: close_buttons_frame(data, func))
        
        roow = 9
        for j in cursor_history:
            if "," in j[2]:
                auth = "AUTHORS: "
            else:
                auth = "AUTHOR: "
            if len(j[2]) > 25:
                authors = j[2][:22]+"..."
            elif len(j[2]) <= 25:
                authors = j[2]
            if len(j[1]) > 50:
                title = j[1][:47]+"..."
            elif len(j[1]) <= 50:
                title = j[1]
            if str(j[4]) == "0000-00-00 00:00:00":
                return_date = "to be returned"
            elif str(j[4]) != "0000-00-00 00:00:00":
                return_date = str(j[4])
            if first_input == 1:
                label_book = ctk.CTkLabel(master=frame_student_info, fg_color="#262626", text="TITLE: "+title+"      "+auth+authors+"      ISBN: "+j[0]+"\nBorrow date: "+str(j[3])+"      Return date: "+return_date, font=("Helvetica", 15), cursor="hand2")
                label_book.grid(row=roow, column=0, columnspan=2, sticky="nsew", padx=(40, 5), pady=8, ipadx=5)
                label_book.bind("<Button-1>", book_isbn(j[0], "book_details"))
            else:  
                label_book = ctk.CTkLabel(master=frame_student_info, fg_color="#262626", text="TITLE: "+title+"      "+auth+authors+"      ISBN: "+j[0]+"      Borrow date: "+str(j[3])+"      Return date: "+return_date, font=("Helvetica", 15), cursor="hand2")
                label_book.grid(row=roow, column=0, columnspan=2, sticky="w", padx=(40, 5), pady=4, ipadx=5)
                label_book.bind("<Button-1>", book_isbn(j[0], "book_details"))
            roow = roow + 1
    
    cursor_history.close()
    cursor_s.close()
    frame_student_info.grid_columnconfigure(1, weight=2, uniform="group1")
    
    
def close_buttons_frame(data, func):
    global first_input
    if first_input == 1:
        first_input = 0
    if user_searches:
        user_searches.clear()
    if buttons_list:
        buttons_list.clear()
    frame_show_search_buttons.pack_forget()
    if func == "book_details":
        book_details(data)
    elif func == "student_info":
        student_info(data)
        
        
def user_menu(id):
    for widget in root_admin.winfo_children():
        widget.pack_forget()
    
    frame_user_menu.pack(padx=15, pady=15, fill="both", expand=True)
    
    toggle = 0
    
    back_btn = ctk.CTkButton(master=frame_user_menu, text="Back", command=back_button, width=85, fg_color="#29a329", hover_color="#248f24", cursor="hand2", font=("Helvetica", 15))
    back_btn.grid(row=0, column=0, padx=15, pady=15, sticky="w")
    
    cursor_a=conn.cursor()
    cursor_a.execute("select * from admins where ID=" + str(id))
    
    for i in cursor_a:
        img = Image.open(io.BytesIO(i[7]))
        img = img.resize((300, 370))
        image_s = ImageTk.PhotoImage(img)
        
        label_image_a = ctk.CTkLabel(master=frame_user_menu, text="", image=image_s)
        label_image_a.grid(row=1, column=0, rowspan=3, sticky="w", padx=(40, 30), pady=(30, 15))
        
        last_name = Tk.Text(master=frame_user_menu, height=1, width=11+len(i[2]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        last_name.grid(row=1, column=1, sticky="w", padx=0, pady=(30, 15))
        last_name.insert("end", "Last name: " + i[2])
        last_name.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        last_name.tag_add("tag_bold_txt", 1.0, 1.11)
        last_name.configure(state="disabled")
        
        first_name = Tk.Text(master=frame_user_menu, height=1, width=12+len(i[1]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        first_name.grid(row=2, column=1, sticky="w", padx=0, pady=15)
        first_name.insert("end", "First name: " + i[1])
        first_name.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        first_name.tag_add("tag_bold_txt", 1.0, 1.12)
        first_name.configure(state="disabled")
        
        email = Tk.Text(master=frame_user_menu, height=1, width=8+len(i[5]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        email.grid(row=3, column=1, columnspan=1, sticky="w", padx=0, pady=15)
        email.insert("end", "E-mail: " + i[5])
        email.tag_configure("tag_one_txt", font=("Courier 20 bold"))
        email.tag_add("tag_one_txt", 1.0, 1.8)
        email.configure(state="disabled")
        
        date_tel = Tk.Text(master=frame_user_menu, height=1, width=39+len(str(i[4]))+len(str(i[6])), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        date_tel.grid(row=4, column=0, columnspan=2, sticky="w", padx=(40, 30), pady=15)
        date_tel.insert("end", "Date of Birth: " + str(i[4]))
        date_tel.tag_configure("tag_one_txt", font=("Courier 20 bold"))
        date_tel.tag_add("tag_one_txt", 1.0, 1.14)
        date_tel.insert("end", "            Telephone: 0" + str(i[6]))
        date_tel.tag_configure("tag_two_txt", font=("Courier 20 bold"))
        date_tel.tag_add("tag_two_txt", "1."+str(27+len(str(i[4]))), "1."+str(37+len(str(i[4]))))
        date_tel.configure(state="disabled")
        
        frame_user_psw = ctk.CTkFrame(master=frame_user_menu, fg_color="#292929")
        frame_user_psw.grid(row=5, column=0, columnspan=2, padx=32, pady=15, sticky="w")
        
        paswrd = Tk.Text(master=frame_user_psw, height=1, width=10+len(i[3]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        paswrd.grid(row=0, column=0)
        paswrd.insert("end", "Password: " + "*" * len(i[3]))
        paswrd.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        paswrd.tag_add("tag_bold_txt", 1.0, 1.9)
        paswrd.configure(state="disabled")
        
        eye_img = Image.open("eye_open4.png")
        eye_img = eye_img.resize((40, 30))
        eye_img = ImageTk.PhotoImage(eye_img)
        eye_open = Tk.Button(master=frame_user_psw, image = eye_img, command=lambda: toggle_pswd(frame_user_psw, paswrd, i[3], eye_open, toggle), borderwidth=0, bg="#292929", activebackground="#292929", cursor="hand2")
        eye_open.image = eye_img
        eye_open.grid(row=0, column=1, padx=(10, 0))
        
        change_pass = ctk.CTkButton(master=frame_user_psw, text="Change password", command=lambda: change_password(frame_user_psw, i[3], i[0]), cursor="hand2")
        change_pass.grid(row=0, column=2, padx=(30, 0))
        
    cursor_a.close()
    frame_user_menu.grid_columnconfigure(1, weight=2, uniform="group1")


def toggle_pswd(frame_user_psw, paswrd, password, eye_btn, toggle):
    if toggle == 0:
        eye_btn.destroy()
        eye_img = Image.open("eye_close4.png")
        eye_img = eye_img.resize((40, 30))
        eye_img = ImageTk.PhotoImage(eye_img)
        eye_open = Tk.Button(master=frame_user_psw, image = eye_img, command=lambda: toggle_pswd(frame_user_psw, paswrd, password, eye_open, toggle), borderwidth=0, bg="#292929", activebackground="#292929", cursor="hand2")
        eye_open.image = eye_img
        eye_open.grid(row=0, column=1, padx=(10, 0))
        paswrd.destroy()
        paswrd = Tk.Text(master=frame_user_psw, height=1, width=10+len(password), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        paswrd.grid(row=0, column=0)
        paswrd.insert("end", "Password: " + password)
        paswrd.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        paswrd.tag_add("tag_bold_txt", 1.0, 1.9)
        paswrd.configure(state="disabled")
        toggle = 1
    else:
        eye_btn.destroy()
        eye_img = Image.open("eye_open4.png")
        eye_img = eye_img.resize((40, 30))
        eye_img = ImageTk.PhotoImage(eye_img)
        eye_open = Tk.Button(master=frame_user_psw, image = eye_img, command=lambda: toggle_pswd(frame_user_psw, paswrd, password, eye_open, toggle), borderwidth=0, bg="#292929", activebackground="#292929", cursor="hand2")
        eye_open.image = eye_img
        eye_open.grid(row=0, column=1, padx=(10, 0))
        paswrd.destroy()
        paswrd = Tk.Text(master=frame_user_psw, height=1, width=10+len(password), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        paswrd.grid(row=0, column=0)
        paswrd.insert("end", "Password: " + "*" * len(password))
        paswrd.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        paswrd.tag_add("tag_bold_txt", 1.0, 1.9)
        paswrd.configure(state="disabled")
        toggle = 0
        
        
def change_password(frame_user_psw, password, id):
    for widget in frame_user_psw.winfo_children():
        widget.destroy()
    old_password = ctk.CTkEntry(master=frame_user_psw, text_color="white", placeholder_text = "Old password")
    old_password.grid(row=0, column=0, padx=10, pady=10)
    new_password = ctk.CTkEntry(master=frame_user_psw, text_color="white", placeholder_text = "New password")
    new_password.grid(row=1, column=0, padx=10, pady=10)
    confirm = ctk.CTkButton(master=frame_user_psw, text = "Confirm", command=lambda: update_password(frame_user_psw, password, old_password, new_password, old_password.get(), new_password.get(), id), width=50, cursor="hand2", fg_color="#00b300", hover_color="#009900", text_color="black")
    confirm.grid(row=0, column=1, rowspan=2, padx=10, pady=10)


def update_password(frame_user_psw, password, old_password_entry, new_password_entry, old_password, new_password, id):
    if old_password == "" and new_password == "":
        old_password_entry.configure(placeholder_text_color="#990000")
        old_password_entry.after(2000, lambda: old_password_entry.configure(placeholder_text_color="#737373"))
        new_password_entry.configure(placeholder_text_color="#990000")
        new_password_entry.after(2000, lambda: new_password_entry.configure(placeholder_text_color="#737373"))
    elif old_password == "" and new_password != "":
        old_password_entry.configure(placeholder_text_color="#990000")
        old_password_entry.after(2000, lambda: old_password_entry.configure(placeholder_text_color="#737373"))
    elif old_password != "" and old_password != password and new_password != "":
        old_password_entry.configure(text_color="red")
        old_password_entry.after(2000, lambda: old_password_entry.configure(text_color="white"))
    elif old_password == password and new_password == "":
        new_password_entry.configure(placeholder_text_color="#990000")
        new_password_entry.after(2000, lambda: new_password_entry.configure(placeholder_text_color="#737373"))
    elif old_password != "" and old_password != password and new_password == "":
        old_password_entry.configure(text_color="red")
        old_password_entry.after(2000, lambda: old_password_entry.configure(text_color="white"))
    elif old_password != "" and old_password == password and new_password != "":
        update_success = ctk.CTkLabel(master=frame_user_psw, text="Password updated!", text_color="#009900")
        update_success.grid(row=0, rowspan=2, column=2, padx=10, pady=10)
        update_success.after(4000, lambda: update_success.grid_forget())
        old_password_entry.delete(0, "end")
        new_password_entry.delete(0, "end")
        cursor_update_pass=conn.cursor()
        cursor_update_pass.execute("update admins set password='" + new_password + "'where ID=" + str(id))
        conn.commit()
        cursor_update_pass.close()
        
        
def new_book():
    global new_image
    new_image = 0
    if zero_found.winfo_ismapped():
        zero_found.pack_forget()
    if frame_first_page.winfo_ismapped():
        frame_first_page.pack_forget()
    if user_entry_frame.winfo_ismapped():
        user_entry_frame.pack_forget()
    if frame_show_books_details.winfo_ismapped():
        frame_show_books_details.pack_forget()
    if frame_show_search_buttons.winfo_ismapped():
        frame_show_search_buttons.pack_forget()
    if frame_student_info.winfo_ismapped():
        frame_student_info.pack_forget()
    
    frame_new_book.pack(pady=15, padx=15, side="right", fill="both", expand=True)
    
    back_btn = ctk.CTkButton(master=frame_new_book, text="Back", command=back_button, width=85, fg_color="#29a329", hover_color="#248f24", cursor="hand2", font=("Helvetica", 15))
    back_btn.grid(row=0, column=0, padx=15, pady=15, sticky="w")
    
    my_canvas = ctk.CTkCanvas(master=frame_new_book, width=295, height=365, cursor="hand2")
    my_canvas.grid(pady=15, padx=15, row=1, rowspan=4, column=0, columnspan=1, sticky="nw")
    my_canvas.bind("<Button-1>", lambda p: add_new_image(my_canvas, frame_new_book, 1))
    my_canvas.create_text(150, 180, text="Add book image", font=("Helvetica", 26, "bold"), fill="black")
    my_canvas.create_text(150, 3, text="--------------------------------", font=("Helvetica", 20), fill="black")
    for line in range(17, 360, 15):
        my_canvas.create_text(5, line, text="|", font=("Helvetica", 10, "bold"), fill="black")
    for line in range(17, 360, 15):
        my_canvas.create_text(292, line, text="|", font=("Helvetica", 10, "bold"), fill="black")
    my_canvas.create_text(150, 360, text="--------------------------------", font=("Helvetica", 20), fill="black")
    
    frame_new_book.update_idletasks()
    title=Tk.Text(master=frame_new_book, width=int(frame_new_book.winfo_width()*0.05), height=1, font=("Courier 20"), pady=6, bg="#212121", fg="#4d4d4d", borderwidth=0)
    title.insert(0.0, "Title...")
    title.bind("<FocusIn>", lambda p: foc_in(title))
    title.bind("<FocusOut>", lambda p: foc_out(title, "Title..."))
    title.grid(pady=(15, 0), padx=15, row=1, column=1, columnspan=1, sticky="w")
    
    authors = Tk.Text(master=frame_new_book, width=int(frame_new_book.winfo_width()*0.05), height=1, font=("Courier 20"), pady=2, bg="#212121", fg="#4d4d4d", borderwidth=0)
    authors.insert(0.0, "Authors...")
    authors.bind("<FocusIn>", lambda p: foc_in(authors))
    authors.bind("<FocusOut>", lambda p: foc_out(authors, "Authors..."))
    authors.grid(pady=(15, 0), padx=15, row=2, column=1, columnspan=1, sticky="w")
    
    frame_no_authors = ctk.CTkFrame(master=frame_new_book, fg_color="#292929", border_width=0)
    frame_no_authors.grid(pady=(15, 0), padx=15, ipady=0, ipadx=0, row=3, column=1, sticky="w")
    
    label_no_authors = ctk.CTkLabel(master=frame_no_authors, fg_color="#292929", text = "Authors Number:", text_color="#808080", font=("Courier", 20))
    label_no_authors.pack(side="left")
    
    no_authors = Tk.Text(master=frame_no_authors, width=2, height=1, font=("Courier 20"), pady=2, bg="#212121", fg="white", borderwidth=0)
    no_authors.pack(side="left")
        
    publisher = Tk.Text(master=frame_new_book, width=int(frame_new_book.winfo_width()*0.05), height=1, font=("Courier 20"), pady=2, bg="#212121", fg="#4d4d4d", borderwidth=0)
    publisher.insert(0.0, "Publisher...")
    publisher.bind("<FocusIn>", lambda p: foc_in(publisher))
    publisher.bind("<FocusOut>", lambda p: foc_out(publisher, "Publisher..."))
    publisher.grid(pady=(15, 0), padx=15, row=4, column=1, columnspan=1, sticky="w")
    
    isbn = Tk.Text(master=frame_new_book, width=15, height=1, font=("Courier 20"), pady=2, bg="#212121", fg="#4d4d4d", borderwidth=0)
    isbn.insert(0.0, "ISBN...")
    isbn.bind("<FocusIn>", lambda p: foc_in(isbn))
    isbn.bind("<FocusOut>", lambda p: foc_out(isbn, "ISBN..."))
    isbn.grid(pady=(15, 0), padx=15, row=5, column=1, columnspan=1, sticky="w")
    
    img_book = ImageTk.PhotoImage(Image.open("add_new_book.ico").resize((40,40)))
    button_add = ctk.CTkButton(master=frame_new_book, text="Add book", image=img_book, command=lambda: save_new_book(title, authors, no_authors, publisher, isbn, available_copies, description), font=("Helvetica", 18), width=200, height=40, compound="right", cursor="hand2", fg_color="#006080", hover_color="#004d66")
    button_add.grid(pady=(15, 0), padx=15, row=5, column=0, columnspan=1)
        
    copies = ctk.CTkFrame(master=frame_new_book, fg_color="#292929", border_width=0)
    copies.grid(pady=(15, 0), padx=15, ipady=0, ipadx=0, row=6, column=0)
    
    label_available_copies = ctk.CTkLabel(master=copies, fg_color="#292929", text = "Available copies:", text_color="#808080", font=("Courier", 20))
    label_available_copies.pack(side="left")
    
    available_copies = Tk.Text(master=copies, width=2, height=1, font=("Courier 20"), pady=2, bg="#212121", fg="white", borderwidth=0)
    available_copies.pack(side="left")

    description =Tk.Text(master=frame_new_book, wrap="word", width=int(frame_new_book.winfo_width()*0.06), height=12, font=("Courier 20"), bg="#212121", fg="#4d4d4d", borderwidth=0)
    description.insert(0.0, "Description...")
    description.bind("<FocusIn>", lambda p: foc_in(description))
    description.bind("<FocusOut>", lambda p: foc_out(description, "Description..."))
    description.grid(pady=15, padx=15, row=7, column=0, columnspan=3)
    
    
def foc_in(widget):
    if widget['fg'] == "#4d4d4d":
        widget.delete(0.0, 'end')
        widget['fg'] = "white"
        
        
def foc_out(widget, placeholder_text):
    if not widget.get(0.0, "end-1c"):
        widget.insert(0.0, placeholder_text)
        widget['fg'] = "#4d4d4d"
        
        
def save_new_book(title, authors, no_authors, publisher, isbn, available_copies, description):
    global new_image
    field_empty = 0
    if len(title.get(0.0, "end-1c")) == 0 or title.get(0.0, "end-1c") == "Title...":
        field_empty = 1
        title.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        title.after(2000, lambda: title.configure(highlightthickness=0))
    if len(authors.get(0.0, "end-1c")) == 0 or authors.get(0.0, "end-1c") == "Authors...":
        field_empty = 1
        authors.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        authors.after(2000, lambda: authors.configure(highlightthickness=0))
    if len(no_authors.get(0.0, "end-1c")) == 0 or check_type(no_authors.get(0.0, "end-1c")) == False:
        field_empty = 1
        no_authors.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        no_authors.after(2000, lambda: no_authors.configure(highlightthickness=0))
    if len(publisher.get(0.0, "end-1c")) == 0 or publisher.get(0.0, "end-1c") == "Publisher...":
        field_empty = 1
        publisher.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        publisher.after(2000, lambda: publisher.configure(highlightthickness=0))
    if len(isbn.get(0.0, "end-1c")) == 0 or isbn.get(0.0, "end-1c") == "ISBN...":
        field_empty = 1
        isbn.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        isbn.after(2000, lambda: isbn.configure(highlightthickness=0))
    if len(available_copies.get(0.0, "end-1c")) == 0 or check_type(available_copies.get(0.0, "end-1c")) == False:
        field_empty = 1
        available_copies.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        available_copies.after(2000, lambda: available_copies.configure(highlightthickness=0))
    if len(description.get(0.0, "end-1c")) == 0 or description.get(0.0, "end-1c") == "Description...":
        field_empty = 1
        description.configure(state="normal", bg="#212121", highlightthickness=2, highlightbackground="red", highlightcolor="red")
        description.after(2000, lambda: description.configure(highlightthickness=0))
    
    if field_empty == 0:
        cursor_update=conn.cursor()
        if new_image == 1:
            sql = "INSERT INTO books(ISBN, title, description, authors, no_authors, publisher, no_copies, available_copies, picture) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor_update.execute(sql, (isbn.get(0.0, "end-1c").strip(), title.get(0.0, "end-1c").strip(), description.get(0.0, "end-1c").strip(), authors.get(0.0, "end-1c").strip(), str(no_authors.get(0.0, "end-1c").strip()), publisher.get(0.0, "end-1c").strip(), str(available_copies.get(0.0, "end-1c").strip()), str(available_copies.get(0.0, "end-1c").strip()), add_new_image.blob_image))
            conn.commit()
            tkmb.showinfo(title="Info", message="Book saved successfully!")
            back_button()
        else:
            tkmb.showerror(title="Error", message="Add a picture of the book!")
        
        
def back_button():
    global first_input
    back_btn.grid_forget()
    logout_btn.grid(row=0, column=0, sticky="w", padx=15, pady=15)
    if frame_student_info.winfo_ismapped():
        for widget in frame_student_info.winfo_children():
            widget.destroy()
        frame_student_info.pack_forget()
    if frame_show_books_details.winfo_ismapped():
        frame_show_books_details.pack_forget()
    if frame_show_search_buttons.winfo_ismapped():
        frame_show_search_buttons.pack_forget()
    if zero_found.winfo_ismapped():
        zero_found.pack_forget()
    if frame_new_book.winfo_ismapped():
        for widget in frame_new_book.winfo_children():
            widget.destroy()
        frame_new_book.pack_forget()
        user_entry_frame.pack(pady=(15, 0), padx=15, fill="both")
    if frame_user_menu.winfo_ismapped():
        frame_user_menu.pack_forget()
        for widget in frame_user_menu.winfo_children():
            widget.destroy()
        user_entry_frame.pack(pady=(15, 0), padx=15, fill="both")
    frame_first_page.pack(pady=15, padx=15, fill="both", expand=True)
    if first_input == 1:
        first_input = 0
    if user_searches:
        user_searches.clear()


def main_login():
    global first_input
    root_admin.destroy()
    first_input = 0
    if buttons_list:
        buttons_list.clear()
    if user_searches:
        user_searches.clear()
    from main import login_form
    login_form()
    
def close():
    if tkmb.askokcancel("Quit", "Do you want to quit?"):
        conn.close()
        tunnel.stop()
        root_admin.destroy()
        exit()