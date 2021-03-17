# EXPORTAR A HTML
def generate_HTML(data):
    # LEER LINEAS
    lfp_stream = open('./out/template/index.html', encoding='utf-8')
    lfp_lines = lfp_stream.read()

    # MAPA DE OPCIONES
    def options_map(option):
        return f'<div><strong>{option["name"]}</strong><p>{option["id"]}</p><p>{option["name"]}</p><p>{option["description"]}</p><p>Q {option["price"]}</p></div>'

    # MAPA DE SECCIONES
    def sections_map(section):
        return f'<li><h2>{section["name"]}</h2>{"<br/>".join(map(options_map, section["options"]))}</li>'

    # VARIABLES
    lfp_lines = lfp_lines.replace(
        '{{ res_name }}', data[0]['res_name']).replace('{{ sections }}',  "".join(map(sections_map, data[0]["sections"])))

    # ESCRIBIR
    lfp_stream_write = open('./out/index.html', 'w')
    lfp_stream_write.write(lfp_lines)

    # CERRAR
    lfp_stream_write.close()
    lfp_stream.close()


# EXPORTAR TABLA DE LEXEMAS A HTML
def generate_tokens_HTML(data):
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
    lfp_stream_write = open('./out/lex.html', 'w')
    lfp_stream_write.write(lfp_lines)

    # CERRAR
    lfp_stream_write.close()
    lfp_stream.close()


# EXPORTAR TABLA DE ERRORES A HTML
def generate_errs_HTML(data):
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
    lfp_stream_write = open('./out/errors.html', 'w')
    lfp_stream_write.write(lfp_lines)

    # CERRAR
    lfp_stream_write.close()
    lfp_stream.close()
