from psychopy import visual, core, event, gui, data
import os
from live_gaze import EyeTrackerManager
from testeppy import write_buffer_to_file

''' 
    TO DO AQ: BOTAR P ELE PEGAR UMA PALAVRA ALEATORIA EM CADA TENTATIVA NO TRIAL 
    FAZER A BOLINHA APARECER 
    SALVAR O ARQUIVO EM FORMATO DE LOG, NO LUGAR DO FORMATO SEBOSO Q TA AGORA 
'''
win = visual.Window(size = (2048, 1152), units='pix', fullscr=True)

horizontal_spacing = 180 
keys = [
    ('Q', [-350, 400]), ('W', [-350 + horizontal_spacing, 400]),
    ('E', [-350 + 2 * horizontal_spacing, 400]), ('R', [-350 + 3 * horizontal_spacing, 400]),
    ('T', [-350 + 4 * horizontal_spacing, 400]), ('Y', [-350 + 5 * horizontal_spacing, 400]),
    ('U', [-350 + 6 * horizontal_spacing, 400]), ('I', [-350 + 7 * horizontal_spacing, 400]),
    ('O', [-350 + 8 * horizontal_spacing, 400]), ('P', [-350 + 9 * horizontal_spacing, 400]),
    ('A', [-300, 200]), ('S', [-300 + horizontal_spacing, 200]),
    ('D', [-300 + 2 * horizontal_spacing, 200]), ('F', [-300 + 3 * horizontal_spacing, 200]),
    ('G', [-300 + 4 * horizontal_spacing, 200]), ('H', [-300 + 5 * horizontal_spacing, 200]),
    ('J', [-300 + 6 * horizontal_spacing, 200]), ('K', [-300 + 7 * horizontal_spacing, 200]),
    ('L', [-300 + 8 * horizontal_spacing, 200]),
    ('Z', [-275, 0]), ('X', [-275 + horizontal_spacing, 0]),
    ('C', [-275 + 2 * horizontal_spacing, 0]), ('V', [-275 + 3 * horizontal_spacing, 0]),
    ('B', [-275 + 4 * horizontal_spacing, 0]), ('N', [-275 + 5 * horizontal_spacing, 0]),
    ('M', [-275 + 6 * horizontal_spacing, 0]),
    ('BOTAO_ACABAR', [-100, -200])
]

for key in keys:
    key[1][1] -= 200  
    key[1][0] -= 400  


def get_participant_info():
    participant_dialog = gui.Dlg(title="Informações do Participante")
    participant_dialog.addField("Nome")
    participant_dialog.addField("Idade")
    participant_dialog.addField("Genero", choices=["Masculino", "Feminino", "Outro", "Prefiro não informar"])
    
    participant_data = participant_dialog.show() 
    if participant_dialog.OK:
        return {'name': participant_data['Nome'], 'age': participant_data['Idade'], 'gender': participant_data['Genero']}
    else:
        core.quit()

win.winHandle.set_fullscreen(False)
win.winHandle.minimize()
win.flip()
participant_info = get_participant_info()

experiment_filename = f"data_{participant_info['name']}.csv"  
this_exp = data.ExperimentHandler(
    name='WordExperiment',
    version='1.0',
    extraInfo=participant_info,  
    dataFileName=experiment_filename  
)

win.winHandle.maximize()
win.winHandle.activate()
win.winHandle.set_fullscreen(True)
win.flip()

words = ['primeiro', 'tarde', 'casa', 'árvore', 'rio']

conditions = [{'word': word} for word in words]

key_rectangles = []
key_labels = []
for label, pos in keys:
    rect = visual.Rect(win, width=160, height=160, pos=pos, lineColor='black', fillColor='lightgray')
    text = visual.TextStim(win, text=label, pos=pos, color='black', height=50)  # Ajuste o tamanho da fonte se necessário
    key_rectangles.append(rect)
    key_labels.append(text)
    rect_yellow = visual.Rect(win, width=160, height=160, pos=(0, 0), lineColor='yellow', fillColor='lightgray')

trials = data.TrialHandler(
    trialList=conditions,  
    nReps=2,               
    method='random'         
)

this_exp.addLoop(trials)

def run_trial(trial):
    with EyeTrackerManager() as et:
        # Exibe a palavra por 1 segundo antes de mostrar o teclado
        word_stim = visual.TextStim(win, text=trial['word'], pos=(0, 450), color='black', height=50)
        word_stim.draw()
        win.flip()
        core.wait(1)  # Mostra a palavra por 1 segundo

        # Exibe o teclado e começa a capturar os pontos de gaze            
        response = None
        clock_tracker = core.Clock()
        gazes_draw = []
        data_buffer = []

        progress_bar = visual.Rect(win, width=0.0, height=0.05, pos=(0, -0.5), fillColor='green', lineColor='white')
        space_hold_timer = core.Clock()
        space_bar_fill = 0
        holding_space = False 
        required_hold_time = 1.0
        fixation_time = core.Clock()

        while True:
            x, y = et.latest_gaze
            target_area = keys[-1][1]
            if x is not None and y is not None:
                actual_gaze = visual.ImageStim(win, image='/Users/saladeux/Documents/WGaze-experiments/EXP/Stimuli/circle.png', size=(80, 80), pos=(x, y))
                gazes_draw.append(actual_gaze)
                data_buffer.append([x, y])
                print(x, y)
                actual_gaze.draw()

                target_limits = [-300, 300, -300, 300]

                if target_area[0] - 60 <= x <= target_area[0] + 60 and target_area[1] - 60<=y <= target_area[1] +60:
                    if fixation_time.getTime() > 1.5:
                        print('olhou por um segundo')
                        break 
                    else:
                        fixation_time.reset()
            
            
            for rect, textin in zip(key_rectangles, key_labels):
                rect.draw()
                textin.draw()
                rect_yellow.draw()

            word_stim.draw()

            win.flip()

        if data_buffer:
            trials.addData('response', data_buffer)





# Executa todos os trials
for trial in trials:
    run_trial(trial)
    this_exp.nextEntry()

# Finaliza e salva os dados
this_exp.saveAsWideText(experiment_filename)
this_exp.saveAsPickle(experiment_filename)

# Mensagem final
end_stim = visual.TextStim(win, text="Experimento finalizado! Obrigado!", pos=(0, 0), color='black', height=50)
end_stim.draw()
win.flip()
core.wait(3)

# Fechar a janela
win.close()
core.quit()

