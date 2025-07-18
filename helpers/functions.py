from openpyxl.utils import get_column_letter, range_boundaries
from consuming_api.models import Country
import requests
import matplotlib
matplotlib.use('Agg')  # ⚠️ Importante para evitar errores en macOS
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import io
from PIL import Image as PILImage
from openpyxl.drawing.image import Image as OpenpyxlImage
from .styles import BORDER

# Additional functions

# Return a predifined number of maximum values
def return_max_numbers(n, list_numbers):
    final_list = []
    for i in range(n):
        max_currently_number = max(list_numbers)
        final_list.append(max_currently_number)
        list_numbers.remove(max_currently_number)
    
    return final_list

# Create new country instances based in a range with init and limit
def post_new_countries(init, limit):
    url = "https://restcountries.com/v3.1/all"
    params = {
        "fields": "name,capital,region,population,flags,subregion,area,latlng,translations"
    }

    response = requests.get(url, params=params)

    data = response.json()
    for country in data[init:limit]:
        try:
            Country.objects.create(name=country['name']['common'], region=country['region'], subregion=country['subregion'],
                            capital=country.get('capital', ['Desconocida'])[0], population=country['population'],
                            latitude=country['latlng'][0],  longitude=country['latlng'][1], area=country['area'],
                            flag=country['flags']['alt'])
        except IndexError:
            Country.objects.create(name=country['name']['common'], region=country['region'], subregion=country['subregion'],
                            population=country['population'], latitude=country['latlng'][0],  longitude=country['latlng'][1], 
                            area=country['area'], flag=country['flags']['alt'])
    return response.status_code

# Excel template functions

# Apply border for a cell in a worksheet
def apply_border_to_range(ws, cell_range, border):
    """
    Aplica un borde a todas las celdas dentro del rango dado.
    """
    min_col, min_row, max_col, max_row = range_boundaries(cell_range)
    for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
        for cell in row:
            cell.border = border

# Apply styles for a specific cell
def apply_cell_styles(cell, styles):
    cell.alignment = styles['alignment']
    cell.font = styles['font']
    cell.fill = styles['fill']

# Insert a personalized text in a worksheet
def insert_text(ws, start_cell, end_cell, text, style=None):
    # Join cells
    cell_range = f"{start_cell}:{end_cell}"
    ws.merge_cells(cell_range)
    cell = ws[start_cell]
    cell.value = text
    if style:
        apply_cell_styles(cell, style)
        apply_border_to_range(ws, cell_range, style['border'])

# Create a excel table using dictionaries with values and styles
def create_excel_table(ws, datos, styles=None, inicio=(1, 1), not_styles=[]):
    # Pull your key and value lists
    encabezados = list(datos.keys())
    filas = zip(*datos.values())  # The rows are the value columns from dictionary

    # Write your initial coordinates
    fila_inicio, col_inicio = inicio

    ws.row_dimensions[fila_inicio].height = 20

    # Write your headers
    for col, encabezado in enumerate(encabezados, start=col_inicio):
        celda = ws.cell(row=fila_inicio, column=col, value=encabezado)
        ws.column_dimensions[get_column_letter(col)].width = len(str(celda.value)) + 1
        # Aplicar estilo de encabezado si se proporciona
        if styles and col not in not_styles:
            apply_cell_styles(celda, styles['headers'])
            celda.border = BORDER

    # Write your main data
    for fila_idx, fila in enumerate(filas, start=fila_inicio + 1):
        for col_idx, valor in enumerate(fila, start=col_inicio):
            ws.row_dimensions[fila_idx].height = 25
            celda = ws.cell(row=fila_idx, column=col_idx, value=valor)
            if ws.column_dimensions[get_column_letter(col_idx)].width < len(str(celda.value)):
                ws.column_dimensions[get_column_letter(col_idx)].width = len(str(celda.value)) + 1
            # Aplicar estilo a las celdas de datos si se proporciona
            if styles and col_idx not in not_styles:
                apply_cell_styles(celda, styles['data'])
                celda.border = BORDER

# matplotlib section

# Apply a new image for your excel report specifying a position and a worksheet
def set_img(ws, position, fig):
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    img_buffer.seek(0)

    excel_image = OpenpyxlImage(img_buffer)
    ws.add_image(excel_image, position)

