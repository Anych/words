import json
import random
from json import JSONDecodeError
from time import sleep
from tkinter import *
from PIL import ImageTk
import threading

from bin.english_dictionary import english_words


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
        with open('bin/dictionary.json', 'w') as f:
            json.dump(english_words, f)

        self.overrideredirect(True)
        self.attributes('-topmost', 'true')
        self.top_square = StringVar()
        self.bottom_square = StringVar()

        self.save_img = ImageTk.PhotoImage(file="save.ico")
        self.exit_img = ImageTk.PhotoImage(file="exit.ico")

        self.key = str()
        self.value = str()

        self.open_words()

        self.russian = Label(self, width=40, font=('arial', '14', 'bold'), bg='#f3cc5a', textvariable=self.top_square)
        self.english = Label(self, width=40, font=('arial', '14', 'bold'), textvariable=self.bottom_square)

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
        words = self.try_to_read_json('currently_learning')
        current_words_length = len(words)

        if current_words_length < 50:
            self.add_words_to_learning(current_words_length, words)

        self.next_word(words)
        self.set_word()

    def set_word(self):
        with open('bin/learned_from_russian.json', 'r') as f:
            words = json.load(f)
            if self.key in words.keys():
                self.top_square.set(self.key)
            else:
                self.top_square.set(self.value)

        thread = threading.Thread(target=self.english_translate)
        thread.start()

    def save_word(self):
        words = self.try_to_read_json('learned_from_russian')

        if self.key in words.keys():
            del words[self.key]
            self.remove_word_from_learning()
            learned_words = self.try_to_read_json('learned_words')
            learned_words[self.key] = self.value
            self.dump_json('learned_words', learned_words)

        else:
            words[self.key] = self.value

        self.dump_json('learned_from_russian', words)

        self.top_square.set('')
        self.bottom_square.set('Выучено')

    def try_to_read_json(self, file_name):
        with open(f'bin/{file_name}.json', 'r') as f:
            try:
                words = json.load(f)
            except JSONDecodeError:
                self.dump_json(file_name, {})
                words = json.load(f)

        return words

    def english_translate(self):
        sleep(5)
        if self.top_square.get() == self.key:
            self.bottom_square.set(self.value)
        else:
            self.bottom_square.set(self.key)
        sleep(5)
        self.bottom_square.set('')
        self.open_words()

    def add_words_to_learning(self, current_words_length, current_words):
        with open('bin/dictionary.json', 'r') as f:
            dictionary = json.load(f)
            while current_words_length < 50:
                self.next_word(dictionary)
                learned = self.try_to_read_json('learned_words')
                russian_learned = self.try_to_read_json('learned_from_russian')
                if self.key not in (current_words, russian_learned, learned):
                    current_words[self.key] = self.value
                else:
                    continue

                del dictionary[self.key]
                current_words_length += 1

        self.dump_json('dictionary', dictionary)

        self.dump_json('currently_learning', current_words)

    def next_word(self, dictionary):
        self.key = random.choice(list(dictionary.keys()))
        self.value = dictionary[self.key]

    def remove_word_from_learning(self):
        words = self.try_to_read_json('currently_learning')
        del words[self.key]
        self.dump_json('currently_learning', words)

    @staticmethod
    def dump_json(file_name, data):
        with open(f'bin/{file_name}.json', 'w') as f:
            json.dump(data, f)


if __name__ == '__main__':
    main = Main
    main()
