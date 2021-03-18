# IMPORTS
import json
from files.reader import lfp_reader
from files.parser import parse_menu_files, parse_order_files
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
        menu('(1) Cargar menu | (2) Cargar menu  | (3) Generar orden | (4) Generar factura | (5) Generar Árbol | (6) Salir', {
            1: self.set_file,
            2: self.set_order_file,
            3: self.get_output_file,
            4: self.get_order_output_file,
            5: self.get_output_tree,
            6: self.exit
        })

    # OPCIONES
    def set_file(self):
        self.lfp_file = lfp_reader()
        self.init_menu()

    # ORDEN
    def set_order_file(self):
        self.lfp_file = lfp_reader()
        self.init_menu()

    # ÁRBOL
    def get_output_tree(self):
        if self.lfp_file:
            # GENERAR ARCHIVO
            generate_DOT(self.data[0])
        else:
            input('No se ha cargado ningún menu ')

        # REGRESAR
        self.init_menu()

     # HTML
    def get_order_output_file(self):
        if self.lfp_file:
            # GENERAR DICCIONARIO
            self.data = parse_order_files(
                self.lfp_file.get_lines('./orden.lfp'))

        else:
            input('No se ha cargado ningún menu ')

    # HTML ORDEN

    def get_output_file(self):
        if self.lfp_file:
            # LIMITE
            confirm_limit = input('¿Deseas ver un limite de precios? (y/n): ')
            limit = float('inf') if confirm_limit == 'n' else float(
                input('Ingresa el limite de precios: '))

            # GENERAR DICCIONARIO
            self.data = parse_menu_files(self.lfp_file.get_lines(), limit)

            # GENERAR SIN ERRORES
            if len(self.data[0]["errs"]) == 0:
                generate_HTML(self.data)
                generate_tokens_HTML(self.data)
            else:
                generate_errs_HTML(self.data)
        else:
            input('No se ha cargado ningún menu ')

        # REGRESAR
        self.init_menu()

    # SALIR

    def exit(self):
        pass


# INICIAR
if __name__ == "__main__":
    main()
