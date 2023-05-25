import customtkinter, os
from threading import Thread, Event
from PIL import Image
#import connection as conn

#import db_entry as _entry


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        #app default windows type/size
        self.title("LaDobleT.py")
        self.geometry("800x550")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        car_images_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imagenes_carros")
        self.company_logo = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "hauling-logo_black.png")),
                                                   dark_image=Image.open(os.path.join(image_path, "hauling-logo_white.png")), size=(65, 60))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.vehicle_data_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "datos_vehiculo_image.png")), size=(450, 120))
        self.entry_data_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "datos_entrada_image.png")), size=(450, 120))
        self.vehicles_label = customtkinter.CTkImage(Image.open(os.path.join(image_path, "vehiculos_label.png")), size=(450, 120))
        self.car1_image = customtkinter.CTkImage(Image.open(os.path.join(car_images_path, "accord.jpg")), size=(80, 80))
        self.services_label = customtkinter.CTkImage(Image.open(os.path.join(image_path, "services_label.png")), size=(450, 120))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.next_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "next_logo.png")), size=(20, 10))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.car_logo = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "car_logo_black.png")),
                                               dark_image=Image.open(os.path.join(image_path, "car_logo_white.png")), size=(26, 26))
        self.service_logo = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "service_logo_black.png")),
                                                   dark_image=Image.open(os.path.join(image_path, "service_logo_white.png")), size=(25, 20))


        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)


        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  La Doble T", image=self.company_logo,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

            #BOTON:  pestaña 1 (inicio) - donde estará el formulario para el registro
        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="  Inicio",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

            #BOTON:  pestaña 2 (Vehiculos) - donde apareceran los carros que hayan sido registrados
        self.vehicles_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Vehiculos",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.car_logo, anchor="w", command=self.vehicles_button_event)
        self.vehicles_button.grid(row=2, column=0, sticky="ew")

            #BOTON:  pestaña 3 (Servicios) - para mi es la principal, estará el registro de servicios
        self.services_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Servicios",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.service_logo, anchor="w", command=self.services_button_event)
        self.services_button.grid(row=3, column=0, sticky="ew")

            #No tiene importancia, es para poder elegir el tema o color de la app
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        #self.home_frame.grid_columnconfigure(1, weight=2)

        """self.home_frame_label = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame_label.grid_columnconfigure(1, weight=0)"""

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.entry_data_image, anchor="center")
        self.home_frame_large_image_label.grid(row=0, column=0, padx=15, pady=8)
        self.home_frame_large_image_label.grid_configure(columnspan=2)

        """self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)"""
            #menu para fabricantes - datos vehiculo
        self.optionmenu_fabricante = customtkinter.CTkComboBox(self.home_frame,
                                                        values=['fabricantes','fabricante_nombre'])
        self.optionmenu_fabricante.grid(row=1, column=0, padx=20, pady=(20, 10))
            #menu para años - datos vehiculo
        self.optionmenu_ano = customtkinter.CTkComboBox(self.home_frame,
                                                        values=['carros','fecha_de_creacion'])
        self.optionmenu_ano.grid(row=2, column=0, padx=20, pady=(20, 10))
            #menu para modelos - datos vehiculo
        self.optionmenu_modelo = customtkinter.CTkComboBox(self.home_frame,
                                                        values=['modelo_de_carro','modelo_nombre'])
        self.optionmenu_modelo.grid(row=3, column=0, padx=20, pady=(20, 10))
            #menu para color - datos vehiculo
        self.optionmenu_color = customtkinter.CTkComboBox(self.home_frame,
                                                        values=['carros','color'])
        self.optionmenu_color.grid(row=4, column=0, padx=20, pady=(20, 10))
            #menu para detalles del carro - datos vehiculo
        self.optionmenu_detalles = customtkinter.CTkComboBox(self.home_frame,
                                                        values=['carros','carro_detalles'])
        self.optionmenu_detalles.grid(row=1, column=1, padx=20, pady=(20, 10))
            #menu para la foto del carro - datos vehiculo
        self.photo_path_button = customtkinter.CTkButton(self.home_frame, text="Eliga la foto", image=self.image_icon_image, compound="right",
                                                        command=self.photo_path_button_event, fg_color="#95989B")#979da2
        self.photo_path_button.grid(row=4, column=1, padx=20, pady=20)
        self.photo_path_button.configure()
            #menu para nombre dueño - dueno_carro
        self.optionmenu_nombre = customtkinter.CTkComboBox(self.home_frame,
                                                        values=['dueno_carro','nombre'])
        self.optionmenu_nombre.grid(row=3, column=1, padx=20, pady=(20, 10))
            #menu para direccion dueño - dueno _carro
        self.optionmenu_direccion = customtkinter.CTkComboBox(self.home_frame,
                                                        values=['deuno_carro','direccion'])
        self.optionmenu_direccion.grid(row=2, column=1, padx=20, pady=(20, 10))
        #boton de guardar - datos vehiculo (guarda los datos del carro en variables, y pasa a la siguiente etapa del cuetionario - datos dueño)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="Guardar", image=self.next_image, compound="right",
                                                           font=("BOLD",16), command=self.home_vehicle_save_button_event)
        self.home_frame_button_2.grid(row=5, column=0, padx=20, pady=20)
        self.home_frame_button_2.grid_configure(columnspan=2)

        """    #menu para nombre del dueño - dueño_carrp
        self.optionmenu_nombre_dueno = customtkinter.CTkComboBox(self.home_frame,
                                                        values=self.connection_db.query_column_data_5pos('modelo_de_carro','modelo_nombre'))
        self.optionmenu_nombre_dueno.grid(row=3, column=0, padx=20, pady=(20, 10))
            #menu para direccion del dueño - dueño_carro
        self.optionmenu_dir_dueno = customtkinter.CTkComboBox(self.home_frame,
                                                        values=self.connection_db.query_column_data_5pos('carros','color'))
        self.optionmenu_dir_dueno.grid(row=4, column=0, padx=20, pady=(20, 10))"""


        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        #   data
        self.vehicles_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.vehicles_label, anchor="center")
        self.vehicles_frame_large_image_label.grid(row=0, column=0, padx=15, pady=8)
        self.vehicles_frame_large_image_label.grid_configure(columnspan=2)

        self.car1_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car1_image, anchor="center")
        self.car1_image_label.grid(row=1, column=0, padx=15, pady=8)

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.services_frame_large_image_label = customtkinter.CTkLabel(self.third_frame, text="", image=self.services_label, anchor="center")
        self.services_frame_large_image_label.grid(row=0, column=0, padx=15, pady=8)
        self.services_frame_large_image_label.grid_configure(columnspan=2)

        # select default frame
        self.select_frame_by_name("home")

        #select default scaling
        customtkinter.set_widget_scaling(1.2)
        customtkinter.set_appearance_mode("Dark")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.vehicles_button.configure(fg_color=("gray75", "gray25") if name == "vehicles" else "transparent")
        self.services_button.configure(fg_color=("gray75", "gray25") if name == "services" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "vehicles":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "services":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def vehicles_button_event(self):
        self.select_frame_by_name("vehicles")

    def services_button_event(self):
        self.select_frame_by_name("services")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "Dark":
            self.photo_path_button.configure(fg_color = "#565b5e")
        elif (new_appearance_mode == "Light"):
            self.photo_path_button.configure(fg_color = "#95989B")
        elif customtkinter.get_appearance_mode()== "Light":
            self.photo_path_button.configure(fg_color = "#95989B")
        else:
            self.photo_path_button.configure(fg_color = "#565b5e")

    def connection_thread(self):
        self.connection_db = conn.Conn()
        self.connection_db.establish_connection()

    def home_vehicle_save_button_event(self):
        print("\n\nSiguiente a datos del dueño' click")
        print("Se guardan los siguientes datos",
              "\nfabricante: ",self.optionmenu_fabricante.get(),
              "\nmodelo: ",self.optionmenu_modelo.get(),
              "\naño: ",self.optionmenu_ano.get(),
              "\ncolor: ",self.optionmenu_color.get())
        if self.entry.path_to_image==None:
            #mensaje = self.mesagebox(text='Agregue una foto',title="Error")
            pass


    def insert_vehicle_db(self):
        self.entry.fabricante_nombre = self.optionmenu_fabricante.get()
        self.entry.modelo_nombre = self.optionmenu_modelo.get()
        self.entry.fecha_de_creacion = self.optionmenu_ano.get()
        self.entry.carro_detalles = self.optionmenu_detalles.get()
        #self.entry.path_to_image = self.photo_path_button.get()
        self.entry.color = self.optionmenu_color.get()
        self.entry.nombre = self.optionmenu_nombre_dueno.get()
        self.entry.dueno_direccion = self.optionmenu_dir_dueno.get()

    def photo_path_button_event(self):
        self.entry.path_to_image = self.file_explorer.open_file()





if __name__ == "__main__":
    app = App()
    app.mainloop()

