import re

# AGREGAR ERROR


def add_error(errs, err_index, groups, line, line_number, msg, custom_col=0):
    # ERROR
    errNo = len(errs)
    err = re.search(groups[err_index], line)

    # PROPIEDADES
    char = groups[err_index]
    msg = f"\'{groups[err_index]}\' {msg}"
    col = custom_col if custom_col != 0 else err.start() + 1 if err else 0

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
        "col": re.search(groups[group_index], line).start() + 1 if re.search(groups[group_index], line) else 0,
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
        valid = True

        # ERROR AL ESCRIBIR restaurante
        if not re.match("^restaurante$", groups[0], re.IGNORECASE):
            valid = False
            add_error(errs, 0, groups, line, line_number,
                      "debe ser \'restaurante\'")

        # ERROR AL IGUALAR
        if groups[1] != '=':
            valid = False
            add_error(errs, 1, groups, line, line_number,
                      "debe ser \'=\'")

        # ERROR AL ASIGNAR
        if not re.match("'[^']*'", groups[2], re.IGNORECASE):
            valid = False
            add_error(errs, 2, groups, line, line_number,
                      "debe ser un string")

        # AGREGAR RESTAURANTE
        if valid:
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
        valid = True

        # ERROR AL IGUALAR
        if(groups[2] != ':'):
            valid = False
            add_error(errs, 2, groups, line, line_number,
                      "debe ser \':\'")

        # ERROR DE COMILLAS
        if not re.match("'[^']*'$", groups[0], re.IGNORECASE):
            valid = False
            add_error(errs, 0, groups, line, line_number,
                      "falto cerrar comillas", re.search(groups[0], line).start() + 1 + len(groups[0]))

        # AGREGAR RESTAURANTE
        if valid:
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
        "\s*([\[\(\{])(.+)([\]\}\)])\s*", line)

    if res_declarations:
        # GRUPOS
        groups = res_declarations.groups()

        valid = True
        option_values = list(map(lambda value: value.strip(), groups[1].replace(
            groups[0], '').replace(groups[2], '').strip().split(';')))

        # VERIFICAR QUE SE CIERRE EL ]
        if groups[0] != '[':
            valid = False
            add_error(errs, 0, [f'\{groups[0]}'], line, line_number,
                      "se esperaba un '['")

        if groups[2] != ']':
            valid = False
            add_error(errs, 0, [f'\{groups[2]}'], line, line_number,
                      "se esperaba un ']'")

        # VERIFICAR ID
        if not re.match('^[a-z][a-z0-9_]*$', option_values[0]):
            valid = False
            add_error(errs, 0, option_values, line, line_number,
                      "id con formato incorrecto")

        # VERIFICAR NOMBRE
        if len(option_values) > 1 and not re.match("'[^']*'$", option_values[1]):
            valid = False
            quotes = re.match("^'.*[^']$", option_values[1])
            add_error(errs, 1, option_values, line, line_number,
                      "falto cerrar comillas" if quotes else "se esperaba un string", re.search(option_values[1], line).start() + 1 + len(option_values[1]) if quotes else 0)

        # VERIFICAR PRECIO
        if len(option_values) > 2 and not re.match("^\.?[0-9]+(\.[0-9]*)?$", option_values[2]):
            valid = False
            add_error(errs, 2, option_values, line, line_number,
                      "se esperaba un numero")

        # VERIFICAR DESCRIPCION
        if len(option_values) > 3 and not re.match("'[^']*'$", option_values[3]):
            valid = False
            quotes = re.match("^'.*[^']$", option_values[3])
            add_error(errs, 3, option_values, line, line_number,
                      "falto cerrar comillas" if quotes else "se esperaba un string", re.search(option_values[3], line).start() + 1 + len(option_values[3]) if quotes else 0)

        # OPCIÓN VALIDA
        if valid:
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
    res_declarations = re.search("^\s*(\w+)\s*(\W)\s*(\w+)\s*(\W)*", line)

    if res_declarations:
        # GRUPOS
        groups = res_declarations.groups()
        valid = True

        # ERROR DE NÚMEROS
        if not re.match("\.?[0-9]+(\.[0-9]*)?", groups[0], re.IGNORECASE):
            valid = False
            add_error(errs, 0, groups, line, line_number,
                      "se esperaba un número")

        # ERROR DE TOKENS
        if groups[3]:
            valid = False
            add_error(errs, 0, [f"\{groups[3]}"], line, line_number,
                      "token invalido")

        # ERROR DE COMA
        if groups[1] != ',':
            valid = False
            add_error(errs, 1, groups, line, line_number,
                      "debe ser ','")

        # ERROR DE ID
        if not re.match("^[a-z][a-z0-9_]*$", groups[2]):
            valid = False
            add_error(errs, 2, groups, line, line_number,
                      "id con formato incorrecto")

        # AGREGAR
        if valid:
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
        valid = True

        # ERRORES DE COMILLAS
        if groups[0] != "'":
            valid = False
            add_error(errs, 0, groups, line, line_number,
                      "debe ser comillas simple")

        if groups[2] != "'":
            valid = False
            add_error(errs, 2, groups, line, line_number,
                      "debe ser comillas simple", re.search(groups[1], line).end() - 1)

        if groups[4] != "'":
            valid = False
            add_error(errs, 4, groups, line, line_number,
                      "debe ser comillas simple", re.search(groups[5], line).start() + 1)

        if groups[6] != "'":
            valid = False
            add_error(errs, 6, groups, line, line_number,
                      "debe ser comillas simple", re.search(groups[5], line).end())

        if groups[8] != "'":
            valid = False
            add_error(errs, 8, groups, line, line_number,
                      "debe ser comillas simple",  re.search(groups[9], line).start() + 1)

        if groups[10] != "'":
            valid = False
            add_error(errs, 10, groups, line, line_number,
                      "debe ser comillas simple", re.search(groups[9], line).end() - 1)

        # ERRORES DE NÚMEROS
        if not re.match("\.?[0-9]+(\.[0-9]*)?", groups[12], re.IGNORECASE):
            valid = False
            add_error(errs, 12, groups, line, line_number,
                      "se esperaba un numero")

        # ERRORES DE PORCENTAJE
        if groups[13] != '%':
            valid = False
            add_error(errs, 13, groups, line, line_number,
                      "debe ser '%'")

        # ERRORES DE COMAS
        if groups[3] != ",":
            valid = False
            add_error(errs, 3, groups, line, line_number,
                      "debe ser ','", re.search(groups[1], line).end() + 2)

        if groups[7] != ",":
            valid = False
            add_error(errs, 7, groups, line, line_number,
                      "debe ser ','", re.search(groups[5], line).end() + 2)

        if groups[11] != ",":
            valid = False
            add_error(errs, 11, groups, line, line_number,
                      "debe ser ','", re.search(groups[9], line).end() + 2)

        # AGREGAR TOKENS
        if valid:
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

