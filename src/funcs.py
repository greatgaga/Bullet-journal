import json
from config import WELCOME_TEXT_PATH, JSON_TASKS_PATH, JSONS_CONFIG_PATH
from datetime import *

def set_task_num(new_num):
    with JSONS_CONFIG_PATH.open('r') as config_file:
        config_data = json.load(config_file)
    
    config_data["TASK_NUM"] = new_num

    with JSONS_CONFIG_PATH.open('w') as config_file:
        json.dump(config_data, config_file, indent=4)

def get_task_num():
    with JSONS_CONFIG_PATH.open('r') as f:
        config = json.load(f)
    return config.get("TASK_NUM", 0)

def add_task():
    try:
        print("Text of task you want to add: ", end='')

        task_text = input()
    except KeyboardInterrupt:
        print()
        return

    with JSON_TASKS_PATH.open('r') as tasks:
        tasks_data = json.load(tasks)
        tasks.close()

    tasks_data[get_task_num()] = {'text': task_text, 'status': 'incomplete'}

    # Create a temporary file to write the updated data
    temp_path = JSON_TASKS_PATH.with_suffix('.tmp')

    try:
        with temp_path.open('w') as temp_file:
            json.dump(tasks_data, temp_file, indent=4)
            temp_file.close()
    except Exception as e:
        print(f"An error occurred while writing to the temporary file: {e}")
        return

    # Replace the original file with the temporary file
    try:
        temp_path.replace(JSON_TASKS_PATH)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if temp_path.exists():
            temp_path.unlink()

    print('Task added successfully!')

    # Increment the task number for the next task
    new_task_num = (get_task_num() + 1)
    set_task_num(new_task_num)

def remove_task():
    try:
        print("Index of task you want to remove: ", end='')

        index = input()
    except KeyboardInterrupt:
        print()
        return

    # Removing task

    with JSON_TASKS_PATH.open('r') as tasks:
        tasks_data = json.load(tasks)
        tasks.close()

    tasks_data.pop(str(index), None)

    # Decrementing task number
    new_task_num = (get_task_num() - 1)
    set_task_num(new_task_num)

    # Fixing indexes of all tasks

    counter = 0

    flag = False

    copy = {}

    for key in tasks_data:
        delta = tasks_data[key]
        copy[counter] = delta

        counter += 1

    tasks_data = copy

    # Making backup if dumping fails

    temp_path = JSON_TASKS_PATH.with_suffix('.tmp')

    try:
        with temp_path.open('w') as temp_file:
            json.dump(tasks_data, temp_file, indent=4)
            temp_file.close()
    except Exception as e:
        print("An error occurred: ", e)

    # Fixing tasks.json

    try:
        temp_path.replace(JSON_TASKS_PATH)
    except Exception as e:
        print("An error occurred: ", e)
    finally:
        if temp_path.exists():
            temp_file.unlink()

    print("Succesfuly removed task!")

def display_tasks_for_today():
    print(f'+-({datetime.today().strftime("%d-%m-%Y")})----------------------------------+')

    with JSON_TASKS_PATH.open('r') as tasks:
        tasks_data = json.load(tasks)

    for key in tasks_data:
        output = '| '

        # Index of task
        if int(key) < 9:
            output += '0'

        output += key + ': '

        # Adding actuall text

        text = tasks_data[key]['text']

        while len(text) > 41:
            text = text.lstrip()

            if tasks_data[key]['text'] != text:
                output += '|     '

            output += text[0:41]
            output += ' |\n'

            text = text[41:]

        if tasks_data[key]['text'] != text:
            output += '|     '

        text = text.lstrip()

        output += text

        if tasks_data[key]['text'] != text:
            output += ''

        # 49 chars in total per line

        output += ' ' * (47 - len(text) - 6)

        output += ' |\n'

        output += '+-----------------------------------------------+'

        print(output)

def configure_repetitive_task():
    try:
        print("Text of repetitive task you want to configure: ", end='')

        text = input()

        print("Length of cycle for this repetitive task to repeat itself: ", end='')

        num_days = int(input())
    except KeyboardInterrupt:
        print()
        return

    