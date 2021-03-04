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
        "^\s*(\w+)\s*(\W)\s*\'*([^\']*)?\'*", line)

    if(res_declarations):
        # GRUPOS
        groups = res_declarations.groups()

        # ERROR AL ESCRIBIR restaurante
        if(not re.match("^restaurante$", groups[0], re.IGNORECASE)):
            add_error(errs, 0, groups, line, line_number,
                      "debe ser \'restaurante\'")

        # ERROR AL IGUALAR
        elif(not re.match("^=$", groups[1], re.IGNORECASE)):
            add_error(errs, 1, groups, line, line_number,
                      "debe ser \'=\'")

        # ERROR AL ASIGNAR
        elif(not re.match("^[a-zA-Z]+$", groups[2], re.IGNORECASE)):
            add_error(errs, 2, groups, line, line_number,
                      "debe ser un string")

        # AGREGAR RESTAURANTE
        else:
            res_names.append(groups[2])

    return res_names


def parse_menu_files(lines):
    # LISTA DE ERRORES
    errs = []
    res_names = []

    line_number = 1

    for line in lines.split('\n'):
        # BUSCAR NOMBRES DE RESTAURANTES
        find_restaurants(res_names, line, line_number, errs)

        # AUMENTAR LINEA
        line_number += 1

    print(res_names)

    # MOSTRAR ERRORES
    print('\n')
    for err in errs:
        print(err['toString']())
    print('\n')

    return True
