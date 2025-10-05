from funcs import *
from pathlib import Path
import json
from config import WELCOME_TEXT_PATH, JSON_TASKS_PATH, TASK_NUM

if __name__ == '__main__':
    file = open(WELCOME_TEXT_PATH, 'r')
    print(file.read())

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