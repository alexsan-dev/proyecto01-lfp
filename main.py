# IMPORTS
import json
from files.reader import lfp_reader
from files.parser import parse_menu_files, parse_order_files
from files.output import generate_HTML, generate_tokens_HTML, generate_errs_HTML, generate_order_HTML
from files.graphviz import generate_DOT
from menu.menu import menu


class main():
    def __init__(self):
        # GLOBALES
        self.lfp_file = None
        self.lfp_order_file = None
        self.menu_data = None
        self.init_menu()

    # MENU PRINCIPAL
    def init_menu(self):
        menu('(1) Cargar menu | (2) Cargar orden  | (3) Generar menu | (4) Generar factura | (5) Generar Árbol | (6) Salir', {
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
        self.lfp_order_file = lfp_reader()
        self.init_menu()

    # ÁRBOL
    def get_output_tree(self):
        if self.lfp_file:
            # GENERAR ARCHIVO
            generate_DOT(self.menu_data[0])
        else:
            input('No se ha cargado ningún menu ')

        # REGRESAR
        self.init_menu()

     # HTML
    def get_order_output_file(self):
        if self.lfp_order_file != None and self.menu_data:
            # GENERAR DICCIONARIO
            self.order_data = parse_order_files(
                self.lfp_order_file.get_lines('./orden.lfp'), self.menu_data)

            # GENERAR SIN ERRORES
            if self.order_data.get("customer", None) and len(self.order_data["errs"]) == 0:
                generate_order_HTML(self.menu_data, self.order_data)
                generate_tokens_HTML(
                    [self.order_data], './out/lex_orders.html')
            else:
                generate_errs_HTML(
                    [self.order_data],  './out/errors_orders.html')

        else:
            input('No se ha cargado ningúna orden ')

        # REGRESAR
        self.init_menu()

    # HTML ORDEN

    def get_output_file(self):
        if self.lfp_file:
            # LIMITE
            confirm_limit = input('¿Deseas ver un limite de precios? (y/n): ')
            limit = float('inf') if confirm_limit != 'y' else float(
                input('Ingresa el limite de precios: '))

            # GENERAR DICCIONARIO
            self.menu_data = parse_menu_files(self.lfp_file.get_lines(), limit)

            # GENERAR SIN ERRORES
            if len(self.menu_data[0]["errs"]) == 0:
                generate_HTML(self.menu_data)
                generate_tokens_HTML(self.menu_data)
            else:
                generate_errs_HTML(self.menu_data)
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