# ERRORES DE TOKENS
def find_invalid_order_tokens(line, line_number, errs):
    match_1 = "^\s*(\W)([^']*)(\W)\s*(\W)\s*(\W)([^']*)(\W)\s*(\W)\s*(\W)([^']*)(\W)\s*(\W)\s*([^']*)(\W)\s*"
    match_2 = "^\s*(\w+)\s*(\W)\s*(\w+)"

    if not re.match("^\s*$", line) and not re.match(match_1, line) and not re.match(match_2, line):
        add_error(errs, 0, [line], line, line_number, "Token invalido")
        return True

def find_invalid_tokens(line, line_number, errs):
    match_1 = "^\s*(\w+)\s*(\W)\s*(\'*([^\']*)?\'*)"
    match_2 = "^\s*('([^']*)'*)\s*(\W)"
    match_3 = "\s*([\[\(\{])(.+)([\]\}\)])\s*"

    if not re.match("^\s*$", line) and not re.match(match_1, line) and not re.match(match_2, line) and not re.match(match_3, line):
        add_error(errs, 0, [line], line, line_number, "Token invalido")
        return True


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

        # BUSCAR ERRORES
        find_invalid_order_tokens(line, line_number, errs)

        if invalid_order:
            input(f'Ocurrió un error {invalid_order} no existe en el menu ')
            enable_generate = False

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
                
        # BUSCAR ERRORES
        find_invalid_tokens(line, line_number, errs)

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
