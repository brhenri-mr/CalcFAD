import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
from shapely.geometry import Polygon as ShapelyPolygon, LineString
from shapely.geometry.polygon import orient
from shapely.ops import split

def tensaoArmadura(sigmac:float, 
                   sigmacmin:float, 
                   d_max:float, 
                   d_min:float,
                   dlinha_max:float,
                   dlinha_min:float,
                   x_max:float, 
                   x_min:float,
                   ae:int,
                   TYPE='Inferior') -> float:
    '''
    Função para cálculo do gradiente de tensão induzido por fadiga nas armaduras

    Parameters
    ----------
    sigmac: tensão atuante no concreto
    sigmacmin: tensão mínima atuante no concreto
    d:altura útil do concreto
    x:Altura da linha neutra da seção
    ae: proporçao entre módulo de elasticidade do aço/concreto
    '''

    # Diferenciando entre posição da armadura
    if TYPE == 'Inferior':
        tension_max = ae*sigmac*(d_max - x_max)/x_max # Tensão máxima 
        tension_min = ae*sigmacmin*(d_min - x_min)/x_min # Tensão mínima 

    else: 
        tension_max = ae*sigmac*(x_max - dlinha_max)/x_max # Tensão máxima 
        tension_min = ae*sigmacmin*(x_min - dlinha_min)/x_min # Tensão mínima 

    return (tension_max - tension_min)*10


def draw_figure(canvas, figure):
    '''
    Função que adiciona um desenho do matplotlib ao GUI do SimpleGui

    Parameters
    ----------
    canvas: Canvas do SimpleGUi
    figura: Figura do matplotlib

    
    '''
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

# Função para desenhar o polígono no gráfico
def draw_polygon(polygon, ax, color):
    '''
    Função para plotar o polygono em uma figura do matplotlib
    '''
    if polygon.is_empty:
        return
    x, y = polygon.exterior.xy
    ax.fill(x, y, alpha=0.5, fc=color, edgecolor='black', linewidth=3)



def drawSectionT(bw:float, bf:float, h: float, hf:float, x:float, momento:int):
    '''
    Função que desenha a seção T em um plot do matplotlib

    Paramters
    ---------
    bw: comprimento da base da superior geométrica
    bf: comprimento da base superior da figura geométrica
    h: altura da seção 
    hf: Espessura do talão
    x: altura da linha neutra
    '''

    origem = bw/2 # Definição da origem do desenh ocomo sendo o meio da figura geométrica
    # Definir o tamanho desejado em pixels
    desired_width = 451
    desired_height = 275

    # Definir o DPI (pontos por polegada) desejado, normalmente 100 ou 200 é uma boa escolha
    dpi = 100

    # Calcular o tamanho em polegadas (dividir o tamanho em pixels pelo DPI)
    fig_width = desired_width / dpi
    fig_height = desired_height / dpi

    # Criar a figura com o tamanho ajustado
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)

    # Definindo os vertices da seção trasnversaç
    vertices = [
    (origem, 0), # 
    (origem + bw/2, 0), 
    (origem+bw/2, h-hf), 
    (origem+bw/2+(bf-bw)/2, h-hf), 
    (origem+bw/2+(bf-bw)/2, h), 
    (origem+bw/2+(bf-bw)/2 - bf, h),  
    (origem+bw/2+(bf-bw)/2 - bf, h-hf), 
    (origem+bw/2+(bf-bw)/2 - bf + bf/2 - bw/2, h-hf), 
    (origem - bw/2, 0), 
    (origem, 0),
]
    
    # Criar o polígono no Shapely
    polygon = ShapelyPolygon(vertices)

    # Definir a linha de corte (uma linha horizontal)
    cut_line = LineString([(origem - bf, x), (origem + bf, x)])  # Corte horizontal y = 2

    # Cortar o polígono usando a lin
    collection = split(polygon, cut_line)

    draw_polygon(collection.geoms[0], ax, 'blue' if momento<0 else 'red')
    draw_polygon(collection.geoms[1], ax, 'red' if momento<0 else 'blue')

    # Linha de corte
    x_x = [-bf*1.15/2, bf*1.15]
    y_x = [x for _ in range(len(x_x))]
    ax.plot(x_x, y_x, color='red', linestyle='dashed')

    # Ajustar os limites do gráfico para que o "T" seja visível
    ax.set_xlim((origem-bf/2)*1.05, (origem+bf/2)*1.05)
    ax.set_ylim(0, h*1.05)

    # Ajustar o aspecto do gráfico
    ax.set_aspect('equal')
    #ax.axis('off')

    return fig


if __name__ == '__main__':
    drawSectionT(4,8,12,3,3)
