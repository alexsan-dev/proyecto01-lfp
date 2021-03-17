# IMPORTS
import json
from files.reader import lfp_reader
from files.parser import parse_menu_files
from files.output import generate_HTML, generate_tokens_HTML, generate_errs_HTML
from files.graphviz import generate_DOT
from menu.menu import menu


class main():
    def __init__(self):
        # GLOBALES
        self.lfp_file = None
        self.data = None
        self.init_menu()

    # MENU PRINCIPAL
    def init_menu(self):
        menu('(1) Cargar menu | (2) Generar orden | (3) Generar Árbol | (4) Salir', {
            1: self.set_file,
            2: self.get_output_file,
            3: self.get_output_tree,
            4: self.exit
        })

    # OPCIONES
    def set_file(self):
        self.lfp_file = lfp_reader()
        self.init_menu()

    # ÁRBOL
    def get_output_tree(self):
        if self.data[0]:
            # GENERAR ARCHIVO
            generate_DOT(self.data[0])

            # REGRESAR
            self.init_menu()

     # HTML
    def get_output_file(self):
        # GENERAR DICCIONARIO
        self.data = parse_menu_files(self.lfp_file.get_lines())

        # GENERAR SIN ERRORES
        if self.data[0]:
            if len(self.data[0]["errs"]) == 0:
                generate_HTML(self.data)
                generate_tokens_HTML(self.data)
            else:
                generate_errs_HTML(self.data)

        # REGRESAR
        self.init_menu()

    # SALIR
    def exit(self):
        pass


# INICIAR
if __name__ == "__main__":
    main()
