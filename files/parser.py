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
        "row": line_number
    })


# AGREGAR TOKEN
def add_token(res_tokens, groups, group_index, line, line_number, token_name):
    # TOKEN DE ID
    res_tokens.append({
        "lex": groups[group_index],
        "row": line_number,
        "col": re.search(groups[group_index], line).start() + 1,
        "token": token_name
    })

# BUSCAR RESTAURANTES


def find_restaurants(res_tokens, res_names, line, line_number, errs):
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
            # TOKEN DE ID
            add_token(res_tokens, groups, 0, line,
                      line_number, "identificador")

            # TOKEN DE OPERADOR
            add_token(res_tokens, groups, 1, line, line_number, "operador")

            # TOKEN DE CADENA
            add_token(res_tokens, groups, 2, line, line_number, "cadena")

            # AGREGAR
            res_names.append(groups[2].replace('\'', '').strip())

# BUSCAR SECCIONES


def find_sections(res_tokens, res_sections, line, line_number, errs):
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
            # TOKEN DE CADENA
            add_token(res_tokens, groups, 0, line, line_number, "cadena")

            # TOKEN DE OPERADOR
            add_token(res_tokens, groups, 2, line, line_number, "operador")

            # AGREGAR
            res_sections.append(groups[0].replace('\'', '').strip())
            return True

# BUSCAR OPCIONES


def find_options(res_tokens, res_options, line, line_number, errs, sections_index, price_limit):
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
            elif not re.match("\.?[0-9]+(\.[0-9]*)?", option_values[2]):
                add_error(errs, 2, option_values, line, line_number,
                          "se esperaba un numero")

            # VERIFICAR DESCRIPCION
            elif not re.match("'[^']*'$", option_values[3]):
                quotes = re.match("^'.*[^']$", option_values[3])
                add_error(errs, 3, option_values, line, line_number,
                          "falto cerrar comillas" if quotes else "se esperaba un string", re.search(option_values[3], line).start() + 1 + len(option_values[3]) if quotes else 0)

            # OPCIÓN VALIDA
            else:
                # TOKEN DE ID
                add_token(res_tokens, option_values, 0,
                          line, line_number, "identificador")

                # TOKEN DE CADENA
                add_token(res_tokens, option_values, 1,
                          line, line_number, "cadena")

                # TOKEN DE NUMERO
                add_token(res_tokens, option_values, 2,
                          line, line_number, "número")

                # TOKEN DE CADENA
                add_token(res_tokens, option_values, 3,
                          line, line_number, "cadena")

                # AGREGAR
                current_option = res_options.get(sections_index, [])
                if float(option_values[2]) <= price_limit:
                    current_option.append({
                        "id": option_values[0],
                        "name": option_values[1].replace('\'', ''),
                        "price": float(option_values[2]),
                        "description": option_values[3].replace('\'', '')
                    })

                # REASIGNAR
                res_options[sections_index] = current_option

# BUSCAR PEDIDOS


def find_orders(res_tokens, res_orders, line, line_number, errs, menu_data):
    # SEARCH
    res_declarations = re.search("^\s*(\w+)\s*(\W)\s*(\w+)", line)

    if res_declarations:
        # GRUPOS
        groups = res_declarations.groups()

        # ERROR DE NÚMEROS
        if not re.match("\.?[0-9]+(\.[0-9]*)?", groups[0], re.IGNORECASE):
            add_error(errs, 0, groups, line, line_number,
                      "se esperaba un número")

        # ERROR DE COMA
        elif groups[1] != ',':
            add_error(errs, 1, groups, line, line_number,
                      "debe ser ','")

        # ERROR DE ID
        elif not re.match("[a-z][a-z0-9_]*", groups[2]):
            add_error(errs, 2, groups, line, line_number,
                      "id con formato incorrecto")

        # AGREGAR
        else:
            # TOKEN DE ID
            add_token(res_tokens, groups, 0,
                      line, line_number, "numero")

            # TOKEN DE NUMERO
            add_token(res_tokens, groups, 2,
                      line, line_number, "identificador")

            # VALIDAR ID
            invalid_id = groups[2]
            for section in menu_data[0]["sections"]:
                for option in section["options"]:
                    if option["id"] == groups[2]:
                        invalid_id = None

            if invalid_id == None:
                # AGREGAR A ORDENES
                res_orders.append({
                    "quantity": int(groups[0]),
                    "id": groups[2]
                })

            return invalid_id


# BUSCAR CLIENTE


