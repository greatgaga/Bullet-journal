from funcs import *
from pathlib import Path
import json
from config import *
import datetime
from check_date import run_check_date

if __name__ == '__main__':
    file = open(WELCOME_TEXT_PATH, 'r')
    print(file.read())
    file.close()

    # Configuring tasks.json for future
    # This is used for debuging

    """
    tasks_data = {}

    current_date = datetime.date.today()

    for i in range(30):
        next_date = (current_date + datetime.timedelta(days=i)).strftime("%d-%m-%Y")

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
    
    # Checking if everything in config.json is correct

    with JSON_TASKS_PATH.open('r') as tasks:
        tasks_data = json.load(tasks)

    max_val = -1
    for month in tasks_data.keys():
        for day, value in tasks_data[month].items():
            max_val = max(int(day), max_val)

    if max_val != -1:
        max_val += 1
    else:
        max_val = 0

    with JSON_REPETITIVE_TASKS_PATH.open('r') as rep_tasks:
        rep_tasks_data = json.load(rep_tasks)

    max_val_rep = len(list(rep_tasks_data.keys()))

    with JSONS_CONFIG_PATH.open('r') as config:
        config_data = json.load(config)

    config_data["TASK_NUM"] = max_val
    config_data["REPETITIVE_TASK_NUM"] = max_val_rep

    # Making backup in case something goes wrong while writing to original config file
    temp_path = JSONS_CONFIG_PATH.with_suffix('.tmp')

    try:
        with temp_path.open('w') as temp_file:
            json.dump(config_data, temp_file, indent=4)
            temp_file.close()
    except Exception as e:
        print(f"An error occurred while writing to the temporary file: {e}")
        exit(1)

    # Replace the original file with the temporary file
    try:
        temp_path.replace(JSONS_CONFIG_PATH)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if temp_path.exists():
            temp_path.unlink()

    run_check_date()

    # Client should connect than after that client gets to leading logic

    command = ''

    try:
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

            with JSON_TASKS_PATH.open('r') as tasks:
                tasks_data = json.load(tasks)
                tasks.close()

            # Fixing indexes
            tasks_data = fix_indexes(tasks_data)

            # Create a temporary file to write the updated data
            temp_path = JSON_TASKS_PATH.with_suffix('.tmp')

            try:
                with temp_path.open('w') as temp_file:
                    json.dump(tasks_data, temp_file, indent=4)
                    temp_file.close()
            except Exception as e:
                print(f"An error occurred while writing to the temporary file: {e}")
                exit(1)

            # Replace the original file with the temporary file
            try:
                temp_path.replace(JSON_TASKS_PATH)
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                if temp_path.exists():
                    temp_path.unlink()
    except KeyboardInterrupt:
        print("\nLeaving...")
        exit