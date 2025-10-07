from funcs import *
from pathlib import Path
import json
from config import WELCOME_TEXT_PATH, JSON_TASKS_PATH, TASK_NUM, LAST_DATE, HELP_TEXT_PATH
from datetime import *

if __name__ == '__main__':
    file = open(WELCOME_TEXT_PATH, 'r')
    print(file.read())
    file.close()

    # Configuring tasks.json for future
    """

    tasks_data = {}

    for i in range(30):
        current_date = date.today()

        next_date = (current_date + timedelta(days=i)).strftime("%d-%m-%Y")

        tasks_data[next_date] = {}

    try:
        with JSON_TASKS_PATH.open('w') as tasks_file:
            json.dump(tasks_data, tasks_file, indent=4)
    except Exception as e:
        print("Error while init, reseting tasks.json")
        with JSON_TASKS_PATH.open('w') as tasks_file:
            json.dump({}, tasks_file, indent=4)

    # Configuring repetitive tasks

    with JSON_REPETITIVE_TASKS_PATH.open('r') as tasks:
        tasks_data = json.load(tasks)

    for key in tasks_data:
        repeat_num = tasks_data[key]['cycle']
        text = tasks_data[key]['text']

        configure_tasks(repeat_num, text)
    """

    # Should start a python script that will check if date changed every 3 hours (start in background, so it runs constantly)

    # Client should connect than after that client gets to leading logic

    command = ''

    while command != "exit":
        print('>> ', end='')

        command = input()

        if command == '1':
            add_task()
        elif command == '2':
            remove_task()
        elif command == '6':
            display_tasks_for_today()
        elif command == '4':
            configure_repetitive_task()
        elif command == '5':
            display_schedule_for_next_days()
        elif command == 'help':
            file = HELP_TEXT_PATH.open('r')
            print(file.read())
        elif command == '7':
            remove_repetitive_task()
        elif command == '8':
            display_repetitive_tasks()