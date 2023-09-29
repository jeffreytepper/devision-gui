from nicegui import ui
from tkinter import filedialog
import easygui

# def choose_local_file():
#     try:
#         file = filedialog.askopenfilename()
#         print('click')
#         ui.input(label='Local File Path', value=f"{file}", placeholder='Local File Path', validation={'Input too long': lambda value: len(value) < 20})
#     except:
#         print('Error')
#         return

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
        self.train_filepath = ''
        self.test_filepath = ''

    def set_name(self, name):
        self.model_name = name

    def set_filepath(self, filepath):
        self.test_filepath = filepath

params = Params()

def choose_local_file():
    try:
        file = easygui.fileopenbox()
        ui.input(label='Local File Path', value=f"{file}", placeholder='Local File Path', validation={'Input too long': lambda value: len(value) < 20})
    except:
        print("ERROR WITH choose_local_file")
        return

#ui.button('Select training filepath').connect(lambda: ui.file_dialog(on_file_selected))

#Total Data: Sets the total amount of data. Default: total amount of images in the images folder.
total_data_silder = ui.slider(min=0, max=params.total_data, value=params.total_data)
ui.label().bind_text_from(total_data_silder, 'value')
#Dataset Size: Sets the size of the dataset to be used. Cannot be equal to total_data as there would be no testing data and the program will not work. Default: .75 of the total_data.
dataset_size_slider = ui.slider(min=0, max=params.total_data - 1, value=params.total_data // 1.333)
ui.label().bind_text_from(dataset_size_slider, 'value')
#Rays: Sets the number of Rays. Default: 32.
rays_slider = ui.slider(min=4, max=128, value=32)
ui.label().bind_text_from(rays_slider, 'value')
#Train Split: Sets the percent to split training/validation data. Default: .85.
train_split_slider = ui.slider(min=0.01, max=1.00, value=0.85, step=0.01)
ui.label().bind_text_from(train_split_slider, 'value')
#Testing Size: Sets the number of testing images. Default: 1 to ensure the program works.
testing_size_slider = ui.slider(min=1, max=params.total_data - 1, value=1)
ui.label().bind_text_from(testing_size_slider, 'value')
#Epochs: Sets the number of epochs. Accepts a number or list of numbers. E.g. --epochs 10 50 100 300. Default: 10.
epochs_slider = ui.slider(min=1, max=100, value=10)
ui.label().bind_text_from(epochs_slider, 'value')
#Model Name: Sets the name of the model. Accepts a string. Default: customModel
ui.input(label='Model Name', placeholder='customModel',
         on_change=lambda e: params.set_name(e.value))


#Add filepath
ui.button('Click me!', on_click=choose_local_file)

ui.run()