# IMPORTS
import os


def menu(options, actions):
    # LIMPIAR
    os.system('clear' if os.name == 'posix' else 'cls')

    # SEPARADOR
    hr = "-" * (len(options) + 4)

    # MENU
    print(f'{hr}\n| {options} |\n{hr}')

    # OPCIONES
    option = input('Escribe una opción: ')

    # LLAMAR OPCIÓN
    func = actions.get(int(option), lambda: menu(options, actions))
    func()
