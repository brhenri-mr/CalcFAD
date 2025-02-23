from fad.utils  import tensaoArmadura, drawSectionT, draw_figure
from fad.models import Elemento
import FreeSimpleGUI as sg
from PIL import Image
import keyboard
import pickle
from copy import deepcopy

sg.theme('Reddit')
#sg.theme('SystemDefault')

save_path = None

IMG_PATH = 'T.png'

TAMANHO_TEXT = (4, 1)
TAMANHO_TEXTINPUT = (16,1)
TAMANHO_TEXT_RED = (3, 1)
TAMANHO_UNID = (5, 1)

DESCRIPT = [
    "Barras retas pi dobradas com D>25",
    "D ={8ø com ø>20}",
    "D ={5ø com ø<20}",
    "D ={3ø com ø<=10}",
    "Agressividade IV",
    "Barras soldadas incluindo solda por pontos ou exterimandades"
]


POD = {'Vigas':0.5,
       'Transversina':0.7,
       'Laje ou tabuleiro':0.8,
       'Ponte ferroviária':1,
       'Pont Rolante':1}

BITOLAS = [10, 12.5, 16, 20, 22, 25, 32, 40]


layout_entradas = [ [sg.Text('1.1 Carregamentos')],
            [sg.Combo(list(POD.keys()), s=(28,1), enable_events=True, readonly=True, k='-POND-')],
            [sg.Text('Mg=',size=TAMANHO_TEXT), sg.InputText(size=TAMANHO_TEXTINPUT, k='-MG-'), sg.Text('kN.cm', size=TAMANHO_UNID)],
            [sg.Text('M+=',size=TAMANHO_TEXT), sg.InputText(size=TAMANHO_TEXTINPUT, k='-M+-'), sg.Text('kN.cm', size=TAMANHO_UNID)],
            [sg.Text('M-=',size=TAMANHO_TEXT), sg.InputText(size=TAMANHO_TEXTINPUT, k='-M--'), sg.Text('kN.cm', size=TAMANHO_UNID)],
            [sg.Text('1.2 Propriedades geométricas Amadura')],
            [sg.Combo(DESCRIPT, s=(28,1), enable_events=True, readonly=True, k='-COMBO-')],
            [sg.Text('Ainf=',size=TAMANHO_TEXT), sg.InputText(size=TAMANHO_TEXTINPUT, k='-QINF-'), sg.Combo(BITOLAS, s=(3,1), enable_events=True, readonly=True, k='-øINF-')],
            [sg.Text('Asup=',size=TAMANHO_TEXT), sg.InputText(size=TAMANHO_TEXTINPUT, k='-QSUP-'), sg.Combo(BITOLAS, s=(3,1), enable_events=True, readonly=True, k='-øSUP-')],
            [sg.Text('i=',size=TAMANHO_TEXT), sg.InputText(size=TAMANHO_TEXTINPUT, k='-I-'), sg.Text('cm', size=TAMANHO_UNID)],
            [sg.Text('s=',size=TAMANHO_TEXT), sg.InputText(size=TAMANHO_TEXTINPUT, k='-S-'), sg.Text('cm', size=TAMANHO_UNID)],
            [sg.Text('1.3 Propriedades geométricas Seção')],
            [sg.Text('bw=',size=TAMANHO_TEXT), sg.InputText(size=TAMANHO_TEXTINPUT, k='-BW-'), sg.Text('cm', size=TAMANHO_UNID)],
            [sg.Text('bf=',size=TAMANHO_TEXT), sg.InputText(size=TAMANHO_TEXTINPUT, k='-BF-'), sg.Text('cm', size=TAMANHO_UNID)],
            [sg.Text('h=',size=TAMANHO_TEXT), sg.InputText(size=TAMANHO_TEXTINPUT, k='-H-'), sg.Text('cm', size=TAMANHO_UNID)],
            [sg.Text('hf=',size=TAMANHO_TEXT), sg.InputText(size=TAMANHO_TEXTINPUT, k='-HF-'), sg.Text('cm', size=TAMANHO_UNID)]]

layout_resultados = [
                    [sg.Text('', k='-TSUP-')],
                    [sg.Text('', k='-TINF-')]
                    ]


