# IMPORTS
import json
from files.reader import lfp_reader
from files.parser import parse_menu_files
from menu.menu import menu


class main():
    def __init__(self):
        # GLOBALES
        self.lfp_file = None
        self.init_menu()

    # MENU PRINCIPAL
    def init_menu(self):
        menu('(1) Cargar | (2) Generar | (3) Salir', {
            1: self.set_file,
            2: self.get_output_file,
            3: self.exit
        })

    # OPCIONES
    def set_file(self):
        self.lfp_file = lfp_reader()
        self.init_menu()

     # HTML
    def get_output_file(self):
        print(parse_menu_files(self.lfp_file.get_lines()))

    # SALIR
    def exit(self):
        pass


# INICIAR
if __name__ == "__main__":
    main()
