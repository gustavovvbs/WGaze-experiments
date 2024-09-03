from psychopy import visual, core, event
import numpy as np

# Crie uma janela
win = visual.Window(size=(800, 600), units='pix', fullscr=True)

# Defina as posições e etiquetas das teclas com distância horizontal ajustada
horizontal_spacing = 180 # Ajuste esse valor para aumentar ou diminuir a distância
keys = [
    ('Q', [-350, 400]), ('W', [-350 + horizontal_spacing, 400]), 
    ('E', [-350 + 2 * horizontal_spacing, 400]), ('R', [-350 + 3 * horizontal_spacing, 400]), 
    ('T', [-350 + 4 * horizontal_spacing, 400]),
    ('Y', [-350 + 5 * horizontal_spacing, 400]), ('U', [-350 + 6 * horizontal_spacing, 400]), 
    ('I', [-350 + 7 * horizontal_spacing, 400]), ('O', [-350 + 8 * horizontal_spacing, 400]), 
    ('P', [-350 + 9 * horizontal_spacing, 400]),
    ('A', [-300, 200]), ('S', [-300 + horizontal_spacing, 200]), 
    ('D', [-300 + 2 * horizontal_spacing, 200]), ('F', [-300 + 3 * horizontal_spacing, 200]), 
    ('G', [-300 + 4 * horizontal_spacing, 200]),
    ('H', [-300 + 5 * horizontal_spacing, 200]), ('J', [-300 + 6 * horizontal_spacing, 200]), 
    ('K', [-300 + 7 * horizontal_spacing, 200]), ('L', [-300 + 8 * horizontal_spacing, 200]),
    ('Z', [-275, 0]), ('X', [-275 + horizontal_spacing, 0]), 
    ('C', [-275 + 2 * horizontal_spacing, 0]), ('V', [-275 + 3 * horizontal_spacing, 0]),
    ('B', [-275 + 4 * horizontal_spacing, 0]), ('N', [-275 + 5 * horizontal_spacing, 0]), 
    ('M', [-275 + 6 * horizontal_spacing, 0])
]

for key in keys:
    key[1][1] -= 200
    key[1][0] -= 400



# Crie retângulos e etiquetas das teclas
key_rectangles = []
key_labels = []

for label, pos in keys:
    rect = visual.Rect(win, width=160, height=160, pos=pos, lineColor='black', fillColor='lightgray')
    text = visual.TextStim(win, text=label, pos=pos, color='black', height=50)  # Ajuste o tamanho da fonte se necessário
    key_rectangles.append(rect)
    key_labels.append(text)

# Defina o tempo de exibição em segundos
display_time = 200.0

# Desenhe o teclado e exiba por um tempo determinado
start_time = core.getTime()
while core.getTime() - start_time < display_time:
    for rect, text in zip(key_rectangles, key_labels):
        rect.draw()
        text.draw()
    
    win.flip()
    
    # Verifique se a tecla de escape foi pressionada
    keys = event.getKeys()
    if 'escape' in keys:
        break

# Feche a janela
win.close()
core.quit()

