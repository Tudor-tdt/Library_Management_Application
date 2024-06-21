import customtkinter as ctk
import tkinter.messagebox as tkmb
from db_connection import *
from PIL import Image, ImageTk
import tkinter as Tk
import io
from datetime import datetime

first_input = 0
first_user_menu = 0
toggle = 0
buttons_list = []
user_searches = []

def student_page(f_name, l_name, reg_no):
    
    global root_student
    
    student_page.regis_num = reg_no

    root_student = ctk.CTkToplevel() 
    root_student.geometry("1300x750")
    root_student.minsize(width=root_student.winfo_screenwidth(), height=root_student.winfo_screenheight())
    root_student.title("Library Management System - STUDENT")
    iconpath = ImageTk.PhotoImage(file = "books3.ico")
    root_student.wm_iconbitmap()
    root_student.after(300, lambda: root_student.iconphoto(False, iconpath))
    
    global user_entry_frame
    user_entry_frame = ctk.CTkFrame(master = root_student, height=50, fg_color="#242424")
    user_entry_frame.pack(pady=(15, 0), padx=15, fill="both")
    
    global back_btn
    back_btn = ctk.CTkButton(master=user_entry_frame, text="Back", command=back_button, width=85, fg_color="#29a329", hover_color="#248f24", cursor="hand2", font=("Helvetica", 15))
    
    global logout_btn
    logout_btn = ctk.CTkButton(master=user_entry_frame, text="Logout", width=85, fg_color="#ff0000", hover_color="#e60000", cursor="hand2", font=("Helvetica", 15), command=main_login)
    logout_btn.grid(row=0, column=0, sticky="w", padx=15, pady=15)
    
    global user_entry_search
    user_entry_search = ctk.CTkEntry(master=user_entry_frame, placeholder_text="Search for a book...", width=300) 
    user_entry_search.grid(row=0, column=2, sticky="w", padx=15, pady=15)
    user_entry_search.bind('<KeyRelease>', show_book_search)
    
    label_name = ctk.CTkLabel(master=user_entry_frame, text = l_name + " " + f_name, font=('Helvetica',16))
    label_name.grid(row=0, column=3, sticky="e", padx=3, pady=15)
    
    user_img = Image.open("user_icon8.png")
    user_img = user_img.resize((50, 50))
    user_img = ImageTk.PhotoImage(user_img)
    user_btn = Tk.Button(master=user_entry_frame, image = user_img, command=lambda: user_menu(reg_no), borderwidth=0, bg="#262626", activebackground="#262626", cursor="hand2")
    user_btn.grid(row=0, column=4, sticky="e", padx=15, pady=15)
    
    user_entry_frame.grid_columnconfigure(1, weight=1)
    user_entry_frame.grid_columnconfigure(3, weight=1)
    
    global latest_books
    latest_books = ctk.CTkLabel(master=root_student, text = "Latest Books:", font=('Arial Black',18), height=0, fg_color="#242424")
    latest_books.pack(padx=15, anchor="w")
    
    global frame_show_books
    frame_show_books = ctk.CTkFrame(master=root_student)
    frame_show_books.pack(pady=15, padx=15, fill="both", expand=True)
        
    cursor_book=conn.cursor()
    cursor_book.execute("select * from books order by ID desc limit 8")
    
    nr_column = 0
    nr_row = 0
        
    for i in cursor_book:
        img = Image.open(io.BytesIO(i[9]))
        img = img.resize((int((root_student.winfo_screenwidth()+300)/6)-25, int((root_student.winfo_screenwidth()+300)/6)+5))
        img = ImageTk.PhotoImage(img)
        
        global frame_book
        frame_book = ctk.CTkFrame(master=frame_show_books, fg_color="#262626")
        frame_book.grid(row = nr_row, column = nr_column, padx = 10, pady = 10)
        
        book_isbn = lambda isbn: (lambda p: book_details(isbn))
    
        label_book = ctk.CTkLabel(master = frame_book, image = img, text="", cursor="hand2")
        label_book.pack(pady=5, padx=5, fill="both", expand=True)
        label_book.bind("<Button-1>", book_isbn(i[1]))
        
        if len(i[2]) > 30:
            book_title = i[2][:30] + "..."
        else:
            book_title = i[2]
        
        label_book = ctk.CTkLabel(master = frame_book, text = book_title, cursor="hand2")
        label_book.pack(pady=5, padx=5, fill="both", expand=True)
        label_book.bind("<Button-1>", book_isbn(i[1]))
        
        nr_column = nr_column + 1
        if nr_column == 4:
            nr_row = nr_row + 1
            nr_column = 0
    
    for i in range(0, 4):
        frame_show_books.grid_columnconfigure(i, weight=1, uniform="group1")
    for i in range(0, 2):
        frame_show_books.grid_rowconfigure(i, weight=1)
    
    global frame_show_books_buttons, frame_show_books_details, frame_user_menu, zero_found
    frame_show_books_details = ctk.CTkScrollableFrame(master=root_student, fg_color="#292929")
    frame_show_books_buttons = ctk.CTkFrame(master=root_student, width=450, fg_color="#292929")
    frame_user_menu = ctk.CTkScrollableFrame(master=root_student, fg_color="#292929")
    zero_found = ctk.CTkLabel(master=root_student, text="No Found", font=("Helvetica", 30))
        
    root_student.protocol("WM_DELETE_WINDOW", close)
    root_student.mainloop()


