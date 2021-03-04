import re

# AGREGAR ERROR


def add_error(errs, err_index, groups, line, line_number, msg, custom_col=0):
    # ERROR
    errNo = len(errs)
    err = re.search(groups[err_index], line)

    # PROPIEDADES
    char = groups[err_index]
    msg = f"\'{groups[err_index]}\' {msg}"
    col = custom_col if custom_col != 0 else err.start() + 1

    # AGREGAR A LISTA DE ERRORES
    errs.append({
        "char": char,
        "msg": msg,
        "col": col,
        "row": line_number,
        "toString": lambda: f"Error {errNo}: {msg} en linea: {line_number}, columna: {col}"
    })


def find_restaurants(res_names, line, line_number, errs):
    # SEARCH
    res_declarations = re.search(
        "^\s*(\w+)\s*(\W)\s*(\'*([^\']*)?\'*)", line)

    if res_declarations:
        # GRUPOS
        groups = res_declarations.groups()

        # ERROR AL ESCRIBIR restaurante
        if not re.match("^restaurante$", groups[0], re.IGNORECASE):
            add_error(errs, 0, groups, line, line_number,
                      "debe ser \'restaurante\'")

        # ERROR AL IGUALAR
        elif groups[1] != '=':
            add_error(errs, 1, groups, line, line_number,
                      "debe ser \'=\'")

        # ERROR AL ASIGNAR
        elif not re.match("'[^']*'", groups[2], re.IGNORECASE):
            add_error(errs, 2, groups, line, line_number,
                      "debe ser un string")

        # AGREGAR RESTAURANTE
        else:
            res_names.append(groups[2].replace('\'', '').strip())

# BUSCAR SECCIONES


def find_sections(res_sections, line, line_number, errs):
    # SEARCH
    res_declarations = re.search(
        "^\s*('([^']*)'*)\s*(\W)", line)

    if res_declarations:
        # GRUPOS
        groups = res_declarations.groups()

        # ERROR AL IGUALAR
        if(groups[2] != ':'):
            add_error(errs, 2, groups, line, line_number,
                      "debe ser \':\'")

        # ERROR DE COMILLAS
        elif not re.match("'[^']*'$", groups[0], re.IGNORECASE):
            add_error(errs, 0, groups, line, line_number,
                      "falto cerrar comillas", re.search(groups[0], line).start() + 1 + len(groups[0]))

        # AGREGAR RESTAURANTE
        else:
            res_sections.append(groups[0].replace('\'', '').strip())
            return True

# BUSCAR OPCIONES


def find_options(res_options, line, line_number, errs, sections_index):
    # SEARCH
    res_declarations = re.search(
        "^\s*(\[.*\W.*\W.*\W.*\]*)", line)

    if res_declarations:
        # GRUPOS
        main_group = res_declarations.group(0)

        # VERIFICAR QUE SE CIERRE EL ]
        if not re.match('.+\]$', main_group):
            custom_group = ["]"]
            add_error(errs, 0, custom_group, line, line_number,
                      "falto cerrar corchetes", len(main_group) + 1)

        # AHORA VERIFICAR VALOR POR VALOR
        else:
            option_values = list(map(lambda value: value.strip(), main_group.replace(
                '[', '').replace(']', '').strip().split(';')))

            # VERIFICAR ID
            if not re.match('[a-z][a-z0-9_]*', option_values[0]):
                add_error(errs, 0, option_values, line, line_number,
                          "id con formato incorrecto")

            # VERIFICAR NOMBRE
            elif not re.match("'[^']*'$", option_values[1]):
                quotes = re.match("^'.*[^']$", option_values[1])
                add_error(errs, 1, option_values, line, line_number,
                          "falto cerrar comillas" if quotes else "se esperaba un string", re.search(option_values[1], line).start() + 1 + len(option_values[1]) if quotes else 0)

            # VERIFICAR PRECIO
            elif not re.match("\.*[0-9]+(\.[0-9]*)?", option_values[2]):
                add_error(errs, 2, option_values, line, line_number,
                          "se esperaba un numero")

            # VERIFICAR DESCRIPCION
            elif not re.match("'[^']*'$", option_values[3]):
                quotes = re.match("^'.*[^']$", option_values[3])
                add_error(errs, 3, option_values, line, line_number,
                          "falto cerrar comillas" if quotes else "se esperaba un string", re.search(option_values[3], line).start() + 1 + len(option_values[3]) if quotes else 0)

            # OPCIÓN VALIDA
            else:
                current_option = res_options.get(sections_index, [])
                current_option.append({
                    "id": option_values[0],
                    "name": option_values[1].replace('\'', ''),
                    "price": float(option_values[2]),
                    "description": option_values[3].replace('\'', '')
                })

                # REASIGNAR
                res_options[sections_index] = current_option


def parse_menu_files(lines):
    # LISTA DE ERRORES Y RESTAURANTES
    errs = []
    res_names = []
    res_sections = []
    res_options = {}
    sections_index = -1

    # LISTA DE DATOS FINALES
    data = []

    # RECCORER
    line_number = 1
    for line in lines.split('\n'):
        # BUSCAR NOMBRES DE RESTAURANTES
        find_restaurants(res_names, line, line_number, errs)

        # BUSCAR NOMBRES DE SECCIONES
        valid_section = find_sections(
            res_sections, line, line_number, errs)
        if valid_section:
            sections_index += 1

        # BUSCAR SECCIONES
        find_options(res_options, line, line_number, errs, sections_index)

        # AUMENTAR LINEA
        line_number += 1

    # CREAR SECCIONES
    for res_name in res_names:
        # RECORRER SECCIONES
        sections = []
        for res_section_index in range(len(res_sections)):

            sections.append({
                "name": res_sections[res_section_index],
                "options": res_options.get(res_section_index, [])
            })

        # DATOS FINALES
        data_dict = {
            "res_name": res_name,
            "sections": sections
        }

        # AGREGAR
        data.append(data_dict)

    return errs if len(errs) > 0 else data
