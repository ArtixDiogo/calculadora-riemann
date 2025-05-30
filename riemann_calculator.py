# riemann_calculator.py
import numpy as np

def calcular_soma_riemann(func, a, b, n, metodo='medio'):
    """
    Calcula a Soma de Riemann para uma dada função.

    Parâmetros:
    func (callable): A função f(x) a ser integrada.
    a (float): Limite inferior do intervalo.
    b (float): Limite superior do intervalo.
    n (int): Número de retângulos.
    metodo (str): 'esquerdo', 'direito' ou 'medio' para o tipo de soma.

    Retorna:
    float: O valor aproximado da integral (Soma de Riemann).
    numpy.ndarray: Coordenadas x dos pontos para os retângulos.
    numpy.ndarray: Alturas y dos retângulos.
    float: Largura delta_x de cada retângulo.
    """
    if n <= 0:
        raise ValueError("O número de retângulos (n) deve ser positivo.")
    if a >= b:
        raise ValueError("O limite inferior (a) deve ser menor que o limite superior (b).")

    delta_x = (b - a) / n
    pontos_x = np.linspace(a, b, n + 1) # n+1 pontos para definir n intervalos

    if metodo == 'esquerdo':
        # Usa o ponto esquerdo de cada subintervalo
        xi = pontos_x[:-1] # Pega todos os pontos exceto o último
    elif metodo == 'direito':
        # Usa o ponto direito de cada subintervalo
        xi = pontos_x[1:]  # Pega todos os pontos exceto o primeiro
    elif metodo == 'medio':
        # Usa o ponto médio de cada subintervalo
        xi = (pontos_x[:-1] + pontos_x[1:]) / 2
    else:
        raise ValueError("Método inválido. Escolha 'esquerdo', 'direito' ou 'medio'.")

    alturas_y = func(xi)
    soma = np.sum(alturas_y * delta_x)

    # Para plotagem dos retângulos, precisamos dos pontos x da base de cada retângulo
    # e suas alturas.
    # Se for esquerdo, o x do retângulo é o xi.
    # Se for direito, o x do retângulo é xi - delta_x (para começar da esquerda).
    # Se for médio, o x do retângulo é xi - delta_x / 2.

    if metodo == 'esquerdo':
        x_retangulos = xi
    elif metodo == 'direito':
        # Os pontos xi são os cantos direitos, então para desenhar o retângulo
        # a partir da esquerda, subtraímos delta_x
        x_retangulos = xi - delta_x
    elif metodo == 'medio':
        # Os pontos xi são os pontos médios, então para desenhar o retângulo
        # a partir da esquerda, subtraímos delta_x/2
        x_retangulos = xi - delta_x / 2

    return soma, x_retangulos, alturas_y, delta_x