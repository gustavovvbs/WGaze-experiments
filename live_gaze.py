import os
import glob
from re import L
import pandas as pd
import math
from collections import namedtuple
import time
# Import some libraries from PsychoPy
from psychopy import core, event, visual, prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound

import tobii_research as tr


EyeData = namedtuple('EyeData', 'x, y, pupil_diameter, validity')
GazeData = namedtuple('GazeData', 'tstamp, left, right, trigger')


def get_best_not_nan(left_value, right_value):
    value = None
    if not math.isnan(left_value) and not math.isnan(right_value):
        value = (left_value + right_value) / 2
    elif not math.isnan(left_value):
        value = left_value
    elif not math.isnan(right_value):
        value = right_value
    return value


#%% Functions

class EyeTrackerManager:
    def __init__(self):
        self.trigger = ''
        # Create an empty list we will append our data to
        self.gaze_data_buffer = []
        self.winsize = (2048, 1152)
        self._latest_gaze = None, None

        # Find all connected eye trackers
        found_eyetrackers = tr.find_all_eyetrackers()
        # We will just use the first one
        self.tracker = found_eyetrackers[0]

    def __enter__(self):
        #Start recording
        self.tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback) # unsubscribe eyetracking
    
    def wait_for_data(self):
        while not self.gaze_data_buffer:
            pass

    # This will be called every time there is new gaze data
    def gaze_data_callback(self, gaze_data):
        # Extract the data we are interested in
        t  = gaze_data.system_time_stamp / 1000.0
        lx = ((gaze_data.left_eye.gaze_point.position_on_display_area[0])*self.winsize[0]) - (self.winsize[0]/2 +0)
        ly = self.winsize[1]/2 - (gaze_data.left_eye.gaze_point.position_on_display_area[1])*self.winsize[1] 
        lp = gaze_data.left_eye.pupil.diameter
        lv = gaze_data.left_eye.gaze_point.validity
        rx = (gaze_data.right_eye.gaze_point.position_on_display_area[0])*self.winsize[0]- (self.winsize[0]/2 +0)
        ry = self.winsize[1]/2 - (gaze_data.right_eye.gaze_point.position_on_display_area[1]*self.winsize[1])
        rp = gaze_data.right_eye.pupil.diameter
        rv = gaze_data.right_eye.gaze_point.validity
            
        # Add gaze data to the buffer 
        self.gaze_data_buffer.append(GazeData(t, EyeData(lx,ly,lp,lv), EyeData(rx,ry,rp,rv), self.trigger))

   
    @property
    def latest_gaze(self):
        if self.gaze_data_buffer:
            for entry in reversed(self.gaze_data_buffer):
                left = entry.left
                right = entry.right
                x = get_best_not_nan(left.x, right.x)
                y = get_best_not_nan(left.y, right.y)
                if x is not None and y is not None:
                    self._latest_gaze = (x, y)
                    break
        return self._latest_gaze
        
  
#%% Load and prepare stimuli
if __name__ == '__main__':
    with EyeTrackerManager() as et_manager:
        win = visual.Window(size = et_manager.winsize, fullscr=True, units='norm')

        gaze = visual.ImageStim(win, image = '/Users/saladeux/Documents/WGaze-experiments/EXP/Stimuli/circle.png', size = (0.1, 0.1))
        fixation = visual.ImageStim(win, image = '/Users/saladeux/Documents/WGaze-experiments/EXP/Stimuli/fixation.png', size = (0.08, 0.08))

        #%% Record the data

        # ### Present the fixation
        win.flip() # we flip to clean the window

        et_manager.wait_for_data()

        clock = core.Clock()
        et_manager.trigger = 'Fixation'
        gazes_draw = []
        while clock.getTime() < 30:
            x, y = et_manager.latest_gaze
            print(x, y)
            if x is not None and y is not None:
                gazes_draw.append(visual.ImageStim(win, image = '/Users/saladeux/Documents/WGaze-experiments/EXP/Stimuli/circle.png', size = (0.1, 0.1), pos = (x, y)))
                
                for i in gazes_draw:
                    i.draw()
                    print(i.pos)
                    # if len(gazes_draw)>200:
                    #     for _ in range(150):
                    #         del gazes_draw[0]
                    #maybe delete the last ones after some treshlhold lenght of the list 
                    #or attribute a timestamp for each of them and after some time has passed after the beginnign of clock it erase the last ones
                # gaze.setPos((x, y))
                # gaze.draw()
            
            fixation.draw()
            win.flip()

            ### Check for closing experiment
            keys = event.getKeys() # collect list of pressed keys
            if 'escape' in keys:
                break

            
        win.close() # close window
        core.quit() # stop study






