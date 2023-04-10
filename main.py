from tkinter import *
from tkinter import ttk
import sqlite3
import addBook, addmember, givebook, getbook
from tkinter import messagebox


con = sqlite3.connect("Library.db")
con.create_function('regexp', 2, lambda x, y: 1 if re.search(x,y) else 0)
cur = con.cursor()

class Main(object):
    def __init__(self, master):
        self.master = master
        def displayStatictics(evt):
            count_books = cur.execute("SELECT count(book_id) FROM Books").fetchall()
            count_members = cur.execute("SELECT count(reader_id) FROM Readers").fetchall()
            taken_books = cur.execute("SELECT taken_amount FROM Books").fetchall()
            samples_books = cur.execute("SELECT samples_amount FROM Books").fetchall()
            samples_amount = 0
            for i in samples_books:
                samples_amount += i[0]
            taken_amount = 0
            samples_amount = 0
            for i in samples_books:
                samples_amount += i[0]
            for i in taken_books:
                taken_amount += i[0]

            self.lbl_bookname_count.config(text = "Наименований Книг в Библиотеке: " + str(count_books[0][0]))
            self.lbl_book_count.config(text="Количество экземпляров в Библиотеке: " + str(samples_amount))
            self.lbl_member_count.config(text = "Всего Читателей: " + str(count_members[0][0]))
            self.lbl_taken_count.config(text = 'Взятых экземпляров: ' + str(taken_amount))
            displayBooks(self)
            displayMembers(self)

        def displayBooks(self):
            books = cur.execute("SELECT * FROM Books").fetchall()
            count = 0
            self.list_books.delete(0, END)
            for book in books:
                self.list_books.insert(count, str(book[0])+"-"+book[1])
                count += 1
            def bookInfo(event):
                value = str(self.list_books.get(self.list_books.curselection()))
                id = value.split('-')[0]
                book = cur.execute("SELECT * FROM Books WHERE book_id=?", (id,))
                book_info = book.fetchall()
                author_query = f"""SELECT first_name, last_name, fathers_name from Authors 
                    WHERE  author_id = {book_info[0][2]}"""
                author = cur.execute(author_query).fetchall()

                self.list_details.delete(0, 'end')
                self.list_details.insert(0, "Название Книги: " + book_info[0][1])
                self.list_details.insert(1, "Автор: " + author[0][0] + " " + author[0][2] + " " + author[0][1])
                self.list_details.insert(2, "Редактор: " + book_info[0][3])
                self.list_details.insert(3, "Год выпуска: " + str(book_info[0][4]))
                self.list_details.insert(5, "Количество страниц: " + str(book_info[0][6]))
                self.list_details.insert(6, "Количество доступных в библиотеке книг: " + str(book_info[0][7]-book_info[0][8]))


                if book_info[0][5] == 0:
                    self.list_details.insert(4, "Статус: Доступна")
                else:
                    self.list_details.insert(4, "Статус: Не Доступна")
            def doubleClick(evt):
                global given_id
                value = str(self.list_books.get(self.list_books.curselection()))
                given_id = value.split('-')[0]
                give_book = givebook.GiveBook()
            self.list_books.bind('<<ListboxSelect>>', bookInfo)
            self.tabs.bind('<<NotebookTabChanged>>', displayStatictics)
            #self.tabs.bind('<<ButtonRelease-1>>', displayBooks)
            self.list_books.bind('<Double-Button-1>', doubleClick)

        def displayMembers(self):
            members = cur.execute("SELECT * FROM Readers").fetchall()
            count = 0
            self.list_members.delete(0, END)
            for member in members:
                self.list_members.insert(count, str(member[0]) + "-" + member[1])
                count += 1

            def userInfo(event):
                value = str(self.list_members.get(self.list_members.curselection()))
                id = value.split('-')[0]
                member = cur.execute("SELECT * FROM Readers WHERE reader_id=?", (id,))
                member_info = member.fetchall()
                taken_books_query = f"""SELECT title FROM Books WHERE book_id IN 
                                (SELECT book_id FROM Issuance WHERE reader_id = {id} AND
                                return_date = '')
                                """
                taken_books = cur.execute(taken_books_query).fetchall()
                self.list_members_details.delete(0, 'end')
                self.list_members_details.insert(0, "читатель: " + member_info[0][1] + " " +  member_info[0][2] + " " +member_info[0][3])
                self.list_members_details.insert(1, "Телефон: " + member_info[0][4])
                self.list_members_details.insert(2, "Адрес: " + str(member_info[0][5]))
                self.list_members_details.insert(3, "Взятые книги: ")
                if taken_books:
                    index = 4
                    for book in taken_books:
                        self.list_members_details.insert(index, book[0])
                        index += 1


            self.list_members.bind('<<ListboxSelect>>', userInfo)

        #главная часть
        mainFrame = Frame(self.master)
        mainFrame.pack()

        #верхняя часть
        topFrame = Frame(mainFrame, width = 1350, height = 70, bg = '#f8f8f8', padx = 20, relief = SUNKEN, borderwidth = 2)
        topFrame.pack(side = TOP, fill = X)

        #центральная часть
        centerFrame = Frame(mainFrame, width = 1350, relief = RIDGE, bg = '#e0f0f0', height = 680)
        centerFrame.pack(side = TOP)

        #левая в центральной
        centerLeftFrame = Frame(centerFrame, width = 900, height = 700, bg = '#e0f0f0', borderwidth = 2, relief = 'sunken')
        centerLeftFrame.pack(side = LEFT)

        #правая в центральной
        centerRightFrame = Frame(centerFrame, width = 450, height = 700, bg = '#e0f0f0', borderwidth = 2, relief = 'sunken')
        centerRightFrame.pack()

        #поисковая строка
        searchBar = LabelFrame(centerRightFrame, width = 440, height = 175, text = 'Поиск', bg = '#9bc9ff')
        searchBar.pack(fill = BOTH)
        self.lbl_search = Label(searchBar, text = 'Поиск', font = 'arial 12 bold', bg = '#9bc9ff', fg = 'white')
        self.lbl_search.grid(row = 0, column = 0, padx = 20, pady = 10)
        self.ent_search = Entry(searchBar, width = 30, bd = 10)
        self.ent_search.grid(row = 0, column = 1, columnspan = 3, padx = 10, pady = 10)
        self.btn_search = Button(searchBar, text = 'Поиск', font = 'arial 12', bg = '#fcc324', fg = 'white',
                                 command = self.searchBooks)
        self.btn_search.grid(row = 0, column = 4, padx = 20, pady = 10)

        #список
        listBar = LabelFrame(centerRightFrame, width = 440, height = 175, text = 'Список', bg = '#fcc324')
        listBar.pack(fill = BOTH)
        lbl_list = Label(listBar, text = 'Отсортировать по:', font = 'times 16 bold', fg  = '#2488ff', bg = '#fcc324')
        lbl_list.grid(row = 0, column = 2)

        self.listChoice = IntVar()
        rb1 = Radiobutton(listBar, text = 'Все книги', var = self.listChoice, value = 1, bg = '#fcc324')
        rb2 = Radiobutton(listBar, text = 'В библиотеке', var = self.listChoice, value = 2, bg = '#fcc324')
        rb3 = Radiobutton(listBar, text = 'Взятые книги', var = self.listChoice, value = 3, bg = '#fcc324')
        rb1.grid(row = 1, column = 0)
        rb2.grid(row = 1, column = 1)
        rb3.grid(row = 1, column = 2)
        btn_list = Button(listBar, text = 'Список книг', bg = '#2488ff', fg = 'white', font = 'arial 12', command = self.listBooks)
        btn_list.grid(row = 1, column = 3, padx = 40, pady = 10)

        #заголовок и картинка
        image_bar = Frame(centerRightFrame, width = 440, height = 350)
        image_bar.pack(fill = BOTH)
        self.title_right = Label(image_bar, text = 'Добро пожаловать в Библиотеку', font = 'arial 16 bold')
        self.title_right.grid(row = 0)
        self.img_library = PhotoImage(file = 'icons/books.png')
        self.lblImg = Label(image_bar, image = self.img_library)
        self.lblImg.grid(row = 1)

