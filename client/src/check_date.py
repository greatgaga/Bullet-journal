# This should check if date changed, and if it changed then it should change date in config.json and also it should adjust repetitive tasks counter for each repetitive task

import datetime
from config import JSON_TASKS_PATH, JSON_REPETITIVE_TASKS_PATH, JSONS_CONFIG_PATH
import json
import time 
from funcs import *

def run_check_date():
    with JSONS_CONFIG_PATH.open("r") as config:
        config_data = json.load(config)

    prev_date = config_data["LAST_DATE"]

    current_time = datetime.date.today().strftime("%d-%m-%Y")
        
    if prev_date != current_time:
        current_time = datetime.date.today().day

        # Adjust tasks.json

        with JSON_TASKS_PATH.open("r") as tasks:
            tasks_data = json.load(tasks)

        with JSON_REPETITIVE_TASKS_PATH.open("r") as rep_tasks:
            rep_tasks_data = json.load(rep_tasks)

        # Removing all the tasks that were last day
        task_num = get_task_num()

        set_task_num(task_num - len(tasks_data[list(tasks_data.keys())[0]]))

        tasks_data.pop(list(tasks_data.keys())[0])

        tasks_data[(datetime.date.today() + datetime.timedelta(days=30)).strftime("%d-%m-%Y")] = {}

        for key, value in rep_tasks_data.items():
            if 30 % value["cycle"] == 0:
                task_num = get_task_num()

                tasks_data[(datetime.date.today() + datetime.timedelta(days=30)).strftime("%d-%m-%Y")][task_num] = {"text": value["text"], "status": "incomplete"}

                set_task_num(task_num + 1)

        # Fixing indexes of tasks_data
        tasks_data = fix_indexes(tasks_data)

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