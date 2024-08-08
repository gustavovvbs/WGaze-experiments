
import tobii_research as tr

def execute():
    eyetrackers = tr.find_all_eyetrackers()

    for eyetracker in eyetrackers:
        print("Address: " + eyetracker.address)
        print("Model: " + eyetracker.model)
        print("Name (It's OK if this is empty): " + eyetracker.device_name)
        print("Serial number: " + eyetracker.serial_number)
        return eyetrackers

execute()
