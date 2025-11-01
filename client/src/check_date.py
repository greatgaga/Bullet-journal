# This should check if date changed, and if it changed then it should change date in config.json and also it should adjust repetitive tasks counter for each repetitive task

import datetime
from config import JSON_TASKS_PATH, JSON_REPETITIVE_TASKS_PATH, JSONS_CONFIG_PATH
import json
import time 
from funcs import *

def run_check_date():
    with JSONS_CONFIG_PATH.open("r") as config:
        config_data = json.load(config)

    fmt = "%d-%m-%Y"

    prev_date = datetime.datetime.strptime(config_data["LAST_DATE"], fmt)

    current_time = datetime.date.today().strftime("%d-%m-%Y")
        
    if prev_date != current_time:
        current_time = datetime.date.today()

        # Adjust tasks.json

        with JSON_TASKS_PATH.open("r") as tasks:
            tasks_data = json.load(tasks)

        with JSON_REPETITIVE_TASKS_PATH.open("r") as rep_tasks:
            rep_tasks_data = json.load(rep_tasks)

        # Adding needed number of days to tasks_data
        last_date = list(tasks_data.items())

        last_date = datetime.datetime.strptime(last_date[-1][0], fmt)

        target_date = (current_time + datetime.timedelta(days=30))

        delta = target_date - last_date.date()

        #print(delta)

        for i in range(1, delta.days + 1):
            date = (last_date + datetime.timedelta(days=i)).date().strftime("%d-%m-%Y")

            print(date)

            tasks_data[date] = {}

        #print(tasks_data)

        # Adding repetitive tasks to tasks_datas new days
        for key, value in tasks_data.items():
            if datetime.datetime.strptime(key, "%d-%m-%Y").date() >= last_date.date():
                for key_rep, value_rep in rep_tasks_data.items():
                    start_date = value_rep["start_date"]
                    cycle = value_rep["cycle"]

                    if ((datetime.datetime.strptime(key, "%d-%m-%Y").date() - datetime.datetime.strptime(start_date, "%d-%m-%Y").date()).days > 0):
                        if (datetime.datetime.strptime(key, "%d-%m-%Y").date() - datetime.datetime.strptime(start_date, "%d-%m-%Y").date()).days % cycle == 0:
                            task_num = get_task_num()
                            tasks_data[key][task_num]["text"] = value["text"]
                            tasks_data[key][task_num]["status"] = "incomplete"

                            set_task_num(task_num + 1)

        # Removing old dates

        # Create a temporary file to write the updated data
        temp_path = JSON_TASKS_PATH.with_suffix('.tmp')

        try:
            with temp_path.open('w') as temp_file:
                json.dump(tasks_data, temp_file, indent=4)
                temp_file.close()
        except Exception as e:
            print(f"An error occurred while writing to the temporary file: {e}")

        # Replace the original file with the temporary file
        try:
            temp_path.replace(JSON_TASKS_PATH)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if temp_path.exists():
                temp_path.unlink()

        # Adjusting date in config.json

        with JSONS_CONFIG_PATH.open("r") as config:
            config_data = json.load(config)

        config_data["LAST_DATE"] = datetime.date.today().strftime("%d-%m-%Y")

        # Create a temporary file to write the updated data
        temp_path = JSONS_CONFIG_PATH.with_suffix('.tmp')

        try:
            with temp_path.open('w') as temp_file:
                json.dump(config_data, temp_file, indent=4)
                temp_file.close()
        except Exception as e:
            print(f"An error occurred while writing to the temporary file: {e}")

        # Replace the original file with the temporary file
        try:
            temp_path.replace(JSONS_CONFIG_PATH)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if temp_path.exists():
                temp_path.unlink()

    prev_date = current_time