def show_book_search(*args):
    global first_input, button_book_details
    
    if user_entry_search.get() != "":
        user_searches.append(user_entry_search.get())
        if user_entry_search.get() != user_searches[len(user_searches)-2] or len(user_searches) == 1:
            frame_show_books.pack_forget()
            latest_books.pack_forget()
            
            if buttons_list:
                buttons_list.clear()
                
            if zero_found.winfo_ismapped():
                zero_found.pack_forget()
                first_input = 0
            
            if first_input == 0:
                frame_show_books_buttons.pack(pady=15, padx=(15, 0), side="left", fill="both")
                frame_show_books_details.pack(pady=15, padx=15, side="right", fill="both", expand=True)
                first_input = 1
                
            if frame_show_books_buttons.winfo_children():
                for widget in frame_show_books_buttons.winfo_children():
                    widget.destroy()
                    
            if frame_show_books_details.winfo_children():
                for widget in frame_show_books_details.winfo_children():
                    widget.destroy()
            
            var_books = book_search(user_entry_search.get())
            
            book_isbn = lambda x: (lambda : book_details(x))
            
            if len(var_books) == 0:
                for widget in root_student.winfo_children():
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
                    
                    button_book_details = ctk.CTkButton(master = frame_show_books_buttons, text = title + "\n" + no_auth + ": " + authors, font=("Courier", 12), anchor="n", corner_radius=10, fg_color="#404040", hover_color="#4d4d4d", width = 450, command = book_isbn(x))
                    button_book_details.pack(padx = 5, pady = 2)
                    buttons_list.append(x)
                    buttons_list.append(button_book_details)
                
            if frame_show_books_buttons.winfo_children():
                book_details(list(var_books.keys())[0])
                frame_show_books_buttons.winfo_children()[0].configure(state="disabled")
                      
    elif user_entry_search.get() == "" and first_input == 1:
        if zero_found.winfo_ismapped():
            zero_found.pack_forget()
        frame_show_books_buttons.pack_forget()
        frame_show_books_details.pack_forget()
        latest_books.pack(padx=15, anchor="w")
        frame_show_books.pack(pady=15, padx=15, fill="both", expand=True)
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
    global label_photo, textbox_title, textbox_authors, textbox_publisher, textbox_description, first_input, first_user_menu, toggle
    
    if frame_show_books_buttons.winfo_ismapped():
        disable_button(isbn, user_entry_search.get())
    
    if first_user_menu == 1:
        toggle = 0
        first_input = 0
        user_searches.clear()
        frame_user_menu.pack_forget()
        user_entry_frame.pack(pady=(15, 0), padx=15, fill="both")
        for widget in frame_user_menu.winfo_children():
            widget.destroy()
        first_user_menu = 0
    
    if not back_btn.winfo_ismapped():
        back_btn.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        logout_btn.grid_forget()
    
    if frame_show_books.winfo_ismapped():
        frame_show_books.pack_forget()
        latest_books.pack_forget()
    
    frame_show_books_details.pack(pady=15, padx=15, side="right", fill="both", expand=True)
    
    if frame_show_books_details.winfo_children():
        for widget in frame_show_books_details.winfo_children():
            widget.destroy()
            
    cursor_find_book=conn.cursor()
    cursor_find_book.execute("SELECT borrow_date, return_date FROM borrowing_history where student="+str(student_page.regis_num)+" and ISBN_book='"+isbn+"' order by borrow_date desc limit 1")
    result = cursor_find_book.fetchmany()
    
    cursor_book=conn.cursor()
    cursor_book.execute("select * from books where ISBN='" + isbn + "'")
    
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
        
        if i[8] > 0:
            if len(result) == 0 or (len(result)>0 and result[0][1] != "0000-00-00 00:00:00"):
                img_book = ImageTk.PhotoImage(Image.open("book10.ico").resize((30,30)))
                button_borrow = ctk.CTkButton(master=frame_show_books_details, command=lambda: borrow_or_return_book(frame_show_books_details, button_borrow, isbn, student_page.regis_num, 0, i[8]-1), text="Borrow book", image=img_book, font=("Helvetica", 15), width=200, height=40, compound="right", cursor="hand2", fg_color="#00b300", hover_color="#009900")
                button_borrow.grid(pady=15, padx=15, row=4, column=0, columnspan=1)
            elif len(result)>0 and result[0][1] == "0000-00-00 00:00:00":
                img_book = ImageTk.PhotoImage(Image.open("book9.ico").resize((30,30)))
                button_borrow = ctk.CTkButton(master=frame_show_books_details, command=lambda: borrow_or_return_book(frame_show_books_details, button_borrow, isbn, student_page.regis_num, 1, i[8]+1), text="Return book", image=img_book, font=("Helvetica", 15), width=200, height=40, compound="right", cursor="hand2")
                button_borrow.grid(pady=15, padx=15, row=4, column=0, columnspan=1)
        elif i[8] == 0 and len(result)>0 and result[0][1] == "0000-00-00 00:00:00":
            img_book = ImageTk.PhotoImage(Image.open("book9.ico").resize((30,30)))
            button_borrow = ctk.CTkButton(master=frame_show_books_details, command=lambda: borrow_or_return_book(frame_show_books_details, button_borrow, isbn, student_page.regis_num, 1, i[8]+1), text="Return book", image=img_book, font=("Helvetica", 15), width=200, height=40, compound="right", cursor="hand2")
            button_borrow.grid(pady=15, padx=15, row=4, column=0, columnspan=1)
        elif i[8] == 0 and len(result) == 0:
            img_book = ImageTk.PhotoImage(Image.open("book10.ico").resize((30,30)))
            button_borrow = ctk.CTkButton(master=frame_show_books_details, state="disabled", text="Borrow book", image=img_book, font=("Helvetica", 15), width=200, height=40, compound="right", fg_color="#00b300", hover_color="#009900")
            button_borrow.grid(pady=15, padx=15, row=4, column=0, columnspan=1)
        
        frame_copies = ctk.CTkFrame(master=frame_show_books_details, fg_color="#292929", border_width=0)
        frame_copies.grid(pady=0, padx=(15, 0), ipady=0, ipadx=0, row=5, column=0)
        
        label_available_copies = ctk.CTkLabel(master=frame_copies, fg_color="#292929", text = "Available copies:", font=("Courier", 20, "bold"))
        label_available_copies.pack(side="left")
        
        global textbox_available_copies
        textbox_available_copies = Tk.Text(master=frame_copies, width=2, height=1, font=("Courier 20"), pady=2, bg="#292929", fg="white", borderwidth=0)
        textbox_available_copies.pack(side="left")
        textbox_available_copies.insert("0.0", i[8])
        textbox_available_copies.configure(state="disabled")
        
        description_label = ctk.CTkLabel(master=frame_show_books_details, fg_color="#292929", text = "Description:", font=("Courier", 20, "bold"))
        description_label.grid(pady=(20, 15), padx=29, row=6, column=0, sticky="w")
        
        textbox_description =Tk.Text(master=frame_show_books_details, wrap="word", width=int(frame_show_books_details.winfo_width()*0.06), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        textbox_description.grid(pady=(0, 15), padx=15, row=7, column=0, columnspan=3)
        textbox_description.insert("0.0", "      " + i[3])
    
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


def borrow_or_return_book(frame_show_books_details, button_borrow, isbn, reg_no, state, avail_copies):
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    
    textbox_available_copies.configure(state="normal")
    textbox_available_copies.delete("0.0", "end")
    textbox_available_copies.insert("0.0", avail_copies)
    textbox_available_copies.configure(state="disabled")
    
    cursor_avail_copies = conn.cursor()
    cursor_avail_copies.execute("update books set available_copies=" + str(avail_copies) + " where ISBN='" + isbn + "'")
    conn.commit()
    cursor_avail_copies.close()
    
    if state == 0:
        button_borrow.destroy()
        borrowed_msg = ctk.CTkLabel(master=frame_show_books_details, text="Book successfully borrowed!", text_color="#009900")
        borrowed_msg.grid(pady=15, padx=15, row=4, column=0, columnspan=1)
        img_book = ImageTk.PhotoImage(Image.open("book9.ico").resize((30,30)))
        button_borrow = ctk.CTkButton(master=frame_show_books_details, command=lambda: borrow_or_return_book(frame_show_books_details, button_borrow, isbn, reg_no, 1, avail_copies+1), text="Return book", image=img_book, font=("Helvetica", 15), width=200, height=40, compound="right", cursor="hand2")
        
        cursor_time = conn.cursor()
        cursor_time.execute("insert into borrowing_history(student, ISBN_book, borrow_date) values (" + str(reg_no) + ",'" + isbn + "','" + formatted_date + "')")
        conn.commit()
        cursor_time.close()
        
        borrowed_msg.after(4000, lambda: change_borrow_btn(borrowed_msg, button_borrow))
    elif state == 1:
        button_borrow.destroy()
        returned_msg = ctk.CTkLabel(master=frame_show_books_details, text="Book successfully returned!", text_color="#005ce6")
        returned_msg.grid(pady=15, padx=15, row=4, column=0, columnspan=1)
        img_book = ImageTk.PhotoImage(Image.open("book10.ico").resize((30,30)))
        button_borrow = ctk.CTkButton(master=frame_show_books_details, command=lambda: borrow_or_return_book(frame_show_books_details, button_borrow, isbn, reg_no, 0, avail_copies-1), text="Borrow book", image=img_book, font=("Helvetica", 15), width=200, height=40, compound="right", cursor="hand2", fg_color="#00b300", hover_color="#009900")
        
        cursor_time = conn.cursor()
        cursor_time.execute("update borrowing_history set return_date='" + formatted_date + "' where student=" + str(reg_no) + " and ISBN_book='" + isbn + "' and return_date='0000-00-00 00:00:00'")
        conn.commit()
        cursor_time.close()
        
        returned_msg.after(4000, lambda: change_borrow_btn(returned_msg, button_borrow))


def change_borrow_btn(borrowed_msg, button_borrow):
    borrowed_msg.destroy()
    button_borrow.grid(pady=15, padx=15, row=4, column=0, columnspan=1)


def disable_button(isbn, user_input_search):
    if user_input_search != "" and first_input == 1 and len(buttons_list)>2:
        for widget in frame_show_books_buttons.winfo_children():
            if widget.cget("state") == "disabled":
                widget.configure(state="normal")
                break
        for i in range(0, len(buttons_list)-1, 2):
            if buttons_list[i] == isbn:
                frame_show_books_buttons.winfo_children()[int(i/2)].configure(state="disabled")
    
    
def user_menu(reg_no):
    global first_user_menu
    
    for widget in root_student.winfo_children():
        widget.pack_forget()
    
    frame_user_menu.pack(padx=15, pady=15, fill="both", expand=True)
    if first_user_menu == 0:
        first_user_menu = 1
    
    back_btn = ctk.CTkButton(master=frame_user_menu, text="Back", command=back_button, width=85, fg_color="#29a329", hover_color="#248f24", cursor="hand2", font=("Helvetica", 15))
    back_btn.grid(row=0, column=0, padx=15, pady=15, sticky="w")
    
    cursor_history = conn.cursor()
    cursor_history.execute("SELECT b.title, b.authors, b.ISBN, bh.borrow_date, bh.return_date FROM borrowing_history bh JOIN books b ON bh.ISBN_book = b.ISBN WHERE bh.student = "+ str(reg_no) +" ORDER BY bh.borrow_date DESC")
    
    cursor_s=conn.cursor()
    cursor_s.execute("select f_name, l_name, password, registration_number, student_group, programme_of_study, date_of_birth, email, telephone, picture from students where registration_number = " + str(reg_no))
    
    for i in cursor_s:
        img = Image.open(io.BytesIO(i[9]))
        img = img.resize((300, 370))
        image_s = ImageTk.PhotoImage(img)
        
        label_image_s = ctk.CTkLabel(master=frame_user_menu, text="", image=image_s)
        label_image_s.grid(row=1, column=0, rowspan=5, sticky="w", padx=(40, 30), pady=(30, 15))
        
        last_name = Tk.Text(master=frame_user_menu, height=1, width=11+len(i[1]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        last_name.grid(row=1, column=1, sticky="w", padx=0, pady=(30, 15))
        last_name.insert("end", "Last name: " + i[1])
        last_name.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        last_name.tag_add("tag_bold_txt", 1.0, 1.11)
        last_name.configure(state="disabled")
        
        first_name = Tk.Text(master=frame_user_menu, height=1, width=12+len(i[0]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        first_name.grid(row=2, column=1, sticky="w", padx=0, pady=15)
        first_name.insert("end", "First name: " + i[0])
        first_name.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        first_name.tag_add("tag_bold_txt", 1.0, 1.12)
        first_name.configure(state="disabled")
        
        group = Tk.Text(master=frame_user_menu, height=1, width=7+len(i[4]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        group.grid(row=3, column=1, sticky="w", padx=0, pady=15)
        group.insert("end", "Group: " + i[4])
        group.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        group.tag_add("tag_bold_txt", 1.0, 1.7)
        group.configure(state="disabled")
        
        prog_of_study = Tk.Text(master=frame_user_menu, height=1, width=20+len(i[5]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        prog_of_study.grid(row=4, column=1, columnspan=1, sticky="w", padx=0, pady=15)
        prog_of_study.insert("end", "Programme of Study: " + i[5])
        prog_of_study.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        prog_of_study.tag_add("tag_bold_txt", 1.0, 1.19)
        prog_of_study.configure(state="disabled")
        
        registration_number = Tk.Text(master=frame_user_menu, height=1, width=21+len(str(i[3])), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        registration_number.grid(row=5, column=1, sticky="w", padx=0, pady=15)
        registration_number.insert("end", "Registration number: " + str(i[3]))
        registration_number.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        registration_number.tag_add("tag_bold_txt", 1.0, 1.21)
        registration_number.configure(state="disabled")
        
        email = Tk.Text(master=frame_user_menu, height=1, width=51+len(i[7])+len(str(i[8]))+len(str(i[6])), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        email.grid(row=6, column=0, columnspan=2, sticky="w", padx=(40, 30), pady=15)
        email.insert("end", "E-mail: " + i[7] + "        Telephone: 0" + str(i[8]) + "        Date of Birth: " + str(i[6]))
        email.tag_configure("tag_one_txt", font=("Courier 20 bold"))
        email.tag_add("tag_one_txt", 1.0, 1.8)
        email.tag_configure("tag_two_txt", font=("Courier 20 bold"))
        email.tag_add("tag_two_txt", "1."+str(16+len(i[7])), "1."+str(16+len(i[7])+11))
        email.tag_configure("tag_three_txt", font=("Courier 20 bold"))
        email.tag_add("tag_three_txt", "1." + str(36+len(i[7])+len(str(i[8]))), "1."+ str(51+len(i[7])+len(str(i[8]))))
        email.configure(state="disabled")
        
        frame_user_psw = ctk.CTkFrame(master=frame_user_menu, fg_color="#292929")
        frame_user_psw.grid(row=7, column=0, columnspan=2, padx=32, pady=15, sticky="w")
        
        paswrd = Tk.Text(master=frame_user_psw, height=1, width=10+len(i[2]), font=("Courier 20"), bg="#292929", fg="white", borderwidth=0)
        paswrd.grid(row=0, column=0)
        paswrd.insert("end", "Password: " + "*" * len(i[2]))
        paswrd.tag_configure("tag_bold_txt", font=("Courier 20 bold"))
        paswrd.tag_add("tag_bold_txt", 1.0, 1.9)
        paswrd.configure(state="disabled")
        
        eye_img = Image.open("eye_open4.png")
        eye_img = eye_img.resize((40, 30))
        eye_img = ImageTk.PhotoImage(eye_img)
        eye_open = Tk.Button(master=frame_user_psw, image = eye_img, command=lambda: toggle_pswd(frame_user_psw, paswrd, i[2], eye_open), borderwidth=0, bg="#292929", activebackground="#292929", cursor="hand2")
        eye_open.image = eye_img
        eye_open.grid(row=0, column=1, padx=(10, 0))
        
        change_pass = ctk.CTkButton(master=frame_user_psw, text="Change password", command=lambda: change_password(frame_user_psw, i[2], i[3]), cursor="hand2")
        change_pass.grid(row=0, column=2, padx=(30, 0))
        
        books_borrwoed = ctk.CTkLabel(master=frame_user_menu, text="Borrowing history:", font=("Courier", 20, "bold"), text_color="white")
        books_borrwoed.grid(row=8, column=0, sticky="w", padx=34, pady=(15, 15))
        
        book_isbn = lambda x: (lambda p: book_details(x))
        
        roow = 9
        for j in cursor_history:
            if "," in j[1]:
                auth = "AUTHORS: "
            else:
                auth = "AUTHOR: "
            if len(j[1]) > 25:
                authors = j[1][:22]+"..."
            elif len(j[1]) <= 25:
                authors = j[1]
            if len(j[0]) > 50:
                title = j[0][:47]+"..."
            elif len(j[0]) <= 50:
                title = j[0]
            if str(j[4]) == "0000-00-00 00:00:00":
                return_date = "to be returned"
            elif str(j[4]) != "0000-00-00 00:00:00":
                return_date = str(j[4])
            label_book = ctk.CTkLabel(master=frame_user_menu, fg_color="#262626", text="TITLE: "+title+"      "+auth+authors+"      ISBN: "+j[2]+"      Borrow date: "+str(j[3])+"      Return date: "+return_date, font=("Helvetica", 15), cursor="hand2")
            label_book.grid(row=roow, column=0, columnspan=2, sticky="w", padx=(40, 5), pady=4, ipadx=5)
            label_book.bind("<Button-1>", book_isbn(j[2]))
            roow = roow + 1
    
    cursor_history.close()
    cursor_s.close()
    frame_user_menu.grid_columnconfigure(1, weight=2, uniform="group1")


def change_password(frame_user_psw, password, registration_no):
    for widget in frame_user_psw.winfo_children():
        widget.destroy()
    old_password = ctk.CTkEntry(master=frame_user_psw, text_color="white", placeholder_text = "Old password")
    old_password.grid(row=0, column=0, padx=10, pady=10)
    new_password = ctk.CTkEntry(master=frame_user_psw, text_color="white", placeholder_text = "New password")
    new_password.grid(row=1, column=0, padx=10, pady=10)
    confirm = ctk.CTkButton(master=frame_user_psw, text = "Confirm", command=lambda: update_password(frame_user_psw, password, old_password, new_password, old_password.get(), new_password.get(), registration_no), width=50, cursor="hand2", fg_color="#00b300", hover_color="#009900", text_color="black")
    confirm.grid(row=0, column=1, rowspan=2, padx=10, pady=10)


def update_password(frame_user_psw, password, old_password_entry, new_password_entry, old_password, new_password, registration_no):
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
        cursor_update_pass.execute("update students set password='" + new_password + "'where registration_number=" + str(registration_no))
        conn.commit()
        cursor_update_pass.close()

def toggle_pswd(frame_user_psw, paswrd, password, eye_btn):
    global toggle
    if toggle == 0:
        eye_btn.destroy()
        eye_img = Image.open("eye_close4.png")
        eye_img = eye_img.resize((40, 30))
        eye_img = ImageTk.PhotoImage(eye_img)
        eye_open = Tk.Button(master=frame_user_psw, image = eye_img, command=lambda: toggle_pswd(frame_user_psw, paswrd, password, eye_open), borderwidth=0, bg="#292929", activebackground="#292929", cursor="hand2")
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
        eye_open = Tk.Button(master=frame_user_psw, image = eye_img, command=lambda: toggle_pswd(frame_user_psw, paswrd, password, eye_open), borderwidth=0, bg="#292929", activebackground="#292929", cursor="hand2")
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


def back_button():
    global first_input, first_user_menu, toggle
    if first_input == 1:
        first_input = 0
    if user_searches:
        user_searches.clear()
    if first_user_menu == 1:
        toggle = 0
        frame_user_menu.pack_forget()
        for widget in frame_user_menu.winfo_children():
            widget.destroy()
        first_user_menu = 0
    if zero_found.winfo_ismapped():
        zero_found.pack_forget()
    if not user_entry_frame.winfo_ismapped():
        user_entry_frame.pack(pady=(15, 0), padx=15, fill="both")
    if frame_show_books_details.winfo_ismapped():
        frame_show_books_details.pack_forget()
    if frame_show_books_buttons.winfo_ismapped():
        frame_show_books_buttons.pack_forget()
    latest_books.pack(padx=15, anchor="w")
    frame_show_books.pack(pady=15, padx=15, fill="both", expand=True)
    back_btn.grid_forget()
    logout_btn.grid(row=0, column=0, sticky="w", padx=15, pady=15)
    

def main_login():
    global first_input
    root_student.destroy()
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
        root_student.destroy()
        exit()