layout_tab1 = [[sg.Image(IMG_PATH, key='-IMG-')]]

layout_tab2 = [[sg.Canvas(key="-COMBMAX-")],]

layout_tab3 = [[sg.Canvas(key="-COMBMIN-")],]


# All the stuff inside your window.
layout = [ [sg.Menu([['Arquivo', ['Open', 'Save', 'About']]])],
    [sg.Frame('Dados de Entrada',layout_entradas),
             sg.Column([
                        [sg.TabGroup([[sg.Tab('Dados', layout_tab1),
                                    sg.Tab('Mmáx', layout_tab2),
                                    sg.Tab('Mmín', layout_tab3),
                                    ]])],
                        [sg.Frame('Resultados', layout_resultados, vertical_alignment='top', size=(466, 120))]
                        ], vertical_alignment='top' )
             ],
            [sg.Button('Calcular', bind_return_key=True), sg.Button('Cancel')]]

layout_about = [
    [sg.Text("Sobre o Programa", font=("Arial", 14, "bold"))],
    [sg.Text("Programa para análise de fadiga (NBR 6118:2023 e Marchetti (2008)) induzida por flexão em elementos lineares ou simplificadamente lineares (lajes).", size=(55, 2))],
    [sg.Text("Versão: 1.0")],
    [sg.Text("Desenvolvido por: Breno Henrique Mariano Rodrigues")],
    [sg.Text("github: https://github.com/brhenri-mr/CalcFAD")]
]

# Create the Window
window = sg.Window('Calculadora Fadiga', layout, icon='Equibris.ico', return_keyboard_events=True)
fig_canvas_agg = []  # Inicializa sem o gráfico

