import json
import random
from time import sleep
from tkinter import *
from PIL import ImageTk
import threading


class Main:

    def __init__(self):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.geometry('+500+300')

        label = Label(self.root, text='Слова бегом', width=20, font=('arial', '14', 'bold'))
        button1 = Button(self.root, text='Переводчик', width=15, font=('arial', '12'),
                         command=lambda: self.repeat())
        button2 = Button(self.root, text='Повторение', width=15, font=('arial', '12'),
                         command=lambda: self.repeat())
        button3 = Button(self.root, text='Выученные слова', width=15, font=('arial', '12'),
                         command=lambda: self.repeat())
        button4 = Button(self.root, text='Выход', width=15, font=('arial', '12'),
                         command=lambda: self.close())

        label.grid(row=0, column=0, columnspan=2)
        button1.grid(row=1, column=0)
        button2.grid(row=1, column=1)
        button3.grid(row=2, column=0)
        button4.grid(row=2, column=1)

        self.root.mainloop()

    def repeat(self):
        self.root.withdraw()
        Repeat()

    @staticmethod
    def close():
        exit()


class Repeat(Toplevel):

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self.attributes('-topmost', 'true')
        self.russian_txt = StringVar()
        self.english_txt = StringVar()

        self.save_img = ImageTk.PhotoImage(file="save.ico")
        self.exit_img = ImageTk.PhotoImage(file="exit.ico")

        self.key = str()
        self.value = str()

        self.open_words()

        self.russian = Label(self, width=40, font=('arial', '14', 'bold'), bg='#f3cc5a', textvariable=self.russian_txt)
        self.english = Label(self, width=40, font=('arial', '14', 'bold'), textvariable=self.english_txt)

        self.exit = Button(self, image=self.exit_img, relief='ridge', command=lambda: self.quit_pr())
        self.save = Button(self, image=self.save_img, relief='groove', command=lambda: self.save_word())

        self.russian.grid(row=0)
        self.english.grid(row=1)

        self.exit.place(relx=1, rely=0.01, anchor='ne')
        self.save.place(relx=1, rely=0.99, anchor='se')

        self.russian.bind("<ButtonPress-1>", self.start_move)
        self.russian.bind("<ButtonRelease-1>", self.stop_move)
        self.russian.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def quit_pr(self):
        self.destroy()

    def open_words(self):
        with open('learning.json', 'r') as f:
            data = json.load(f)
            while len(data) <= 50:
                with open('to_learn.json', 'r') as to_learn:
                    learn_data = json.load(to_learn)
                    self.key = random.choice(list(learn_data.keys()))
                    self.value = learn_data[self.key]
                    data[self.key] = self.value
                    learn_data.pop(self.key)
                with open('to_learn.json', 'w') as to_learn:
                    json.dump(learn_data, to_learn)
                with open('learning.json', 'w') as file:
                    json.dump(data, file)
            self.key = random.choice(list(data.keys()))
            self.value = data[self.key]
            self.russian_txt.set(self.value)
            thread = threading.Thread(target=self.english_translate)
            thread.start()

    def save_word(self):
        with open('learning.json', 'r') as learning:
            data = json.load(learning)
            data.pop(self.key)
        with open('learning.json', 'w') as qwerty:
            json.dump(data, qwerty)
        self.russian_txt.set('')
        self.english_txt.set('Выучено')

    def english_translate(self):
        sleep(5)
        self.english_txt.set(self.key)
        sleep(5)
        self.english_txt.set('')
        self.open_words()


if __name__ == '__main__':
    main = Main
    main()
