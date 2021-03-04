import re

# AGREGAR ERROR


def add_error(errs, err_index, groups, line, line_number, msg):
    errNo = len(errs)
    err = re.search(groups[err_index], line)
    errs.append({
        "char": groups[err_index],
        "msg": f"\'{groups[err_index]}\' {msg}",
        "col": err.start() + 1,
        "row": line_number,
        "toString": lambda: f"Error {errNo}: '{groups[err_index]}\' {msg} en linea: {line_number}, columna: {err.start() + 1}"
    })


def find_restaurants(res_names, line, line_number, errs):
    # SEARCH
    res_declarations = re.search(
        "^\s*(\w+)\s*(\W)\s*(\'*([^\']*)?\'*)", line)

    if(res_declarations):
        # GRUPOS
        groups = res_declarations.groups()

        # ERROR AL ESCRIBIR restaurante
        if(not re.match("^restaurante$", groups[0], re.IGNORECASE)):
            add_error(errs, 0, groups, line, line_number,
                      "debe ser \'restaurante\'")

        # ERROR AL IGUALAR
        elif(groups[1] != '='):
            add_error(errs, 1, groups, line, line_number,
                      "debe ser \'=\'")

        # ERROR AL ASIGNAR
        elif(not re.match("'[^']*'", groups[2], re.IGNORECASE)):
            add_error(errs, 2, groups, line, line_number,
                      "debe ser un string")

        # AGREGAR RESTAURANTE
        else:
            res_names.append(groups[2].replace('\'', '').strip())


def find_sections(res_sections, line, line_number, errs):
    # SEARCH
    res_declarations = re.search(
        "^\s*('([^']*)'*)\s*(\W)", line)

    if(res_declarations):
        # GRUPOS
        groups = res_declarations.groups()

        # ERROR AL IGUALAR
        if(groups[2] != ':'):
            add_error(errs, 2, groups, line, line_number,
                      "debe ser \':\'")

        # ERROR DE COMILLAS
        elif(not re.match("'[^']*'$", groups[0], re.IGNORECASE)):
            add_error(errs, 0, groups, line, line_number,
                      "falto cerrar comillas")

        # AGREGAR RESTAURANTE
        else:
            res_sections.append(groups[0].replace('\'', '').strip())

    return res_sections


def parse_menu_files(lines):
    # LISTA DE ERRORES Y RESTAURANTES
    errs = []
    res_names = []
    res_sections = []

    # RECCORER
    line_number = 1
    for line in lines.split('\n'):
        # BUSCAR NOMBRES DE RESTAURANTES
        find_restaurants(res_names, line, line_number, errs)

        # BUSCAR NOMBRES DE SECCIONES
        find_sections(res_sections, line, line_number, errs)

        # AUMENTAR LINEA
        line_number += 1

    print(res_names, res_sections)

    # MOSTRAR ERRORES
    print('\n')
    for err in errs:
        print(err['toString']())
    print('\n')

    return True
