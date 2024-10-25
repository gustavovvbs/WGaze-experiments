import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Leia os dados
data = pd.read_csv('data_gustavo3.csv')

# Preencher valores NaN com 0
data = data.fillna(0)
word = data.iloc[0].loc['word']
# Obtenha a resposta da linha 3 (verifique se 'response' está correto)
gaze_points = data.iloc[0].loc['response']

# Limpe a string removendo caracteres nulos ou indesejados
cleaned_gaze_points = gaze_points.replace('\x00', '').strip()

# Converta a string em um array
try:
    array = np.array(eval(cleaned_gaze_points))
except SyntaxError:
    print("Erro ao avaliar a string. Verifique o formato dos dados.")
    array = None

# Verifique se o array foi criado corretamente
if array is not None:
    # Separe as coordenadas x e y
    x_coords = array[:, 0]
    y_coords = array[:, 1]

    # Plote as coordenadas
    plt.plot(x_coords, y_coords)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'focos de visao para {word}')
    plt.show()