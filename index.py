from nicegui import ui
from tkinter import filedialog
import os

from training import main

ui.label('Hello NiceGUI!')

class Params:
    def __init__(self):
        self.total_data = 180
        self.dataset_size = 1
        self.rays = 32
        self.train_split = .85
        self.testing_size = 1
        self.epochs = 10 
        self.model_name = "customModel"
        self.head_filepath = ''
        self.image_filepath = ''
        self.mask_filepath = ''
        self.output_filepath = ''

    def set_filepath(self):

        filepath = filedialog.askdirectory(
            initialdir='/home',
            title = 'select a directory',
        )

        self.head_filepath = filepath
        self.image_filepath = 'image path not found'
        self.mask_filepath = 'mask path not found'
        self.output_filepath = filepath

        for dir, subdirs, files in os.walk(filepath):
            if 'images' in subdirs:
                self.image_filepath = os.path.join(dir, 'images')
            if 'masks' in subdirs:
                self.mask_filepath = os.path.join(dir, 'masks')

        self.dataset_size = self.get_dataset_size()

    def get_dataset_size(self):
        size = len(os.listdir(self.image_filepath))
        if size == len(os.listdir(self.mask_filepath)):
            return size
        else:
            print("Error: files must contains the same number of elements")




params = Params()


#Add filepath
ui.button('Select filepath', on_click=params.set_filepath)
ui.label().bind_text_from(params, 'head_filepath')
ui.label().bind_text_from(params, 'image_filepath')
ui.label().bind_text_from(params, 'mask_filepath')

#Dataset Size: Sets the size of the dataset to be used. Cannot be equal to total_data as there would be no testing data and the program will not work. Default: .75 of the total_data.
dataset_size_slider = ui.slider(min=0, max=params.total_data - 1, value=params.total_data // 1.333).bind_value(params, 'dataset_size')
ui.label().bind_text_from(dataset_size_slider, 'value')
#Rays: Sets the number of Rays. Default: 32.
rays_slider = ui.slider(min=4, max=128, value=32).bind_value(params, 'rays')
ui.label().bind_text_from(rays_slider, 'value')
#Train Split: Sets the percent to split training/validation data. Default: .85.
train_split_slider = ui.slider(min=0.01, max=1.00, value=0.85, step=0.01).bind_value(params, 'train_split')
ui.label().bind_text_from(train_split_slider, 'value')
#Testing Size: Sets the number of testing images. Default: 1 to ensure the program works.
testing_size_slider = ui.slider(min=1, max=params.total_data - 1, value=1).bind_value(params, 'testing_size')
ui.label().bind_text_from(testing_size_slider, 'value')
#Epochs: Sets the number of epochs. Accepts a number or list of numbers. E.g. --epochs 10 50 100 300. Default: 10.
epochs_slider = ui.slider(min=1, max=100, value=10).bind_value(params, 'epochs')
ui.label().bind_text_from(epochs_slider, 'value')
#Model Name: Sets the name of the model. Accepts a string. Default: customModel
ui.input(label='Model Name', placeholder='customModel').bind_value(params, 'model_name')





ui.button('train model', on_click=lambda: main(params))

ui.run()