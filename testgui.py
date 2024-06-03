import tkinter as tk
from tkinter import ttk

class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.hello_label = ttk.Label(self, text='hello world!')
        self.hello_label.pack()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Test')
        self.geometry('400x400')

        self.mainframe = MainFrame(self)
        self.mainframe.pack()

    def click(self):
        print('click')

if __name__ == '__main__':
    app = App()
    app.mainloop()


