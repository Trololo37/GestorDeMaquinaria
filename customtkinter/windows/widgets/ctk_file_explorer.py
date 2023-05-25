    #este archivo nos permite interactuar con el file explorer de WINDOWS
    #va a servir para poder adjuntar las fotos y abrirlas

#import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image


class CTkFileExplorer():
    def __init__(self):
        self.file = None
        self.path_to_file = None
        self.file_name = None
        self.file_type = None
        self._initial_dir = "C:/Users/leona/OneDrive/Documentos/ESCUELA/UACH/6to SEMESTRE/Bases de Datos/LaDobleT/LaDobleT/imagenes_carros/"
        self._directory = "imagenes_carros"

    def open_file(self):
    # selecting the file using the askopenfilename() method of filedialog
        self.name = fd.askopenfile(
            title = "Select a file of any type",
            initialdir = self._initial_dir,
            filetypes = [("All Files", "*.jpg*"), ("All Files", "*.png*")]
            )
        self.path_to_file = self.name.name
        self.name_id()
        self.type_id()
        return self.path_to_file

    def display_image(self):
        img = Image.open(self.path_to_file)
        img.show()

    def name_id(self):
        self.file_name = self.path_to_file.replace(self._initial_dir, '')

    def type_id(self):
        lenght = len(self.file_name)
        index = lenght-4
        self.file_type = self.file_name[index:]





"""archivero = CTkFileExplorer()
archivero.open_file()
#archivero.display_image()
archivero.name_id()
archivero.type_id()"""
