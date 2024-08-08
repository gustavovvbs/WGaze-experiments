import tobii_research as tr
import time 


eyetrackers = tr.find_all_eyetrackers()
eyetracker = eyetrackers[0]
print(eyetracker.model)

def gaze_data_callback(gaze_data):
    print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(gaze_left_eye = gaze_data['left_gaze_point_on_display_area'], gaze_right_eye = gaze_data['right_gaze_point_on_display_area']))

eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary = True)

time.sleep(20)

eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
