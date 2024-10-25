import requests 
import threading 
import queue 
import time 


task_queue = queue.Queue()

def create_proccess_requests(data_buffer, trial):
    def proccess_requests():
        while True:
            task_data = task_queue.get()

            if task_data is None:
                break 

            requests.post('https://sldhzrbw-8000.brs.devtunnels.ms/trial', 
                            json={"data": data_buffer, 
                            "name": "gustavo_teste1", 
                            "age":18, 
                            "word": trial["word"]})

    return

            


            
