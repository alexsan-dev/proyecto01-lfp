from graphviz import Digraph

# GENERAR ÁRBOL DE GRAPHVIZ


def generate_DOT(data):
    # GRAPHVIZ
    g = Digraph('G', filename='hello.gv')

    # SECCIONES
    for section in data["sections"]:
        g.edge(data['res_name'], section["name"], constraint="True")

        # OPCIONES
        order_options = sorted(section["options"], key=lambda k: k['price'])
        for option in order_options:
            g.edge(
                section["name"], f'{option["name"]} Q{option["price"]}\n{option["description"]}', constraint="True")

    g.view()
