from tkinter import *
from tkinter import messagebox

import sqlite3

con = sqlite3.connect('Library.db')
cur = con.cursor()

class AddBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Добавить Книгу")
        self.resizable(False, False)


        ################### Рамки #########################

        #верхняя рамка
        self.topFrame = Frame(self, height = 150, bg = 'white')
        self.topFrame.pack(fill=X)

        #нижняя рамка
        self.bottomFrame = Frame(self, height = 600, bg = '#fcc324')
        self.bottomFrame.pack(fill=X)

        #заголовок, изображение
        self.top_image = PhotoImage(file = 'icons/add_book.png')
        top_image_lbl = Label(self.topFrame, image = self.top_image, bg = 'white')
        top_image_lbl.place(x = 120, y = 10)
        heading = Label(self.topFrame, text = '  Добавить книгу', font = 'arial 22 bold', fg = '#003f88', bg = 'white')
        heading.place(x = 290, y = 60)


        ######################### Ввод и его лейблы#########################
        self.lbl_title = Label(self.bottomFrame, text = "Название", font = 'arial 15 bold', fg = 'white', bg = '#fcc324')
        self.lbl_title.place(x=40, y=40)
        self.ent_title = Entry(self.bottomFrame, width = 31, bd = 4)
        self.ent_title.insert(0, 'Введите название книги')
        self.ent_title.place(x=300, y=45)
        #автор
        self.lbl_author = Label(self.bottomFrame, text="ФИО автора", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_author.place(x=40, y=80)
        self.ent_author = Entry(self.bottomFrame, width=31, bd=4)
        self.ent_author.insert(0, 'Введите ФИО автора')
        self.ent_author.place(x=300, y=85)
        #редактор
        self.lbl_publisher = Label(self.bottomFrame, text="Редактор", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_publisher.place(x=40, y=120)
        self.ent_publisher = Entry(self.bottomFrame, width=31, bd=4)
        self.ent_publisher.insert(0, 'Введите редактора')
        self.ent_publisher.place(x=300, y=125)
        #год издания
        self.lbl_year = Label(self.bottomFrame, text="Год издания", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_year.place(x=40, y=160)
        self.ent_year = Entry(self.bottomFrame, width=31, bd=4)
        self.ent_year.insert(0, 'Введите Год издания')
        self.ent_year.place(x=300, y=165)
        #кол-во страниц
        self.lbl_page = Label(self.bottomFrame, text="Количество страниц", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_page.place(x=40, y=200)
        self.ent_page = Entry(self.bottomFrame, width=31, bd=4)
        self.ent_page.insert(0, 'Введите количество страниц')
        self.ent_page.place(x=300, y=205)
        #кол-во экземпляров
        self.lbl_samples = Label(self.bottomFrame, text="Количество экземпляров", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_samples.place(x=40, y=240)
        self.ent_samples = Entry(self.bottomFrame, width=31, bd=4)
        self.ent_samples.insert(0, 'Введите Количество экземпляров')
        self.ent_samples.place(x=300, y=245)
        # кнопка
        button = Button(self.bottomFrame, text = 'Добавить книгу', command = self.addBook)
        button.place(x = 270, y = 280)

    def addBook(self):
        title = self.ent_title.get()
        if not self.ent_author.get():
            messagebox.showerror("Ошибка", "Поле не может быть пустым", icon='warning')
        author = self.ent_author.get().split() #Фио автора

        author_surname = author[0]
        author_name = author[1]
        try:
            author_fathersname = author[2]
        except:
            author_fathersname = 'unknown'

        #ищем автора
        author_id_query = f"""SELECT author_id FROM Authors 
                            WHERE first_name = ?
                            AND last_name = ?
                            AND fathers_name = ?
                        """

        author_id = cur.execute(author_id_query, (author_name, author_surname, author_fathersname,)).fetchone()
        if author_id:
            author_id = author_id[0]
        if not author_id:
            #добавляем автора если его еще нет
            query = f"""INSERT INTO 'Authors' (first_name, last_name, fathers_name)
                     SELECT * FROM (SELECT '{author_name}', '{author_surname}', '{author_fathersname}') AS temp 
                     WHERE NOT EXISTS (SELECT * FROM Authors WHERE first_name = '{author_name}'
                      AND last_name = '{author_surname}' AND fathers_name = '{author_fathersname}') LIMIT 1"""
            cur.execute(query)
            author_id_query = f"""SELECT author_id from Authors 
                    WHERE first_name = '{author_name}' 
                    AND last_name = '{author_surname}' 
                    AND fathers_name = '{author_fathersname}'"""
            author_id = cur.execute(author_id_query).fetchone()[0]

        publisher = self.ent_publisher.get()
        year = self.ent_year.get()
        page = self.ent_page.get()
        samples = self.ent_samples.get()
        if title and author_id and publisher and year and page and samples:
            try:
                query = """INSERT INTO 'Books' 
                (title, author_id, publisher, published_year, page_amount, samples_amount)
                 VALUES(?,?,?,?,?,?)"""
                cur.execute(query, (title, int(author_id), publisher, int(year), int(page), int(samples),))
                con.commit()
                messagebox.showinfo('Успешно', 'Успешно добавлено в БД', icon = 'info')

            except:
                messagebox.showerror("Ошибка", "Не получилось добавить в БД", icon = 'warning')
        else:
            messagebox.showerror("Ошибка", "Поле не может быть пустым", icon='warning')