# Event Loop to process "events" and get the "values" of the inputs
while True:
    erro = False
    event, values = window.read(timeout=100)

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == 'Open' or keyboard.is_pressed('ctrl+o'):
        open_path = sg.popup_get_file("", no_window=True, file_types=(("FAD Files", "*.fad"), ("Todos os arquivos", "*.*")))

        # Verificando se há um caminho
        if open_path:
            with open(open_path, 'rb') as arquivo:
                open_input = pickle.load(arquivo)

            # Carregando os valores salvos
            window.fill(open_input)
            window.set_title(open_path.split('/')[-1].replace('.fad',''))
            save_path = open_path

    elif event == 'Save' or keyboard.is_pressed('ctrl+s'):

        if not save_path:
            save_path = sg.popup_get_file("Salvar como:", no_window=True, save_as=True, default_extension=".fad")

        if save_path:
            # Removendo valores que causam problemas
            values_output = deepcopy(values)
            values_output.pop('-COMBMAX-')
            values_output.pop('-COMBMIN-')
            values_output.pop(1)
            values_output.pop(0)

            with open(save_path, 'wb') as arquivo:
                pickle.dump(values_output, arquivo)
            sg.popup('Arquiv salvo com sucesso', )


    elif event == 'About':
        # Criando a nova janela
        new_window = sg.Window('Nova Janela', layout_about)
            
        # Loop para a nova janela
        while True:
            event2, values2 = new_window.read()
            if event2 == sg.WIN_CLOSED or event2 == 'Fechar':
                break
        new_window.close()


    calcular = not '' in values.values()
    if event == 'Calcular' and calcular:
        try:
            # Verificação de letras nos campos
            for chave, field_valor in values.items():
                try:
                    if chave not in['-POND-', '-COMBO-', '-COMBMAX-', '-COMBMIN-', 0, 1] and isinstance(field_valor, str):

                        float(field_valor.replace(',','.')) # Froçando o erro

                except:
                    sg.popup("Os campos devem ser preenchidos com números.", title="Aviso")
                    erro = True
                    break

            # Verificando se algum valor geométrico está negativo
            for field_valor in ['-BW-','-BF-', '-H-', '-HF-', '-S-', '-I-', '-QSUP-', '-QINF-']:
                if '-' in values[field_valor]:
                    sg.popup("As propriedades geométricas devem ser valores positivos.", title="Aviso")
                    erro = True
                    break
            
            if erro:
                pass

            # Verificando se as barras são númeor inteiros
            elif '.' in values['-QSUP-'] or '.' in values['-QINF-']:
                sg.popup("A quantidade de Barras precisa ser um número inteiro.", title="Aviso")


            else:
                # Instancia do objeto
                element = Elemento(fck='C30',
                            descricao=values['-COMBO-'],
                            bitolas=values['-øINF-'],
                            bitolai=values['-øSUP-'],
                            bw =float(values['-BW-'].replace(',','.')),
                            bf= float(values['-BF-'].replace(',','.')),
                            h=float(values['-H-'].replace(',','.')),
                            hf=float(values['-HF-'].replace(',','.')),
                            i=float(values['-I-'].replace(',','.')),
                            s=float(values['-S-'].replace(',','.')),
                            bitolainf=values['-øINF-'],
                            bitolasup=values['-øSUP-'],
                            qdntsup=float(values['-QSUP-'].replace(',','.')),
                            qndtinf=float(values['-QINF-'].replace(',','.')))



                # Construindo os carregamentos
                momento_max_comb = float(values['-MG-'].replace(',','.')) + POD[values['-POND-']]*float(values['-M+-'].replace(',','.'))
                momento_min_comb = float(values['-MG-'].replace(',','.')) + POD[values['-POND-']]*float(values['-M--'].replace(',','.'))

                # Calculo da tensão no concreto
                tensao = [element.tensaoConcreto(momento) for momento in [momento_max_comb, momento_min_comb]]
                
                # Calculo do gradiente de tensão nas armaduras
                deltatensao = [tensaoArmadura(sigmac=tensao[0], 
                                            sigmacmin=tensao[1], 
                                            d_max=element.d_posi if momento_max_comb>=0 else element.d_neg, 
                                            d_min=element.d_posi if momento_min_comb>=0 else element.d_neg,
                                            dlinha_min=element.dlinha_posi if momento_min_comb>=0 else element.dlinha_neg,
                                            dlinha_max=element.dlinha_posi if momento_max_comb>=0 else element.dlinha_neg, 
                                            x_max= element.x_posi if momento_max_comb>=0 else element.x_neg, 
                                            x_min=element.x_posi if momento_min_comb>=0 else element.x_neg,
                                            ae=element.ae, 
                                            TYPE=tipo) for tipo in ['Inferior', 'Superior']]

                # Atualizando os valores na tela
                resis_sup = element.fss # Acressimo toleravel  a fadiga superior
                resis_inf = element.fsi # Acressimo toleravel a fadiga inferior

                sup_token = '>' if resis_sup<deltatensao[1] else '<'
                inf_token = '>' if resis_inf<deltatensao[0] else '<'

                verificado_sup = 'Não Verificado' if resis_sup<deltatensao[1] else 'Verificado'
                verificado_inf = 'não Verificado' if resis_inf<deltatensao[0] else 'Verificado'


                window['-TSUP-'].update(f'Situação das armaduras superiores: {round(deltatensao[1], 2)}{sup_token}{resis_sup} MPa --> {verificado_sup}')
                window['-TINF-'].update(f'Situação das armaduras inferiores: {round(deltatensao[0], 2)}{inf_token}{resis_inf} MPa --> {verificado_inf}' )

                # Apagando gráfico anterior
                if len(fig_canvas_agg) != 0:
                        for fig_canvas in fig_canvas_agg:
                            fig_canvas.get_tk_widget().forget()

                # Desenhando as seções T para combinação máxima e mínima 
                for x, comb, sinal in [(element.x_posi, "-COMBMAX-", abs(momento_max_comb)/momento_max_comb),(element.x_neg, "-COMBMIN-", abs(momento_min_comb)/momento_min_comb)]:
                    
                    # Inicializando os objetos
                    canvas_elem = window[comb].Widget # recuperando o canvas
                    figura = drawSectionT(bw=element.bw, bf=element.b, h=element.h, hf=element.hf, x= x, momento=sinal) # Desenhando a seção

                    try:
                        fig_canvas_agg.append(draw_figure(canvas=canvas_elem, figure=figura)) # Aplicando a seção ao canvas 

                    except:
                        print('Erro ao tentar desenhar a seção')

        except Exception as e:
            sg.popup(f'Um erro ocorreu, favor reportar {e}')

window.close()

