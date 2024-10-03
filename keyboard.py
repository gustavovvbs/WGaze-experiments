from psychopy import visual, core, event, gui, data
import os
from live_gaze import EyeTrackerManager
from testeppy import write_buffer_to_file
import tobii_research as tr

''' 
    CALIBRACAO NO EXP -> CHECAR PQ N TA PRESTANDO 
    INTEGRACAO -> PRIMEIROS PASSOS PRA INTEGRAR C A API; CHECAR WEBSOCKER
    CAPTURA DOS DADOS -> DESENVOLVER LOGICA PRA SO PEGAR DPS Q ELE PASSA O OLHO PRA DENTRO DO TECLADO PELA PRIMEIRA VEZ
'''
WIN_WIDTH = 2048
WIN_HEIGHT = 1152
DWELL_TIME = 1.5
DWELL_TOLERANCE = 0.1

win = visual.Window(size=(WIN_WIDTH, WIN_HEIGHT), units='pix', fullscr=True)

win_width = win.size[0]
win_height = win.size[1]

key_width = 160 * 0.75  
key_height = 160 * 0.75

horizontal_spacing = key_width * 0.25 
vertical_spacing = 200 

top_row_y = win_height / 2 - vertical_spacing * 4.6
middle_row_y = top_row_y - vertical_spacing 
bottom_row_y = middle_row_y - vertical_spacing 

row1_labels = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
row2_labels = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
row3_labels = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']

def compute_key_positions(labels, start_x, y_pos):
    positions = []
    for i, label in enumerate(labels):
        x = start_x + i * (key_width + horizontal_spacing)
        positions.append((label, [x, y_pos]))
    return positions

def calculate_start_x(num_keys):
    total_width = num_keys * key_width + (num_keys - 1) * horizontal_spacing
    start_x = -total_width / 2 + key_width / 2
    return start_x

# Calcular posições das teclas para cada linha
keys = []
start_x_row1 = calculate_start_x(len(row1_labels))
keys += compute_key_positions(row1_labels, start_x_row1, top_row_y)

start_x_row2 = calculate_start_x(len(row2_labels))
keys += compute_key_positions(row2_labels, start_x_row2, middle_row_y)

start_x_row3 = calculate_start_x(len(row3_labels))
keys += compute_key_positions(row3_labels, start_x_row3, bottom_row_y)

# Adicionar "BOTAO_ACABAR" abaixo das outras linhas
keys.append(('BOTAO_ACABAR', [0, bottom_row_y - vertical_spacing]))

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

words = ['primeiro', 'teste', 'tela', 'teste']

conditions = [{'word': word} for word in words]

# Criar estímulos das teclas
key_rectangles = []
key_labels = []
for label, pos in keys:
    rect = visual.Rect(win, width=key_width, height=key_height, pos=pos, lineColor='black', fillColor='lightgray')
    text = visual.TextStim(win, text=label, pos=pos, color='black', height=50)  # Ajuste o tamanho da fonte se necessário
    key_rectangles.append(rect)
    key_labels.append(text)
    # rect_yellow = visual.Rect(win, width=key_width, height=key_height, pos=(0, 0), lineColor='yellow', fillColor='lightgray')

trials = data.TrialHandler(
    trialList=conditions,  
    nReps=2,               
    method='random'         
)

this_exp.addLoop(trials)

