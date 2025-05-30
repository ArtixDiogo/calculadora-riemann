# plotter.py
import matplotlib.pyplot as plt
import numpy as np

def plotar_riemann(ax, func_matematica, a, b, n, metodo_soma,
                   x_retangulos=None, alturas_retangulos=None, delta_x_retangulos=None,
                   area_calculada=None):
    """
    Plota a função, os retângulos da Soma de Riemann e a área.

    Parâmetros:
    ax (matplotlib.axes.Axes): O eixo onde o gráfico será desenhado.
    func_matematica (callable): A função f(x) a ser plotada.
    a (float): Limite inferior do intervalo.
    b (float): Limite superior do intervalo.
    n (int): Número de retângulos.
    metodo_soma (str): Método da soma de Riemann ('esquerdo', 'direito', 'medio').
    x_retangulos (numpy.ndarray, opcional): Coordenadas x da base dos retângulos.
    alturas_retangulos (numpy.ndarray, opcional): Alturas y dos retângulos.
    delta_x_retangulos (float, opcional): Largura delta_x dos retângulos.
    area_calculada (float, opcional): Valor da área calculada para exibir no título.
    """
    ax.clear() # Limpa o gráfico anterior

    # Plota a função original
    x_func = np.linspace(a, b, 400)
    y_func = func_matematica(x_func)
    ax.plot(x_func, y_func, 'b-', label=f'f(x)', linewidth=2) # Linha azul para a função

    # Preenche a área sob a curva (opcional, mas bom para visualização)
    ax.fill_between(x_func, y_func, alpha=0.1, color='blue')

    if x_retangulos is not None and alturas_retangulos is not None and delta_x_retangulos is not None:
        # Plota os retângulos da Soma de Riemann
        for i in range(len(x_retangulos)):
            ax.add_patch(plt.Rectangle((x_retangulos[i], 0), delta_x_retangulos, alturas_retangulos[i],
                                       edgecolor='black', facecolor='red', alpha=0.5))
            # Adiciona um ponto no topo do retângulo onde a função foi avaliada
            if metodo_soma == 'esquerdo':
                ponto_x_avaliacao = x_retangulos[i]
            elif metodo_soma == 'direito':
                ponto_x_avaliacao = x_retangulos[i] + delta_x_retangulos
            elif metodo_soma == 'medio':
                ponto_x_avaliacao = x_retangulos[i] + delta_x_retangulos / 2
            else: # Caso padrão (ou erro)
                ponto_x_avaliacao = x_retangulos[i]

            ax.plot(ponto_x_avaliacao, alturas_retangulos[i], 'bo', markersize=4) # Ponto azul


    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    titulo = f'Soma de Riemann ({metodo_soma.capitalize()}) com n={n}'
    if area_calculada is not None:
        titulo += f'\nÁrea Aproximada: {area_calculada:.4f}'
    ax.set_title(titulo)
    ax.legend()
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.5) # Linha do eixo x
    ax.axvline(0, color='black', linewidth=0.5) # Linha do eixo y

    # Ajusta os limites para melhor visualização
    y_min, y_max = ax.get_ylim()
    if min(alturas_retangulos if alturas_retangulos is not None else [0]) < 0:

        ax.set_ylim(min(y_min, min(alturas_retangulos if alturas_retangulos is not None else [0]) -1), max(y_max, max(alturas_retangulos if alturas_retangulos is not None else [0]) + 1))
    else:
        ax.set_ylim(min(y_min, -0.5), max(y_max, max(alturas_retangulos if alturas_retangulos is not None else [0]) + 1) )

    plt.tight_layout()