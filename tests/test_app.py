import FreeSimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Função para desenhar o gráfico e exibir na GUI
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

# Layout da interface
layout = [[sg.Text("Clique para gerar o gráfico")],
          [sg.Canvas(key="-CANVAS-")],  # Canvas para o gráfico
          [sg.Button("Gerar Gráfico"), sg.Button("Fechar")]]

# Criar a janela
window = sg.Window("Gráfico no PySimpleGUI", layout, finalize=True)
fig_canvas_agg = None  # Inicializa sem o gráfico

while True:
    event, values = window.read()
    
    if event in (sg.WIN_CLOSED, "Fechar"):
        break

    elif event == "Gerar Gráfico":
        if fig_canvas_agg:
            fig_canvas_agg.get_tk_widget().forget()  # Remove gráfico anterior

        fig, ax = plt.subplots()
        ax.plot([0, 1, 2, 3, 4], [10, 20, 25, 30, 40], marker="o")  # Gráfico gerado só quando necessário
        ax.set_title("Gráfico no PySimpleGUI")

        # Insere o novo gráfico
        canvas_elem = window["-CANVAS-"].Widget
        fig_canvas_agg = draw_figure(canvas_elem, fig)

window.close()