def find_customers(res_tokens, res_customers, line, line_number, errs):
    # SEARCH
    res_declarations = re.search(
        "^\s*(\W)([^']*)(\W)\s*(\W)\s*(\W)([^']*)(\W)\s*(\W)\s*(\W)([^']*)(\W)\s*(\W)\s*([^']*)(\W)\s*", line)

    # BUSCAR OPCIONES
    if res_declarations:
        # GRUPOS
        groups = res_declarations.groups()

        # ERRORES DE COMILLAS
        if groups[0] != "'":
            add_error(errs, 0, groups, line, line_number,
                      "debe ser comillas simple")

        elif groups[2] != "'":
            add_error(errs, 2, groups, line, line_number,
                      "debe ser comillas simple", re.search(groups[1], line).end() - 1)

        elif groups[4] != "'":
            add_error(errs, 4, groups, line, line_number,
                      "debe ser comillas simple", re.search(groups[5], line).start() + 1)

        elif groups[6] != "'":
            add_error(errs, 6, groups, line, line_number,
                      "debe ser comillas simple", re.search(groups[5], line).end())

        elif groups[8] != "'":
            add_error(errs, 8, groups, line, line_number,
                      "debe ser comillas simple",  re.search(groups[9], line).start() + 1)

        elif groups[10] != "'":
            add_error(errs, 10, groups, line, line_number,
                      "debe ser comillas simple", re.search(groups[9], line).end() - 1)

        # ERRORES DE NÚMEROS
        elif not re.match("\.?[0-9]+(\.[0-9]*)?", groups[12], re.IGNORECASE):
            add_error(errs, 12, groups, line, line_number,
                      "se esperaba un numero")

        # ERRORES DE PORCENTAJE
        elif groups[13] != '%':
            add_error(errs, 13, groups, line, line_number,
                      "debe ser '%'")

        # ERRORES DE COMAS
        elif groups[3] != ",":
            add_error(errs, 3, groups, line, line_number,
                      "debe ser ','", re.search(groups[1], line).end() + 2)

        elif groups[7] != ",":
            add_error(errs, 7, groups, line, line_number,
                      "debe ser ','", re.search(groups[5], line).end() + 2)

        elif groups[11] != ",":
            add_error(errs, 11, groups, line, line_number,
                      "debe ser ','", re.search(groups[9], line).end() + 2)

        # AGREGAR TOKENS
        else:
            # TOKENS DE CADENAS
            add_token(res_tokens, groups, 1,
                      line, line_number, "cadena")
            add_token(res_tokens, groups, 5,
                      line, line_number, "cadena")
            add_token(res_tokens, groups, 9,
                      line, line_number, "cadena")

            # TOKENS DE NÚMEROS
            add_token(res_tokens, groups, 12,
                      line, line_number, "numero")

            # AGREGAR
            res_customers.append({
                "name": groups[1],
                "nit": groups[5],
                "address":  groups[9],
                "tip": float(groups[12])
            })
            return True

# DICCIONARIO DE ORDENES


def parse_order_files(lines, menu_data):
    # LISTA DE ERRORES Y RESTAURANTES
    errs = []
    res_customers = []
    res_orders = []
    res_tokens = []

    enable_generate = True
    invalid_order = None
    data = None

    # RECCORER
    line_number = 1
    for line in lines.split('\n'):
        # BUSCAR CLIENTES
        find_customers(
            res_tokens, res_customers, line, line_number, errs)

        # BUSCAR ORDENES
        invalid_order = find_orders(
            res_tokens, res_orders, line, line_number, errs, menu_data)

        if invalid_order:
            input(f'Ocurrió un error {invalid_order} no existe en el menu ')
            enable_generate = False
            break

        # AUMENTAR LINEA
        line_number += 1

    # AGREGAR A DICCIONARIO
    if len(res_customers) > 0 and enable_generate:
        data = {
            "customer": res_customers[0],
            "orders": res_orders,
            "tokens": res_tokens,
            "errs": errs
        }
    else:
        data = {
            "errs": [{
                "char": invalid_order,
                "msg": 'Identificador no existe en menu',
                "col": 0,
                "row": 0
            }]
        }

    # AGREGAR
    return data


# DICCIONARIO DE MENUS
def parse_menu_files(lines, price_limit):
    # LISTA DE ERRORES Y RESTAURANTES
    errs = []
    res_names = []
    res_sections = []
    res_tokens = []
    res_options = {}
    sections_index = -1

    # LISTA DE DATOS FINALES
    data = []

    # RECCORER
    line_number = 1
    for line in lines.split('\n'):
        # BUSCAR NOMBRES DE RESTAURANTES
        find_restaurants(res_tokens, res_names, line, line_number, errs)

        # BUSCAR NOMBRES DE SECCIONES
        valid_section = find_sections(res_tokens,
                                      res_sections, line, line_number, errs)
        if valid_section:
            sections_index += 1

        # BUSCAR SECCIONES
        find_options(res_tokens, res_options, line,
                     line_number, errs, sections_index, price_limit)

        # AUMENTAR LINEA
        line_number += 1

    # CREAR SECCIONES
    sections = []
    for res_section_index in range(len(res_sections)):
        sections.append({
            "name": res_sections[res_section_index],
            "options": res_options.get(res_section_index, [])
        })

    # DATOS FINALES
    data_dict = {
        "res_name": res_names[0] if len(res_names) > 0 else '',
        "sections": sections,
        "errs": errs,
        "tokens": res_tokens
    }

    # AGREGAR
    data.append(data_dict)
    return data
