import customtkinter, os
import datetime
from threading import Thread, Event
from PIL import Image

#import connection as conn
from basedatos import connection as conn
from basedatos import db_entry as _entry
#import db_entry as _entry


#un boton en la interfaz principal para elegir el tipo de servicio requerido directamente
#en la parte de vehiculos deberan aparecer los servicios que se van registrando, con el ultimo servicio que se les realizo
#y en la parte de servicios deberan aparecer los servicios pendientes, con un boton para eliminiar (o marcar como hechos) los servicios que ya fueron realizados

"""
#
#
#
#
#               SE VA A QUEDAR PENDIENTE QUE ACTUALICE LOS MODELOS AL SELECCIONAR EL FABRICANTE
#               Y QUE ACTUALICE LA DIRECCION DEL CLIENTE AL SELECCIONAL EL DUEÑO
#
#
#
#
"""


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #connection data
        self.connection_db = None
        self._conn_thread = Thread(target=self.connection_thread())
        self._conn_thread.start()

        #data to db entries
        self.entry = _entry.db_entry(self.connection_db)

        #app default windows type/size
        self.title("LaDobleT.py")
        self.geometry("800x550")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.car_images_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imagenes_carros")
        self.company_logo = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "hauling-logo_black.png")),
                                                   dark_image=Image.open(os.path.join(image_path, "hauling-logo_white.png")), size=(65, 60))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.vehicle_data_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "datos_vehiculo_image.png")), size=(450, 120))
        self.entry_data_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "datos_entrada_image.png")), size=(450, 120))
        self.vehicles_label = customtkinter.CTkImage(Image.open(os.path.join(image_path, "vehiculos_label.png")), size=(450, 120))
        self.services_label = customtkinter.CTkImage(Image.open(os.path.join(image_path, "services_label.png")), size=(450, 120))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.next_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "next_logo.png")), size=(20, 10))
        self.previous_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "previous_logo.png")), size=(20, 10))
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
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")



        """


        TODo ESTO ES PARA EL HOME FRAME, O DONDE SE AGREGAN LOS VEHICULOS




        """

        #                   HOMEFRAME

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(1, weight=2)
        self.home_frame.grid_columnconfigure(0, weight=2)
        self.home_frame.grid_rowconfigure(0, weight=2)
        self.home_frame.grid_rowconfigure(1, weight=2)
        self.home_frame.grid_rowconfigure(2, weight=2)
        self.home_frame.grid_rowconfigure(3, weight=2)
        self.home_frame.grid_rowconfigure(4, weight=2)
        self.home_frame.grid_rowconfigure(5, weight=2)

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

        """ #OJO



             Si se quita lo de sticky, cambian completamente la forma de los botones
             Tambien se deberán quitar los pesos en la configuracion del frame



        """

        self.combobox_fabricante = customtkinter.CTkComboBox(self.home_frame,
                                                        values=self.connection_db.query_column_data_5pos('fabricantes','fabricante_nombre'))
        self.combobox_fabricante.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.combobox_fabricante.set("Seleccione Marca")
        self.combobox_fabricante.configure(font=("normal",12))
        #self.combobox_fabricante.bind('<<ComboboxSelected>>', self.combobox_fabricante_event)
        #self.combobox_fabricante.configure(command=self.combobox_fabricante_event)
            #menu para años - datos vehiculo
        self.combobox_ano = customtkinter.CTkComboBox(self.home_frame,
                                                        values=self.connection_db.query_column_data_5pos_years('carros','fecha_de_creacion'))
        self.combobox_ano.grid(row=2, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.combobox_ano.set("Seleccione Año")
        self.combobox_ano.configure(font=("normal",12))
        #self.combobox_ano.configure(command=self.combobox_ano_event)
            #menu para modelos - datos vehiculo
        self.combobox_modelo = customtkinter.CTkComboBox(self.home_frame,
                                                        values=self.connection_db.query_column_data_5pos('modelo_de_carro','modelo_nombre'))
        self.combobox_modelo.grid(row=3, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.combobox_modelo.set("Seleccione Modelo")
        self.combobox_modelo.configure(font=("normal",12))
        #self.combobox_modelo.configure(command=self.combobox_modelo_event)
            #menu para color - datos vehiculo
        self.combobox_color = customtkinter.CTkComboBox(self.home_frame,
                                                        values=self.connection_db.query_column_data_5pos('carros','color'))
        self.combobox_color.grid(row=4, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.combobox_color.set("Seleccione Color")
        self.combobox_color.configure(font=("normal",12))
        #self.combobox_color.configure(command=self.combobox_color_event)
            #menu para detalles del carro - datos vehiculo
        self.combobox_detalles = customtkinter.CTkComboBox(self.home_frame,
                                                        values=self.connection_db.query_column_data_5pos('carros','carro_detalles'))
        self.combobox_detalles.grid(row=1, column=1, padx=20, pady=(20, 10), sticky="ew")
        self.combobox_detalles.set("Escriba los detalles")
        self.combobox_detalles.configure(font=("normal",12))
        #self.combobox_detalles.configure(command=self.combobox_detalles_event)
            #menu para la foto del carro - datos vehiculo
        self.photo_path_button = customtkinter.CTkButton(self.home_frame, text="Eliga la foto", image=self.image_icon_image, compound="right",
                                                        command=self.photo_path_button_event, fg_color="#95989B")#979da2
        self.photo_path_button.grid(row=2, column=1, padx=20, pady=(20, 10), sticky="ew")
        self.photo_path_button.configure(font=("normal",12))
        #self.photo_path_button.configure()
            #menu para nombre dueño - dueno_carro
        self.combobox_nombre = customtkinter.CTkComboBox(self.home_frame,
                                                        values=self.connection_db.query_column_data_5pos('dueno_carro', 'nombre'))
        self.combobox_nombre.bind(self.combobox_nombre, self.update_combobox_direccion)
        self.combobox_nombre.grid(row=3, column=1, padx=20, pady=(20, 10), sticky="ew")
        self.combobox_nombre.set("Nombre del Dueño")
        self.combobox_nombre.configure(font=("normal",12))
        #self.combobox_nombre.configure(command=self.combobox_nombre_event)
            #menu para direccion dueño - dueno _carro
        self.combobox_direccion = customtkinter.CTkComboBox(self.home_frame,
                                                              values=self.connection_db.query_column_data_5pos('dueno_carro', 'dueno_direccion'))
        self.combobox_direccion.grid(row=4, column=1, padx=20, pady=(20, 10), sticky="ew")
        self.combobox_direccion.set("Direccion del dueño")
        self.combobox_direccion.configure(font=("normal",12))
        #self.combobox_direccion.configure(command=self.combobox_direccion_event)

        #boton de guardar - datos vehiculo (guarda los datos del carro en variables, y pasa a la siguiente etapa del cuetionario - datos dueño)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="Guardar", image=self.next_image, compound="right",
                                                           font=("BOLD",15), command=self.home_vehicle_save_button_event)
        self.home_frame_button_2.grid(row=5, column=0, padx=20, pady=20, sticky="ew")
        self.home_frame_button_2.grid_configure(columnspan=2)

        """    #menu para nombre del dueño - dueño_carrp
        self.combobox_nombre_dueno = customtkinter.CTkComboBox(self.home_frame,
                                                        values=self.connection_db.query_column_data_5pos('modelo_de_carro','modelo_nombre'))
        self.combobox_nombre_dueno.grid(row=3, column=0, padx=20, pady=(20, 10))
            #menu para direccion del dueño - dueño_carro
        self.combobox_dir_dueno = customtkinter.CTkComboBox(self.home_frame,
                                                        values=self.connection_db.query_column_data_5pos('carros','color'))
        self.combobox_dir_dueno.grid(row=4, column=0, padx=20, pady=(20, 10))"""




        """


        TODo ESTO ES PARA EL SECOND FRAME, O DONDE SE MUESTRAN LOS VEHICULOS




        """


        #                   VEHICLES FRAME

        # create second frame
        self.second_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(1, weight=2)
        self.second_frame.grid_rowconfigure(4, weight=2)

        self.second_second_frame = customtkinter.CTkFrame(self.second_frame, corner_radius=0, fg_color="transparent")
        self.second_second_frame.grid(row=4, column=1)

        #self.second_frame_scrollbar = customtkinter.CTkScrollableFrame(self.second_frame, command=self.second_frame.yview)
        #self.second_frame.configure(yscrollcommand=self.second_frame_scrollbar.set)


        self.second_frame_page = 0 #Esta variable nos dice la pagina en la que se encuentra
        self.second_frame_next_page_button = customtkinter.CTkButton(self.second_second_frame, text="Siguiente Página", image=self.next_image, compound="right",
                                                           font=("BOLD",15), command=self.vehicle_frame_next_page)
        self.second_frame_next_page_button.grid(row=0, column=1, padx=20, pady=20, sticky="nse")
        self.second_frame_previous_page_button = customtkinter.CTkButton(self.second_second_frame, text="Página Anterior", image=self.previous_image, compound="left",
                                                           font=("BOLD",15), command=self.vehicle_frame_previous_page)
        self.second_frame_previous_page_button.grid(row=0, column=0, padx=20, pady=20, sticky="nsw")

        #   label
        self.vehicles_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.vehicles_label, anchor="center")
        self.vehicles_frame_large_image_label.grid(row=0, column=0, padx=15, pady=8)
        self.vehicles_frame_large_image_label.grid_configure(columnspan=2)

        #Aqui se reclama toda la informacion de los vehiculos al arbir la app
        self.get_vehicle_frame_data()

        #Esto es para darle formato una vez se crea, ya que con el scrollableframe, pierde la geometria predefinida
        self.geometry("900x600")





        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.services_frame_large_image_label = customtkinter.CTkLabel(self.third_frame, text="", image=self.services_label, anchor="center")
        self.services_frame_large_image_label.grid(row=0, column=0, padx=15, pady=8)
        self.services_frame_large_image_label.grid_configure(columnspan=2)

        self.get_services_frame_data()





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
        else:
            self.photo_path_button.configure(fg_color = "#95989B")

    def get_vehicle_frame_data(self):
        self.carros_lib = self.connection_db.raw_manual_query("select carro_id, fecha_de_creacion, color, fabricante_id, carro_detalles, modelo_carro_id, dueno_id, path_to_image from carros")
        self.carros_in_page = self.carros_lib[:3]
        self.second_frame_page = 0
        for i in range (0,3):
            if i==0:
                #   car1 image
                self.car1_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car1_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car1_image, anchor="center")
                self.car1_image_label.grid(row=1, column=0, padx=15, pady=8, sticky="e")
                #   car1 data
                self.car1_label = customtkinter.CTkLabel(self.second_frame, text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car1_label.grid(row=1, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car1_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car1_data_text.grid(row=1, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car1_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[1][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))
            elif i==1:
                #   car2 image
                self.car2_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car2_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car2_image, anchor="center")
                self.car2_image_label.grid(row=2, column=0, padx=15, pady=8, sticky="e")
                #   car2 data
                self.car2_label = customtkinter.CTkLabel(self.second_frame,  text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car2_label.grid(row=2, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car2_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car2_data_text.grid(row=2, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car2_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[1][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))
            elif i==2:
                #   car3 image
                self.car3_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car3_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car3_image, anchor="center")
                self.car3_image_label.grid(row=3, column=0, padx=15, pady=8, sticky="e")
                #   car3 data
                self.car3_label = customtkinter.CTkLabel(self.second_frame, text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car3_label.grid(row=3, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car3_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car3_data_text.grid(row=3, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car3_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[1][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))

    def vehicle_frame_next_page(self):
        self.carros_lib = self.connection_db.raw_manual_query("select carro_id, fecha_de_creacion, color, fabricante_id, carro_detalles, modelo_carro_id, dueno_id, path_to_image from carros")
        if (((self.second_frame_page * 3) +4) > len(self.carros_lib)):
            return
        self.second_frame_page += 1
        self.carros_in_page.clear()
        self.carros_in_page = self.carros_lib[self.second_frame_page*3:(self.second_frame_page*3)+3]
        self.number_of_carros_in_page=len(self.carros_in_page)
        if self.number_of_carros_in_page==1:
            self.car2_image = ""
            self.car2_image_label.destroy()
            self.car2_label.destroy()
            self.car2_data_text.destroy()
            self.car3_image = ""
            self.car3_image_label.destroy()
            self.car3_label.destroy()
            self.car3_data_text.destroy()
        elif self.number_of_carros_in_page == 2:
            self.car3_image = None
            self.car3_image_label.destroy()
            self.car3_label.destroy()
            self.car3_data_text.destroy()

        for i in range (self.number_of_carros_in_page):
            if i==0:
                #   car1 image
                self.car1_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[0][7])), size=(80, 80))
                self.car1_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car1_image, anchor="center")
                self.car1_image_label.grid(row=1, column=0, padx=15, pady=8, sticky="e")
                #   car1 data
                self.car1_label = customtkinter.CTkLabel(self.second_frame, text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[0][3])[0])))
                self.car1_label.grid(row=1, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car1_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car1_data_text.grid(row=1, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car1_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[0][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[0][1]).year),
                                                                                                                                                 self.carros_in_page[0][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[0][6])[0],
                                                                                                                                                 self.carros_in_page[0][4])))
            elif i==1:
                #   car2 image
                self.car2_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car2_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car2_image, anchor="center")
                self.car2_image_label.grid(row=2, column=0, padx=15, pady=8, sticky="e")
                #   car2 data
                self.car2_label = customtkinter.CTkLabel(self.second_frame,  text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car2_label.grid(row=2, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car2_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car2_data_text.grid(row=2, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car2_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[i][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))
            elif i==2:
                #   car3 image
                self.car3_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car3_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car3_image, anchor="center")
                self.car3_image_label.grid(row=3, column=0, padx=15, pady=8, sticky="e")
                #   car3 data
                self.car3_label = customtkinter.CTkLabel(self.second_frame, text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car3_label.grid(row=3, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car3_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car3_data_text.grid(row=3, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car3_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[1][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))

    def vehicle_frame_previous_page(self):
        self.carros_lib = self.connection_db.raw_manual_query("select carro_id, fecha_de_creacion, color, fabricante_id, carro_detalles, modelo_carro_id, dueno_id, path_to_image from carros")
        if self.second_frame_page == 0:
            return
        self.second_frame_page -= 1
        self.carros_in_page.clear()
        self.carros_in_page = self.carros_lib[self.second_frame_page*3:(self.second_frame_page*3)+3]
        for i in range (0,3):
            if i==0:
                #   car1 image
                self.car1_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car1_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car1_image, anchor="center")
                self.car1_image_label.grid(row=1, column=0, padx=15, pady=8, sticky="e")
                #   car1 data
                self.car1_label = customtkinter.CTkLabel(self.second_frame, text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car1_label.grid(row=1, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car1_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car1_data_text.grid(row=1, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car1_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[1][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))
            elif i==1:
                #   car2 image
                self.car2_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car2_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car2_image, anchor="center")
                self.car2_image_label.grid(row=2, column=0, padx=15, pady=8, sticky="e")
                #   car2 data
                self.car2_label = customtkinter.CTkLabel(self.second_frame,  text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car2_label.grid(row=2, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car2_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car2_data_text.grid(row=2, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car2_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[1][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))
            elif i==2:
                #   car3 image
                self.car3_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car3_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car3_image, anchor="center")
                self.car3_image_label.grid(row=3, column=0, padx=15, pady=8, sticky="e")
                #   car3 data
                self.car3_label = customtkinter.CTkLabel(self.second_frame, text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car3_label.grid(row=3, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car3_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car3_data_text.grid(row=3, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car3_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[1][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))

    def get_services_frame_data(self):
        self.servicios_lib = self.connection_db.raw_manual_query("select carro_id, fecha_de_creacion, color, fabricante_id, carro_detalles, modelo_carro_id, dueno_id, path_to_image from carros")
        self.servicios_in_page = self.servicios_lib[:3]
        self.third_frame_page = 0
        for i in range (0,3):
            if i==0:
                #   car1 image
                self.service1_car_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.servicios_in_page[i][7])), size=(80, 80))
                self.service1_car_label = customtkinter.CTkLabel(self.third_frame, text="", image=self.car1_image, anchor="center")
                self.service1_car_label.grid(row=1, column=0, padx=15, pady=8, sticky="e")
                #   car1 data
                self.car1_label = customtkinter.CTkLabel(self.third_frame, text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.servicios_in_page[i][3])[0])))
                self.car1_label.grid(row=1, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car1_data_text = customtkinter.CTkTextbox(self.third_frame, height=90, width=100)
                self.car1_data_text.grid(row=1, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car1_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.servicios_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[1][1]).year),
                                                                                                                                                 self.servicios_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.servicios_in_page[i][6])[0],
                                                                                                                                                 self.servicios_in_page[i][4])))
            elif i==1:
                #   car2 image
                self.car2_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.servicios_in_page[i][7])), size=(80, 80))
                self.car2_image_label = customtkinter.CTkLabel(self.third_frame, text="", image=self.car2_image, anchor="center")
                self.car2_image_label.grid(row=2, column=0, padx=15, pady=8, sticky="e")
                #   car2 data
                self.car2_label = customtkinter.CTkLabel(self.third_frame,  text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.servicios_in_page[i][3])[0])))
                self.car2_label.grid(row=2, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car2_data_text = customtkinter.CTkTextbox(self.third_frame, height=90, width=100)
                self.car2_data_text.grid(row=2, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car2_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.servicios_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.servicios_in_page[1][1]).year),
                                                                                                                                                 self.servicios_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.servicios_in_page[i][6])[0],
                                                                                                                                                 self.servicios_in_page[i][4])))
            elif i==2:
                #   car3 image
                self.car3_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.servicios_in_page[i][7])), size=(80, 80))
                self.car3_image_label = customtkinter.CTkLabel(self.third_frame, text="", image=self.car3_image, anchor="center")
                self.car3_image_label.grid(row=3, column=0, padx=15, pady=8, sticky="e")
                #   car3 data
                self.car3_label = customtkinter.CTkLabel(self.third_frame, text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.servicios_in_page[i][3])[0])))
                self.car3_label.grid(row=3, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car3_data_text = customtkinter.CTkTextbox(self.third_frame, height=90, width=100)
                self.car3_data_text.grid(row=3, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car3_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.servicios_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.servicios_in_page[1][1]).year),
                                                                                                                                                 self.servicios_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.servicios_in_page[i][6])[0],
                                                                                                                                                 self.servicios_in_page[i][4])))

    def services_frame_next_page(self):
        self.carros_lib = self.connection_db.raw_manual_query("select carro_id, fecha_de_creacion, color, fabricante_id, carro_detalles, modelo_carro_id, dueno_id, path_to_image from carros")
        if (((self.second_frame_page * 3) +4) > len(self.carros_lib)):
            return
        self.second_frame_page += 1
        self.carros_in_page.clear()
        self.carros_in_page = self.carros_lib[self.second_frame_page*3:(self.second_frame_page*3)+3]
        self.number_of_carros_in_page=len(self.carros_in_page)
        if self.number_of_carros_in_page==1:
            self.car2_image = ""
            self.car2_image_label.destroy()
            self.car2_label.destroy()
            self.car2_data_text.destroy()
            self.car3_image = ""
            self.car3_image_label.destroy()
            self.car3_label.destroy()
            self.car3_data_text.destroy()
        elif self.number_of_carros_in_page == 2:
            self.car3_image = None
            self.car3_image_label.destroy()
            self.car3_label.destroy()
            self.car3_data_text.destroy()

        for i in range (self.number_of_carros_in_page):
            if i==0:
                #   car1 image
                self.car1_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[0][7])), size=(80, 80))
                self.car1_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car1_image, anchor="center")
                self.car1_image_label.grid(row=1, column=0, padx=15, pady=8, sticky="e")
                #   car1 data
                self.car1_label = customtkinter.CTkLabel(self.second_frame, text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[0][3])[0])))
                self.car1_label.grid(row=1, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car1_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car1_data_text.grid(row=1, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car1_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[0][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[0][1]).year),
                                                                                                                                                 self.carros_in_page[0][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[0][6])[0],
                                                                                                                                                 self.carros_in_page[0][4])))
            elif i==1:
                #   car2 image
                self.car2_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car2_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car2_image, anchor="center")
                self.car2_image_label.grid(row=2, column=0, padx=15, pady=8, sticky="e")
                #   car2 data
                self.car2_label = customtkinter.CTkLabel(self.second_frame,  text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car2_label.grid(row=2, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car2_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car2_data_text.grid(row=2, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car2_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[i][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))
            elif i==2:
                #   car3 image
                self.car3_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car3_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car3_image, anchor="center")
                self.car3_image_label.grid(row=3, column=0, padx=15, pady=8, sticky="e")
                #   car3 data
                self.car3_label = customtkinter.CTkLabel(self.second_frame, text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car3_label.grid(row=3, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car3_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car3_data_text.grid(row=3, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car3_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[1][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))

    def services_frame_previous_page(self):
        self.carros_lib = self.connection_db.raw_manual_query("select carro_id, fecha_de_creacion, color, fabricante_id, carro_detalles, modelo_carro_id, dueno_id, path_to_image from carros")
        if self.second_frame_page == 0:
            return
        self.second_frame_page -= 1
        self.carros_in_page.clear()
        self.carros_in_page = self.carros_lib[self.second_frame_page*3:(self.second_frame_page*3)+3]
        for i in range (0,3):
            if i==0:
                #   car1 image
                self.car1_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car1_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car1_image, anchor="center")
                self.car1_image_label.grid(row=1, column=0, padx=15, pady=8, sticky="e")
                #   car1 data
                self.car1_label = customtkinter.CTkLabel(self.second_frame, text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car1_label.grid(row=1, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car1_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car1_data_text.grid(row=1, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car1_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[1][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))
            elif i==1:
                #   car2 image
                self.car2_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car2_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car2_image, anchor="center")
                self.car2_image_label.grid(row=2, column=0, padx=15, pady=8, sticky="e")
                #   car2 data
                self.car2_label = customtkinter.CTkLabel(self.second_frame,  text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car2_label.grid(row=2, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car2_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car2_data_text.grid(row=2, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car2_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[1][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))
            elif i==2:
                #   car3 image
                self.car3_image = customtkinter.CTkImage(Image.open(os.path.join(self.car_images_path, self.carros_in_page[i][7])), size=(80, 80))
                self.car3_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.car3_image, anchor="center")
                self.car3_image_label.grid(row=3, column=0, padx=15, pady=8, sticky="e")
                #   car3 data
                self.car3_label = customtkinter.CTkLabel(self.second_frame, text=("%s" % (self.connection_db.nombre_for_id("fabricantes", self.carros_in_page[i][3])[0])))
                self.car3_label.grid(row=3, column=1, padx=0, pady=(0,150), sticky="nsew")
                self.car3_data_text = customtkinter.CTkTextbox(self.second_frame, height=90, width=100)
                self.car3_data_text.grid(row=3, column=1, padx=(20, 0), pady=(8, 8), sticky="ew")
                self.car3_data_text.insert("0.0",("Modelo:  %s \tAño:  %s \tColor:  %s \nNombre del dueño:  %s \nDetalles del carro:  %s" % (self.connection_db.nombre_for_id("modelo_de_carro", self.carros_in_page[i][5])[0],
                                                                                                                                                 str(datetime.datetime.date(self.carros_in_page[1][1]).year),
                                                                                                                                                 self.carros_in_page[i][2],
                                                                                                                                                 self.connection_db.nombre_for_id("dueno_carro", self.carros_in_page[i][6])[0],
                                                                                                                                                 self.carros_in_page[i][4])))

    def connection_thread(self):
        self.connection_db = conn.Conn()
        self.connection_db.establish_connection()

    def home_vehicle_save_button_event(self):
        self.insert_vehicle_db()
        """print("\n\nSiguiente a datos del dueño' click")
        print("Se guardan los siguientes datos",
              "\nfabricante: ",self.combobox_fabricante.get(),
              "\nmodelo: ",self.combobox_modelo.get(),
              "\naño: ",self.combobox_ano.get(),
              "\ncolor: ",self.combobox_color.get())
        if self.entry.path_to_image==None:
            #mensaje = self.mesagebox(text='Agregue una foto',title="Error")
            pass"""

    def combobox_ano_event(self):
        self.entry.fecha_de_creacion = self.combobox_ano.get()
    def combobox_color_event(self):
        self.entry.color = self.combobox_color.get()
    def combobox_detalles_event(self):
        self.entry.carro_detalles = self.combobox_detalles.get()
    def combobox_direccion_event(self):
        self.entry.dueno_dirreccion = self.combobox_direccion.get()
    def combobox_fabricante_event(self):
        self.entry.fabricante_nombre = self.combobox_fabricante.get()
    def combobox_modelo_event(self):
        self.entry.modelo_nombre = self.combobox_modelo.get()
    def combobox_nombre_event(self):
        self.entry.nombre = self.combobox_nombre.get()
    def photo_path_button_event(self):
        self.entry.path_to_image = self.file_explorer.open_file()
        self.entry.image = self.file_explorer.file_name
        self.photo_path_button.configure(font=("normal", 10), text="imagen seleccionada")

    def insert_vehicle_db(self):
        self.entry.fecha_de_creacion = self.combobox_ano.get()
        self.entry.color = self.combobox_color.get()
        self.entry.carro_detalles = self.combobox_detalles.get()
        self.entry.dueno_dirreccion = self.combobox_direccion.get()
        self.entry.fabricante_nombre = self.combobox_fabricante.get()
        self.entry.modelo_nombre = self.combobox_modelo.get()
        self.entry.nombre = self.combobox_nombre.get()

        if self.entry.path_to_image==None:
            print("Eliga foto de carro")
            return
        else:
            self.entry.insert()
            #self.connection_db.refresh_data()
            self.combobox_fabricante.set("Seleccione Marca")
            self.combobox_ano.set("Seleccione Año")
            self.combobox_modelo.set("Seleccione Modelo")
            self.combobox_color.set("Seleccione Color")
            self.combobox_detalles.set("Escriba los detalles")
            self.combobox_nombre.set("Nombre del Dueño")
            self.combobox_direccion.set("Direccion del dueño")
            self.photo_path_button.configure(font=("normal", 12), text="Eliga la foto")
            self.connection_db.commit_change()
            print("\nano:  ", self.entry.fecha_de_creacion,
                  "\ncolor:  ", self.entry.color,
                  "\ndetalles:  ", self.entry.carro_detalles,
                  "\ndireccion dueno:  ", self.entry.dueno_dirreccion,
                  "\nfabricante:  ", self.entry.fabricante_nombre,
                  "\nmodelo:  ", self.entry.modelo_nombre,
                  "\nnombre dueno:  ", self.entry.nombre,
                  "\nimagen:  ", self.entry.image,
                  "\ndueno id:  ", self.entry.dueno_id,
                  "\ncarro id:  ", self.entry.carro_id)
        self.combobox_fabricante.configure(values=self.connection_db.query_column_data_5pos('fabricantes','fabricante_nombre'))
        self.combobox_ano.configure(values=self.connection_db.query_column_data_5pos_years('carros','fecha_de_creacion'))
        self.combobox_modelo.configure(values=self.connection_db.query_column_data_5pos('modelo_de_carro','modelo_nombre'))
        self.combobox_color.configure(values=self.connection_db.query_column_data_5pos('carros','color'))
        self.combobox_detalles.configure(values=self.connection_db.query_column_data_5pos('carros','carro_detalles'))
        self.combobox_nombre.configure(values=self.connection_db.query_column_data_5pos('dueno_carro', 'nombre'))
        self.combobox_direccion.configure(values=self.connection_db.query_column_data_5pos('dueno_carro', 'dueno_direccion'))
        print("\nprint para asegurarme que se actualicen los combobox\n")


    def update_combobox_direccion(self):
        self.combobox_direccion['values'] = self._category_dir[self.combobox_nombre.get()]
        #self.combobox_direccion.configure(values=valores)
        #self.combobox_direccion._values = valores
    def set_combobox_direccion(self):
        self.combobox_direccion['values'] = self._category_dir[self.combobox_nombre.get()]
        return self._category_dir[self.combobox_nombre.get()]



if __name__ == "__main__":
    app = App()
    app.mainloop()

