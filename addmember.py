from tkinter import *
from tkinter import messagebox
import re

import sqlite3

con = sqlite3.connect('Library.db')
cur = con.cursor()

class AddMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Добавить Читателя")
        self.resizable(False, False)


        ################### Рамки #########################

        #верхняя рамка
        self.topFrame = Frame(self, height = 150, bg = 'white')
        self.topFrame.pack(fill=X)

        #нижняя рамка
        self.bottomFrame = Frame(self, height = 600, bg = '#fcc324')
        self.bottomFrame.pack(fill=X)

        #заголовок, изображение
        self.top_image = PhotoImage(file = 'icons/add_member.png')
        top_image_lbl = Label(self.topFrame, image = self.top_image, bg = 'white')
        top_image_lbl.place(x = 120, y = 10)
        heading = Label(self.topFrame, text = '  Добавить читателя', font = 'arial 22 bold', fg = '#003f88', bg = 'white')
        heading.place(x = 290, y = 60)


        ######################### вводы и лейблы #########################
        #ФИО
        self.lbl_name = Label(self.bottomFrame, text = "ФИО", font = 'arial 15 bold', fg = 'white', bg = '#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.ent_name = Entry(self.bottomFrame, width = 30, bd = 4)
        self.ent_name.insert(0, 'Введите ФИО читателя')
        self.ent_name.place(x=150, y=45)
        # телефон
        self.lbl_phone = Label(self.bottomFrame, text="Телефон", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=80)
        self.ent_phone = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_phone.insert(0, 'Введите телефон с 79...')
        self.ent_phone.place(x=150, y=85)
        # адрес
        self.lbl_address = Label(self.bottomFrame, text="Адрес", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_address.place(x=40, y=120)
        self.ent_address = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_address.insert(0, 'Введите адрес')
        self.ent_address.place(x=150, y=125)

        # кнопка
        button = Button(self.bottomFrame, text = 'Добавить читателя', command = self.addMember)
        button.place(x = 200, y = 160)

    def addMember(self):
        if not (self.ent_name.get() and self.ent_address.get()):
            messagebox.showerror("Ошибка", "Поле не может быть пустым", icon='warning')
        reader = self.ent_name.get().split() # ФИО читателя
        reader_name = reader[0]
        reader_surname = reader[1]
        reader_fathersname = reader[2]

        phone = self.ent_phone.get()

        address = self.ent_address.get()

        query = f"""
            SELECT * FROM Readers WHERE first_name = '{reader_name}' AND
            last_name = '{reader_surname}' AND
            fathers_name = '{reader_fathersname}' AND 
            phone = '{phone}' AND 
            address = '{address}'
        """
        is_taken = cur.execute(query).fetchone()
        if is_taken:
            messagebox.showerror("Ошибка", "Пользователь уже существует", icon='warning')
        else:
            if reader_name and reader_surname and reader_fathersname and phone and address:
                try:
                    query = "INSERT INTO 'Readers' (first_name, last_name, fathers_name, phone, address) VALUES(?,?,?,?,?)"
                    cur.execute(query, (reader_name, reader_surname, reader_fathersname, phone, address,))
                    con.commit()
                    messagebox.showinfo('Успешно', 'Успешно добавлено в БД', icon = 'info')

                except Exception as e:
                    print(e)
                    messagebox.showerror("Ошибка", "Не получилось добавить в БД", icon = 'warning')
            else:
                messagebox.showerror("Ошибка", "Поле не может быть пустым", icon='warning')