########################### СТРОКА ИНСТРУМЕНТОВ ###################################

        #добавить книгу
        self.iconBook = PhotoImage(file = 'icons/add_book.png')
        self.btnBook = Button(topFrame, text = 'Добавить книгу', image = self.iconBook,
                              compound = LEFT, font = 'arial 12 bold', command = self.addBook)
        self.btnBook.pack(side = LEFT, padx = 10)

        #добавить читателя
        self.iconMember = PhotoImage(file = 'icons/add_member.png')
        self.btnMember = Button(topFrame, text = 'Добавить Читателя', font = 'arial 12 bold', padx = 10, command = self.addMember)
        self.btnMember.configure(image = self.iconMember, compound = LEFT)
        self.btnMember.pack(side = LEFT)

        #дать книгу
        self.iconGive = PhotoImage(file = 'icons/give_book.png')
        self.btnGive = Button(topFrame, text = 'Дать Книгу', font = 'arial 12 bold', padx = 10, image = self.iconGive, compound = LEFT, command = self.giveBook)
        self.btnGive.pack(side = LEFT)

        # вернуть книгу
        self.iconGet = PhotoImage(file='icons/give_book.png')
        self.btnGet = Button(topFrame, text='Вернуть Книгу', font='arial 12 bold', padx=10, image=self.iconGive, compound=LEFT, command=self.getBook)
        self.btnGet.pack(side=LEFT)