def calibrate_eyetracker(eyetracker):
    if eyetracker is None:
        return

    calibration = tr.ScreenBasedCalibration(eyetracker)

    # Enter calibration mode.
    calibration.enter_calibration_mode()
    print(f"Entered calibration mode for eye tracker with serial number {eyetracker.serial_number}.")

    # Define calibration points relative to the center of the screen
    points_to_calibrate = [(0.5, 0.5), (0.1, 0.1), (0.1, 0.9), (0.9, 0.1), (0.9, 0.9)]

    dots = [visual.Circle(win, radius=40, pos=(0, 0), fillColor='black'), 
    visual.Circle(win, radius=40, pos=(-WIN_WIDTH/2 + 100, WIN_HEIGHT/2 - 100), fillColor='black'),
    visual.Circle(win, radius=40, pos=(-WIN_WIDTH/2 +100, -WIN_HEIGHT/2 +100), fillColor='black'),
    visual.Circle(win, radius=40, pos=(WIN_WIDTH/2 - 100, -WIN_HEIGHT/2 + 100), fillColor='black'),
    visual.Circle(win, radius=40, pos=(WIN_WIDTH/2 - 100, WIN_HEIGHT/2 - 100), fillColor='black')]

    for i, point in enumerate(points_to_calibrate):
        # Show the point on the screen.
        instruction = visual.TextStim(win, text="Look at the point until it disappears.", pos=(0, 0.8), color='black', height=30)
        instruction.draw()
        dots[i].draw()
        win.flip()
        core.wait(2)  

        if calibration.collect_data(point[0], point[1]) != tr.CALIBRATION_STATUS_SUCCESS:
            calibration.collect_data(point[0], point[1])

        win.flip()
        core.wait(0.5)

    calibration_result = calibration.compute_and_apply()
    print(f"Compute and apply returned {calibration_result.status} and collected {len(calibration_result.calibration_points)} points.")

    calibration.leave_calibration_mode()
    print("Exited calibration mode.")

def run_trial(trial):
    with EyeTrackerManager() as et:
        calibration_text = visual.TextStim(win, text="A calibração vai começar.\nPor favor, olhe para os pontos que aparecerão na tela até que desapareçam.", pos=(0, 0), color='black', height=30)
        calibration_text.draw()
        win.flip()
        core.wait(3)

        calibrate_eyetracker(et.tracker)

        word_stim = visual.TextStim(win, text=trial['word'], pos=(0, 450), color='black', height=50)
        word_stim.draw()
        win.flip()
        core.wait(1)  

        response = None
        clock_tracker = core.Clock()
        gazes_draw = []
        data_buffer = []

        fixation_time = core.Clock()
        tolerance_time = core.Clock()

        draw_gaze = False  

        while True:
            x, y = et.latest_gaze
            keys_pressed = event.getKeys()

            if 'g' in keys_pressed:
                draw_gaze = not draw_gaze  

            if x is not None and y is not None:
                data_buffer.append([x, y])
                print(x, y)
                if draw_gaze:
                    actual_gaze = visual.ImageStim(win, image='EXP/Stimuli/circle.png', size=(80, 80), pos=(x, y))
                    gazes_draw.append(actual_gaze)
                    actual_gaze.draw()

                # Verificar se o gaze está dentro da área alvo
                target_area = keys[-1][1]  # Posição do 'BOTAO_ACABAR'
                if target_area[0] - 60 <= x <= target_area[0] + 60 and target_area[1] - 60 <= y <= target_area[1] + 60:
                    tolerance_time.reset()
                elif tolerance_time.getTime() > DWELL_TOLERANCE:
                    fixation_time.reset()

                if fixation_time.getTime() > DWELL_TIME:
                    print('Olhou por um segundo')
                    break 

            # Desenhar teclas
            for rect, textin in zip(key_rectangles, key_labels):
                rect.draw()
                textin.draw()

            # Desenhar retângulo de progresso do dwell time
            dwell_progress = fixation_time.getTime() / DWELL_TIME
            if dwell_progress > 1.0:
                dwell_progress = 1.0
            dwell_rect_width = key_width * dwell_progress
            dwell_rect = visual.Rect(win, width=dwell_rect_width, height=key_height, pos=(target_area[0] - (key_width - dwell_rect_width) / 2, target_area[1]), lineColor='black', fillColor='blue')
            dwell_rect.draw()

            win.flip()

        if data_buffer:
            trials.addData('response', data_buffer)

# Executa todos os trials
for trial in trials:
    run_trial(trial)
    this_exp.nextEntry()

# Mensagem final
end_stim = visual.TextStim(win, text="Experimento finalizado! Obrigado!", pos=(0, 0), color='black', height=50)
end_stim.draw()
win.flip()
core.wait(3)

# Fechar a janela
win.close()
core.quit()
