# EXPORTAR A HTML
def generate_HTML(data):
    # LEER LINEAS
    lfp_stream = open('./out/template/index.html', encoding='utf-8')
    lfp_lines = lfp_stream.read()

    # MAPA DE OPCIONES
    def options_map(option):
        return f'<div><strong>🍛 {option["name"]}</strong><p>{option["id"]}</p><p>{option["description"]}</p><p>Q{option["price"]}</p></div>'

    # MAPA DE SECCIONES
    def sections_map(section):
        return f'<li><h2>📜 {section["name"]}</h2>{"<br/>".join(map(options_map, section["options"]))}</li>'

    # VARIABLES
    lfp_lines = lfp_lines.replace(
        '{{ res_name }}', data[0]['res_name']).replace('{{ sections }}',  "".join(map(sections_map, data[0]["sections"])))

    # ESCRIBIR
    lfp_stream_write = open('./out/index.html', 'w')
    lfp_stream_write.write(lfp_lines)

    # CERRAR
    lfp_stream_write.close()
    lfp_stream.close()

# EXPORTAR FACTURA HTML


def generate_order_HTML(menu_data, order_data):
    # LEER LINEAS
    lfp_stream = open('./out/template/billing.html', encoding='utf-8')
    lfp_lines = lfp_stream.read()

    # SUBTOTAL
    sub_total = 0

    # MAPA DE ORDENES
    def order_map(order):
        nonlocal sub_total

        # ENCONTRAR OPCIÓN
        current_option = None
        for section in menu_data[0]["sections"]:
            for option in section["options"]:
                if option["id"] == order["id"]:
                    current_option = option

        # SUMAR SUBTOTAL
        order_sub_total = order['quantity'] * current_option['price']
        sub_total += order_sub_total

        return f"<tr><td>{order['quantity']}</td><td>{current_option['name']}</td><td>Q{'{:.2f}'.format(current_option['price'])}</td><td>Q{'{:.2f}'.format(order_sub_total)}</td></tr>"

    lfp_lines = lfp_lines.replace("{{ res_name }}", menu_data[0]["res_name"]).replace(
        '{{ c_name }}', order_data["customer"]["name"]).replace("{{ c_nit }}", order_data["customer"]["nit"]).replace("{{ c_address }}", order_data["customer"]["address"]).replace("{{ summary }}", "".join(map(order_map, order_data["orders"]))).replace("{{ sub_total }}", "{:.2f}".format(sub_total)).replace("{{ p_percent }}", "{:.2f}".format(min(100, order_data["customer"]["tip"]))).replace("{{ tip }}", "{:.2f}".format(sub_total * (min(100, order_data["customer"]["tip"], 100)/100))).replace("{{ total }}", "{:.2f}".format(sub_total + (sub_total * (min(100, order_data["customer"]["tip"])/100))))

    # ESCRIBIR
    lfp_stream_write = open('./out/billing.html', 'w')
    lfp_stream_write.write(lfp_lines)

    # CERRAR
    lfp_stream_write.close()
    lfp_stream.close()


# EXPORTAR TABLA DE LEXEMAS A HTML
def generate_tokens_HTML(data, filename='./out/lex.html'):
    # LEER LINEAS
    lfp_stream = open('./out/template/lex.html', encoding='utf-8')
    lfp_lines = lfp_stream.read()

    # MAPA DE LEXEMAS
    def lex_map(lex):
        return f'<tr><td>{lex["lex"]}</td><td>{lex["row"]}</td><td>{lex["col"]}</td><td>{lex["token"]}</td></tr>'

    # VARIABLES
    lfp_lines = lfp_lines.replace(
        '{{ lex }}',  "".join(map(lex_map, data[0]["tokens"])))

    # ESCRIBIR
    lfp_stream_write = open(filename, 'w')
    lfp_stream_write.write(lfp_lines)

    # CERRAR
    lfp_stream_write.close()
    lfp_stream.close()


# EXPORTAR TABLA DE ERRORES A HTML
def generate_errs_HTML(data, filename='./out/errors.html'):
    # LEER LINEAS
    lfp_stream = open('./out/template/errors.html', encoding='utf-8')
    lfp_lines = lfp_stream.read()

    # MAPA DE LEXEMAS
    def errs_map(err):
        return f'<tr><td>{err["char"]}</td><td>{err["msg"]}</td><td>{err["row"]}</td><td>{err["col"]}</td></tr>'

    # VARIABLES
    lfp_lines = lfp_lines.replace(
        '{{ errs }}',  "".join(map(errs_map, data[0]["errs"])))

    # ESCRIBIR
    lfp_stream_write = open(filename, 'w')
    lfp_stream_write.write(lfp_lines)

    # CERRAR
    lfp_stream_write.close()
    lfp_stream.close()