################################ Таблички #####################################

        self.tabs = ttk.Notebook(centerLeftFrame, width = 900, height = 660)
        self.tabs.pack()
        ######################## tab1 ############################
        self.tab1_icon = PhotoImage(file = 'icons/give_book.png')
        self.tab2_icon = PhotoImage(file = 'icons/give_book.png')
        self.tab3_icon = PhotoImage(file='icons/give_book.png')
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text = 'Управление библиотекой', image = self.tab1_icon, compound = LEFT)
        self.tabs.add(self.tab2, text = 'Статистика', image = self.tab2_icon, compound = LEFT)
        self.tabs.add(self.tab3, text='Читатели', image=self.tab2_icon, compound=LEFT)
        #список книг
        self.list_books = Listbox(self.tab1, width = 40, height = 30, bd = 5, font = 'times 12 bold')
        self.sb = Scrollbar(self.tab1, orient = VERTICAL)
        self.list_books.grid(row = 0, column = 0, padx = (10, 0), pady = 10, sticky = N)
        self.sb.config(command = self.list_books.yview)
        self.list_books.config(yscrollcommand = self.sb.set)
        self.sb.grid(row = 0, column = 0, sticky = N + S + E)

        self.list_members = Listbox(self.tab3, width=40, height=30, bd=5, font='times 12 bold')
        self.sb_members = Scrollbar(self.tab3, orient=VERTICAL)
        self.list_members.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=N)
        self.sb_members.config(command=self.list_members.yview)
        self.list_members.config(yscrollcommand=self.sb_members.set)
        self.sb_members.grid(row=0, column=0, sticky=N + S + E)
        self.list_members_details = Listbox(self.tab3, width=80, height=303, bd=5, font='times 12 bold')
        self.list_members_details.grid(row=0, column=1, padx=(10, 0), pady=10, sticky=N)

        #описание книги
        self.list_details = Listbox(self.tab1, width = 80, height = 303, bd = 5, font = 'times 12 bold')
        self.list_details.grid(row = 0, column = 1, padx = (10,0), pady = 10, sticky = N)

        ########################### tab2 ###########################
        #статистика
        self.lbl_bookname_count = Label(self.tab2, text = '', pady = 20, font = 'verdana 14 bold')
        self.lbl_bookname_count.grid(row = 0)
        self.lbl_book_count = Label(self.tab2, text='', pady=20, font='verdana 14 bold')
        self.lbl_book_count.grid(row=1, sticky = W)
        self.lbl_member_count = Label(self.tab2, text = '', pady = 20, font = 'verdana 14 bold')
        self.lbl_member_count.grid(row = 2, sticky = W)
        self.lbl_taken_count = Label(self.tab2, text = '', pady = 20, font = 'verdana 14 bold')
        self.lbl_taken_count.grid(row = 3, sticky = W)

        self.list_members = Listbox(self.tab3, width=40, height=30, bd=5, font='times 12 bold')
        self.sb_members = Scrollbar(self.tab3, orient=VERTICAL)
        self.list_members.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=N)
        self.sb_members.config(command=self.list_members.yview)
        self.list_members.config(yscrollcommand=self.sb_members.set)
        self.sb_members.grid(row=0, column=0, sticky=N + S + E)
        self.list_members_details = Listbox(self.tab3, width=80, height=303, bd=5, font='times 12 bold')
        self.list_members_details.grid(row=0, column=1, padx=(10, 0), pady=10, sticky=N)

        #функции
        displayBooks(self)
        displayStatictics(self)
        displayMembers(self)
    def addBook(self):
        add = addBook.AddBook()
    def addMember(self):
        member = addmember.AddMember()
    def searchBooks(self):
        value = self.ent_search.get()
        search = cur.execute("SELECT * FROM Books WHERE title LIKE ?", ('%'+value+'%',)).fetchall()

        self.list_books.delete(0, END)
        count = 0
        for book in search:
            self.list_books.insert(count, str(book[0]) + '-' + book[1])
            count += 1
    def listBooks(self):
        value = self.listChoice.get()
        if value == 1:
            allBooks = cur.execute('SELECT * FROM Books').fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in allBooks:
                self.list_books.insert(count, str(book[0]) + ' - '+book[1])
                count += 1
        elif value == 2:
            books_in_library = cur.execute("SELECT * FROM Books WHERE book_status = ?",(0,)).fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in books_in_library:
                self.list_books.insert(count, str(book[0]) + ' - ' + book[1])
                count += 1
        else:

            taken_books = cur.execute("SELECT * FROM Books WHERE book_status = ?",(1,)).fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in taken_books:
                self.list_books.insert(count, str(book[0]) + ' - ' + book[1])
                count += 1
    def getBook(self):
        get_book = getbook.GetBook()
    def giveBook(self):
        give_book = givebook.GiveBook()



def main():
    root = Tk()
    app = Main(root)
    root.title("Library")
    root.geometry("1350x750+350+200")
    root.iconbitmap() #иконки
    root.mainloop()
if __name__ == "__main__":
    main()