# Apply graph styles for your matplotlib picture/figure
def apply_graph_styles(ws, ax, main_dic, fig, grid=False):
    ax.set_title(main_dic['main_title'], fontsize=10, fontweight="bold")
    if 'x_title' in main_dic:
        ax.set_xlabel(main_dic['x_title'], fontsize=10)
    if 'y_title' in main_dic:
        ax.set_ylabel(main_dic['y_title'], fontsize=10)
    ax.tick_params(axis='x', rotation=25)

    fig.patch.set_facecolor(main_dic['facecolor'])  # Fondo exterior
    ax.set_facecolor(main_dic['background'])         # Fondo del área de gráfico

    if grid == True:
        ax.grid(color = 'black', linestyle = '-', linewidth = 0.5)

    set_img(ws, main_dic['position'], fig)

# Specific function to create a bar graph
def bar(ws, main_dic):
    fig, ax = plt.subplots(figsize=main_dic['figsize'])

    x_labels = main_dic['labels']
    graph_values = main_dic['graph_values']
    bar_colors = main_dic['colors']

    if 'legend' in main_dic:
        bar_labels = x_labels
        ax.bar(x_labels, graph_values, label=bar_labels, color=bar_colors, edgecolor='black')
        ax.legend(title='Legend title', loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    else:
        ax.var(x_labels, graph_values, color=bar_colors, edgecolor='black')

    # Show values above each bar
    for i, val in enumerate(graph_values):
        ax.text(i, val + .2, f"{val}", ha="center", fontsize=8)

    apply_graph_styles(ws, ax, main_dic, fig)

# Specific function to create a lineal graph
def line(ws, main_dic):
    fig, ax = plt.subplots(figsize=main_dic['figsize'])
    # ax.plot(main_dic['labels'], main_dic['graph_values'], main_dic['labels_b'], main_dic['graph_values_b'], marker='o', linestyle='-')
    ax.plot(main_dic['labels'], main_dic['graph_values'], marker='o', linestyle='-')

    # Show values for each point
    for i, valor in enumerate(main_dic['graph_values']):
        ax.text(main_dic['labels'][i], valor + 1, str(valor), ha='center', fontsize=10, color='black')

    apply_graph_styles(ws, ax, main_dic, fig, True)

# Specific function to create a pie chart
def pie(ws, main_dic):
    fig, ax = plt.subplots()
    graph_values = main_dic['graph_values']
    ax.pie(graph_values, labels=main_dic['labels'], autopct='%1.1f%%', shadow=True,
        textprops={'color': 'black', 'font': 'Courier New', 'weight': 'bold', 'size': 10})
    plt.legend(title="Ingredients", loc="center left", bbox_to_anchor=(1, 1))
    
    apply_graph_styles(ws, ax, main_dic, fig)

# Specific function to create a histogram
def histogram(ws, main_dic):
    fig, ax = plt.subplots()
    graph_values = main_dic['graph_values']
    set_values = len(set(graph_values))

    n, bins, patches = ax.hist(graph_values, bins=set_values, color="darkgreen", edgecolor="black")

    # Show values for each bar
    for count, bin_left, bin_right in zip(n, bins[:-1], bins[1:]):
        x = (bin_left + bin_right) / 2  # punto medio del bin
        ax.text(x, count + 1, str(int(count)), ha='center', fontsize=10)

    apply_graph_styles(ws, ax, main_dic, fig)

# Specific function to create a scatter graph
def scatter(ws, main_dic):
    fig, ax = plt.subplots()
    graph_values = main_dic['graph_values']
    colors = [i for i in range(len(graph_values))]
    graph_values_b = main_dic['graph_values_b']
    sc = ax.scatter(np.array(graph_values), np.array(graph_values_b), c=np.array(colors), cmap='viridis')

    # Show values for every little point
    if 'values' in main_dic:
        for i in range(len(graph_values)):
            ax.text(graph_values[i], graph_values_b[i] + .4, f"({graph_values[i]}, {graph_values_b[i]})", fontsize=9, ha='right', color='black')

    plt.colorbar(sc, ax=ax)

    apply_graph_styles(ws, ax, main_dic, fig, True)