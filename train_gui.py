import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import os

from PIL import Image, ImageTk

from train import train

class InputFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.epochs = container.epochs
        self.rays = container.rays
        self.train_split = container.train_split
        self.model_name = container.model_name

        self.epochs_title_label = ttk.Label(self, text='Epochs')
        self.rays_title_label = ttk.Label(self, text='Rays')
        self.train_split_title_label = ttk.Label(self, text='Train Split')

        self.epochs_label = ttk.Label(self, text=self.epochs.get(), width=5)
        self.rays_label = ttk.Label(self, text=self.rays.get(), width=5)
        self.train_split_label = ttk.Label(self, text=self.train_split.get(), width=5)

        self.epochs_slider = ttk.Scale(self, from_=0, to=20, orient='horizontal', variable=self.epochs, command=self.update_label(self.epochs_label, self.epochs))
        self.rays_slider = ttk.Scale(self, from_=4, to=32, orient='horizontal', variable=self.rays, command=self.update_label(self.rays_label, self.rays))
        self.train_split_slider = ttk.Scale(self, from_=0.10, to=1.00, orient='horizontal', variable=self.train_split, command=self.update_label(self.train_split_label, self.train_split))

        self.name_frame = ttk.Frame(self)
        self.model_name_label = ttk.Label(self.name_frame, text='Model Name')
        self.model_name_entry = ttk.Entry(self.name_frame, textvariable=self.model_name)

        self.epochs_title_label.grid(row=0, column=0)
        self.epochs_slider.grid(row=0, column=1)
        self.epochs_label.grid(row=0, column=2)
        
        self.rays_title_label.grid(row=1, column=0)
        self.rays_slider.grid(row=1, column=1)
        self.rays_label.grid(row=1, column=2)

        self.train_split_title_label.grid(row=2, column=0)
        self.train_split_slider.grid(row=2, column=1)
        self.train_split_label.grid(row=2, column=2)

        self.name_frame.grid(row=3, column=0, columnspan=3, pady=10)
        self.model_name_label.pack(pady=2)
        self.model_name_entry.pack()

    def update_label(self, label, param):
        def update(e):
            value = param.get()

            label.config(text=round(param.get(),2))

        return update
    

class Slideshow(ttk.Frame):
    def __init__(self, container): 
        super().__init__(container)

        self.image_files = container.image_files
        self.mask_files = container.mask_files

        self.current_index = 0

        self.next_image_button = ttk.Button(self, text='Next', command=self.next_image)
        self.prev_image_button = ttk.Button(self, text='Prev', command=self.prev_image)

        self.image_base = ImageFrame(self)
        self.image_mask = ImageFrame(self)

        self.image_base.grid(row=0, column=0)
        self.image_mask.grid(row=0, column=1)

        self.prev_image_button.grid(row=1, column=0, pady=5, padx=2, sticky='e')
        self.next_image_button.grid(row=1, column=1, pady=5, padx=2, sticky='w')

    def next_image(self):
        self._to_index(self.current_index + 1)

    def prev_image(self):
        self._to_index(self.current_index - 1)

    def _to_index(self, index):
        self.current_index = index % len(self.image_files)
        self.update_image()

    def update_image(self):
        if self.image_files:
            image_path = self.image_files[self.current_index]
            self.image_base.set_image(image_path)
        if self.mask_files:
            mask_path = self.mask_files[self.current_index]
            self.image_mask.set_image(mask_path)
            print(image_path, mask_path)


class ImageFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container, height=200, width=200, borderwidth=5, relief='sunken')
        self.pack_propagate(0)

        self.image_label = ttk.Label(self)
        self.image_ref = None

        self.image_label.pack()

    def set_image(self, image_path):
        if image_path:
            tiff_image = Image.open(image_path).resize((200,200))
            self.image_ref = ImageTk.PhotoImage(tiff_image)
        else:
            self.image_ref = None
        
        self.image_label.config(image=self.image_ref)

    def erase_image(self):
        self.image_label.config(image=None)

class TrainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.image_files = []
        self.mask_files = []

        self.epochs = tk.IntVar(value=10)
        self.rays = tk.IntVar(value=32)
        self.train_split = tk.DoubleVar(value=0.15)
        self.model_name = tk.StringVar(value='custom_model')

        self.slideshow = Slideshow(self)
        self.inputframe = InputFrame(self)

        self.select_files_button = ttk.Button(self, text='Select Images', command=self.select_images)
        self.select_masks_button = ttk.Button(self, text='Select Masks', command=self.select_masks)
        self.train_button = ttk.Button(self, text='Train', state='disabled', command=self.train)

        self.select_files_button.grid(row=0, column=0, pady=25)
        self.select_masks_button.grid(row=0, column=1, pady=25)
        self.slideshow.grid(row=1, column=0, columnspan=2, pady=25, padx=25)
        self.train_button.grid(row=2, column=0, columnspan=2)
        self.inputframe.grid(row=3, column=0, columnspan=2, pady=10)


    def select_images(self):
        image_dir = filedialog.askdirectory(initialdir='/home/max/development/stardist/data/dsb2018/test/')
        self.image_files.extend([os.path.join(image_dir, file) for file in os.listdir(image_dir)])
        self.image_files.sort()
        self.slideshow.update_image()

        if self.image_files and self.mask_files:
            self.train_button.config(state='normal')

    def select_masks(self):
        mask_dir = filedialog.askdirectory(initialdir='/home/max/development/stardist/data/dsb2018/test/')
        self.mask_files.extend([os.path.join(mask_dir, file) for file in os.listdir(mask_dir)])
        self.mask_files.sort()
        self.slideshow.update_image()

        if self.image_files and self.mask_files:
            self.train_button.config(state='normal')

    def train(self):
        train(self.image_files, self.mask_files, train_split=self.train_split.get(), epochs=self.epochs.get(), rays=self.rays.get(), model_name=self.model_name.get())

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("trainer")
        self.geometry("600x600")

        self.mainframe = TrainFrame(self)
        self.mainframe.pack()

if __name__ ==  '__main__':
    app = App()
    app.mainloop()

