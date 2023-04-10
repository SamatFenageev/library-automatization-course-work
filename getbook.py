from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import datetime

con = sqlite3.connect("Library.db")
cur = con.cursor()

class GetBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+220")
        self.title("Вернуть Книгу")
        self.resizable(False, False)

        query2 = """SELECT * FROM Readers WHERE reader_id IN 
                    (SELECT DISTINCT reader_id FROM Issuance WHERE return_date='')
                    """
        members = cur.execute(query2).fetchall()
        member_list = []
        for member in members:
            member_list.append(str(member[0]) + " - " + member[1] + " " + member[2] + " " + member[3])


        ################### Рамки #########################

        # верхняя рамка
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # нижняя рамка
        self.bottomFrame = Frame(self, height=600, bg='#fcc324')
        self.bottomFrame.pack(fill=X)

        # заголовок, изображение
        self.top_image = PhotoImage(file='icons/add_member.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=10)
        heading = Label(self.topFrame, text='Вернуть Книгу', font='arial 22 bold', fg='#003f88', bg='white')
        heading.place(x=290, y=60)

        ######################### вводы и лейблы #########################
        if members:
            # читатель
            self.member_name = StringVar()
            self.lbl_phone = Label(self.bottomFrame, text="№ читательского билета: ", font='arial 15 bold', fg='white',
                                   bg='#fcc324')
            self.lbl_phone.place(x=40, y=40)
            self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.member_name)
            self.combo_member['values'] = member_list
            self.combo_member.place(x=210, y=45)

            # книга
            self.book_name = StringVar()
            self.lbl_name = Label(self.bottomFrame, text="Название Книги: ", font='arial 15 bold', fg='white', bg='#fcc324')
            self.lbl_name.place(x=40, y=80)
            self.combo_name = ttk.Combobox(self.bottomFrame, textvariable = self.book_name, postcommand = self.findBookByReader)
            self.combo_name.place(x = 210, y = 85)

            # автор
            self.author_name = StringVar()
            self.lbl_author = Label(self.bottomFrame, text="ФИО автора: ", font='arial 15 bold', fg='white', bg='#fcc324')
            self.lbl_author.place(x=40, y=120)
            self.combo_author = ttk.Combobox(self.bottomFrame, textvariable=self.author_name, postcommand = self.findAuthorByBook)
            self.combo_author.place(x=210, y=125)


            # кнопка
            button = Button(self.bottomFrame, text='Вернуть Книгу', command = self.getBook)
            button.place(x=220, y=160)
        else:
            self.lbl_noissueance = Label(self.bottomFrame, text="Все Книги в библиотеке\nВозвращать нечего", font='arial 25 bold', fg='white',
                                  bg='#fcc324')
            self.lbl_noissueance.place(x=130, y=80)
    #TODO choose reader -> drop the borrowed books list -> return the book
    #сортим книги по читателю
    def findBookByReader(self):
        books_list = [""]
        if self.member_name.get():
            query = f"""
                    SELECT book_id, title FROM Books WHERE book_id IN (SELECT book_id FROM Issuance WHERE 
                    reader_id = {self.member_name.get()[0]} AND return_date = '')
                    """
            books = cur.execute(query).fetchall()
            for book in books:
                books_list.append(str(book[0]) + " - " + book[1])
        else:
            query = "SELECT * FROM Books"
            books = cur.execute(query).fetchall()
            for book in books:
                books_list.append(str(book[0]) + " - " + book[1])
        self.combo_name['values'] = books_list

    def findAuthorByBook(self):
        authors_list = [""]
        if self.book_name.get():
            query = f"""
                    SELECT author_id FROM Books WHERE book_id = {self.book_name.get().split()[0]}
                    """
            author_id = cur.execute(query).fetchone()[0]
            query2 = f"""
                        SELECT * FROM Authors WHERE author_id = {author_id}
                        """
            author = cur.execute(query2).fetchone()
            authors_list.append(str(author[0]) + " - " + author[1] + " " + author[3] + " " + author[2])
        else:
            query = "SELECT * FROM Authors"
            authors = cur.execute(query).fetchall()
            for author in authors:
                authors_list.append(str(author[0]) + " - " + author[1] + " " + author[3] + " " + author[2])
        self.combo_author['values'] = authors_list
    def getBook(self):
        book_name = self.book_name.get()
        self.book_id = book_name.split('-')[0]

        self.reader_id = self.member_name.get()[0]
        books_amount_query = f"""
                            SELECT samples_amount FROM Books WHERE book_id = {self.book_id}
                            """
        taken_amount_query = f"""
                                    SELECT taken_amount FROM Books WHERE
                                    book_id = {self.book_id}
                                    """
        taken_amount = cur.execute(taken_amount_query).fetchone()[0]
        samples_amount = cur.execute(books_amount_query).fetchone()[0]

        if self.book_id and self.reader_id and self.author_name.get():
            try:
                query = f"""
                        UPDATE Issuance SET return_date = '{str(datetime.date.today())}'
                        WHERE issuance_id IN (SELECT min(issuance_id) FROM Issuance 
                        WHERE return_date = '' AND reader_id = {self.reader_id} AND  book_id = {self.book_id}) 
                        """
                cur.execute(query)
                if samples_amount - taken_amount+1 > 0:
                    query3 = f"""
                            UPDATE Books SET book_status = 0
                            WHERE book_id = {self.book_id}
                        """
                    cur.execute(query3)

                query4 = f"""
                        UPDATE Books SET
                        taken_amount = {taken_amount - 1}
                        WHERE book_id = {self.book_id}
                        """
                cur.execute(query4)
                messagebox.showinfo("Успешно!", "Успешно добавлено в Базу Данных!")
                con.commit()
            except Exception as e:
                print(e)
                messagebox.showerror("Ошибка", "Не получилось добавить в Базу Данных")

        else:
            messagebox.showerror("Ошибка", "Нельзя оставлять поля пустыми")