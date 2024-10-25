import threading
import math
from collections import namedtuple
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

class EyeTrackerManager:
    def __init__(self):
        self.trigger = ''
        self.gaze_data_buffer = []
        self.winsize = (2048, 1152)
        self._latest_gaze = (None, None)
        self.lock = threading.Lock()  # Initialize the lock

        # Find all connected eye trackers
        found_eyetrackers = tr.find_all_eyetrackers()
        self.tracker = found_eyetrackers[0]

    def __enter__(self):
        # Start recording
        self.tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Unsubscribe from gaze data
        self.tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)

    def wait_for_data(self):
        while not self.gaze_data_buffer:
            pass

    def gaze_data_callback(self, gaze_data):
        # Extract the data we are interested in
        t = gaze_data['system_time_stamp'] / 1000.0
        lx = (gaze_data['left_gaze_point_on_display_area'][0]) * self.winsize[0] - (self.winsize[0] / 2)
        ly = self.winsize[1] / 2 - (gaze_data['left_gaze_point_on_display_area'][1]) * self.winsize[1]
        lp = gaze_data['left_pupil_diameter']
        lv = gaze_data['left_gaze_point_validity']
        rx = (gaze_data['right_gaze_point_on_display_area'][0]) * self.winsize[0] - (self.winsize[0] / 2)
        ry = self.winsize[1] / 2 - (gaze_data['right_gaze_point_on_display_area'][1] * self.winsize[1])
        rp = gaze_data['right_pupil_diameter']
        rv = gaze_data['right_gaze_point_validity']

        gaze_entry = GazeData(
            t,
            EyeData(lx, ly, lp, lv),
            EyeData(rx, ry, rp, rv),
            self.trigger
        )

        with self.lock:
            self.gaze_data_buffer.append(gaze_entry)

    @property
    def latest_gaze(self):
        with self.lock:
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
