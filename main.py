from psychopy import core, visual 

win = visual.Window(fullscr=True)

fixation = visual.ImageStim(win, image = '/Users/saladeux/Documents/WGaze-experiments/EXP/Stimuli/fixation.png')

fixation.draw()
win.flip()
core.wait(3)