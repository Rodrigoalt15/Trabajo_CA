import customtkinter
from tkintermapview import TkinterMapView
import algorithm as alg

customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "Ruta Corta"
    WIDTH = 1024 
    HEIGHT = 640

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)
        self.place = "La Plata, Argentina"
        self.marker_list = []
        self.coordx = []
        self.coordy = []
        self.algoritmo = alg.algorithm(self.place)
        self.camino = customtkinter.CTkFrame()

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Borrar",
                                                command=self.clear_marker_event)
        
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Centrar Mapa",
                                                command=self.centrar_mapa)

        self.button_3.grid(pady=(100, 0), padx=(20, 20), row=1, column=0)

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="Escriba la avenida o calle que no quiera utilizar")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Buscar Ruta",
                                                width=90,
                                                command=self.buscar_ruta)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        self.map_widget.add_right_click_menu_command( label="Añadir Marcador",
                                        command= self.set_marker_event,
                                        pass_coords=True)


        # Set default values
        
        self.map_widget.set_address(self.place)

    def set_marker_event(self, coords):
        current_position = self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(coords[0], coords[1] ))
        self.coordx.append(coords[0])
        self.coordy.append(coords[1])

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()
        self.marker_list.clear()
        self.coordx.clear()
        self.coordy.clear()
        self.camino.delete()
    
    def centrar_mapa(self):
        self.map_widget.set_address(self.place)

    def buscar_ruta(self):

            if self.entry != "":
                self.algoritmo.eliminar_calle(self.entry.get())
            marker1 = self.algoritmo.set_nearest_node(self.marker_list[0] ,self.coordy[0], self.coordx[0])
            marker2 = self.algoritmo.set_nearest_node(self.marker_list[1], self.coordy[1], self.coordx[1])

            path = self.algoritmo.handle_change_location(marker1 , marker2)
            y , x = self.algoritmo.leer_archivo(path)
            coordenadas = [i for i in zip(y, x)]
            self.camino = self.map_widget.set_path(coordenadas)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

    


if __name__ == "__main__":
    app = App()
    app.start()