from psychopy import visual, core, event, gui, data
import os
from live_gaze import EyeTrackerManager


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
    ('M', [-275 + 6 * horizontal_spacing, 0])
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
    text = visual.TextStim(win, text=label, pos=pos, color='black', height=50) 
    key_rectangles.append(rect)
    key_labels.append(text)

trials = data.TrialHandler(
    trialList=conditions,  
    nReps=2,               
    method='random'         
)

this_exp.addLoop(trials)

def run_trial(trial):
    with EyeTrackerManager() as et:
        word_stim = visual.TextStim(win, text=trial['word'], pos=(0, 450), color='black', height=50)

        response = None
        clock_tracker = core.Clock()
        gazes_draw = []
        data_buffer = []

        while True:
            x, y = et.latest_gaze
            if x is not None and y is not None:
                actual_gaze = visual.ImageStim(win, image='/Users/saladeux/Documents/WGaze-experiments/EXP/Stimuli/circle.png', size=(80, 80), pos=(x, y))
                gazes_draw.append(actual_gaze)
                data_buffer.append([x, y])
                actual_gaze.draw()


            for rect, textin in zip(key_rectangles, key_labels):
                rect.draw()
                textin.draw()

            word_stim.draw()


            win.flip()
            key = event.getKeys()

            if 'space' in key:
                break

        if data_buffer:
            trials.addData('response', data_buffer)

for trial in trials:
    run_trial(trial)
    this_exp.nextEntry()

# Finaliza e salva os dados
this_exp.saveAsWideText(experiment_filename)
# this_exp.saveAsPickle(experiment_filename)

end_stim = visual.TextStim(win, text="Experimento finalizado! Obrigado!", pos=(0, 0), color='black', height=50)
end_stim.draw()
win.flip()
core.wait(3)

win.close()
core.quit()

