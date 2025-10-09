import json
from config import *
from datetime import *

# Helper funcs

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

def set_repetitive_task(new_num):
    with JSONS_CONFIG_PATH.open('r') as config_file:
        config_data = json.load(config_file)
    
    config_data["REPETITIVE_TASK_NUM"] = new_num

    with JSONS_CONFIG_PATH.open('w') as config_file:
        json.dump(config_data, config_file, indent=4)

def get_repetitive_task():
    with JSONS_CONFIG_PATH.open('r') as f:
        config = json.load(f)
    return config.get("REPETITIVE_TASK_NUM", 0)

def configure_tasks(cycle, text):
    with JSON_TASKS_PATH.open('r') as tasks:
        tasks_data = json.load(tasks)
        tasks.close()

    counter = 0

    for key in tasks_data:
        if counter % cycle == 0 :
            counter = 0

            task_num = get_task_num()

            tasks_data[key][task_num] = {}

            tasks_data[key][task_num]['text'] = text
            tasks_data[key][task_num]['status'] = 'incomplete'

            set_task_num(task_num + 1)

        counter += 1

    with JSON_TASKS_PATH.open('w') as tasks:
        json.dump(tasks_data, tasks, indent=4)
        tasks.close()

def fix_tasks(index):
    # Getting detials about this task for begginng
    with JSON_TASKS_PATH.open('r') as tasks:
        tasks_data = json.load(tasks)

    with JSON_REPETITIVE_TASKS_PATH.open('r') as tasks:
        repetitive_tasks_data = json.load(tasks)

    details = repetitive_tasks_data[str(index)]

    counter = 0

    # Remove tasks from tasks_data that match the repetitive task's text
    for date_key in tasks_data:
        remove_indices = []
        for idx, task in tasks_data[date_key].items():
            if task.get('text') == details['text']:
                remove_indices.append(idx)
        for idx in remove_indices:
            tasks_data[date_key].pop(idx)
            set_task_num(get_task_num() - 1)

    # Fixing indexing in dict

    copy = {}

    for date_key in tasks_data:
        copy[date_key] = {}
        for key in sorted(tasks_data[date_key].keys(), key=lambda x: int(x)):
            copy[date_key][counter] = tasks_data[date_key][key]
            counter += 1

    tasks_data = copy

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

    print('Repetitive task removed successfully!')

# Features

def add_task():
    try:
        print("Text of task you want to add: ", end='')

        task_text = input()

        print("Date you to which you want to add that task to (eg 'today', '05-10-2025', '23-10-2026', ...): ", end='')

        date_ = input()
    except KeyboardInterrupt:
        print()
        return

    with JSON_TASKS_PATH.open('r') as tasks:
        tasks_data = json.load(tasks)
        tasks.close()

    if date_ == 'today':
        date_ = date.today().strftime("%d-%m-%Y")

    tasks_data[date_][get_task_num()] = {'text': task_text, 'status': 'incomplete'}

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

    for key in tasks_data:
        if str(index) in tasks_data[key]:
            tasks_data[key].pop(str(index), None)

            real_key = key

    # Decrementing task number
    new_task_num = (get_task_num() - 1)
    set_task_num(new_task_num)

    # Fixing indexes of all tasks

    counter = 0

    flag = False

    copy = {}

    for key in tasks_data[real_key]:
        delta = tasks_data[real_key][key]
        copy[counter] = delta

        counter += 1

    tasks_data[real_key] = copy

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

    date = datetime.today().strftime("%d-%m-%Y")

    with JSON_TASKS_PATH.open('r') as tasks:
        tasks_data = json.load(tasks)

    for key in tasks_data[datetime.today().strftime("%d-%m-%Y")]:
        output = '| '

        # Index of task
        if int(key) <= 9:
            output += '0'

        output += key + ': '

        # Adding actuall text

        text = tasks_data[datetime.today().strftime("%d-%m-%Y")][key]['text']

        while len(text) > 41:
            text = text.lstrip()

            if tasks_data[datetime.today().strftime("%d-%m-%Y")][key]['text'] != text:
                output += '|     '

            output += text[0:41]
            output += ' |\n'

            text = text[41:]

        if tasks_data[datetime.today().strftime("%d-%m-%Y")][key]['text'] != text:
            output += '|     '

        text = text.lstrip()

        output += text

        if tasks_data[datetime.today().strftime("%d-%m-%Y")][key]['text'] != text:
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

    if num_days > 99:
        print("Cycle of repetitive tasks can be 99 at max")
        return 

    # Changing repetitive tasks data

    with JSON_REPETITIVE_TASKS_PATH.open('r') as tasks:
        repetitive_tasks_data = json.load(tasks)

    repetitive_tasks_num = get_repetitive_task()

    repetitive_tasks_data[repetitive_tasks_num] = {"text": text, "cycle": num_days}

    # Create a temporary file to write the updated data
    temp_path = JSON_REPETITIVE_TASKS_PATH.with_suffix('.tmp')

    try:
        with temp_path.open('w') as temp_file:
            json.dump(repetitive_tasks_data, temp_file, indent=4)
            temp_file.close()
    except Exception as e:
        print(f"An error occurred while writing to the temporary file: {e}")
        return

    # Replace the original file with the temporary file
    try:
        temp_path.replace(JSON_REPETITIVE_TASKS_PATH)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if temp_path.exists():
            temp_path.unlink()

    set_repetitive_task(repetitive_tasks_num + 1)

    print('Repetitive task added successfully!')

    configure_tasks(num_days, text)

    print('Succesfuly configured repetitive task!')

def display_schedule_for_next_days():
    try:
        print("Number of days to be displayed: ", end='')

        num_days = int(input())
    except KeyboardInterrupt:
        print()
        return

    if num_days > 30:
        print("Can only display next 30 days as max")
        return

    for i in range(num_days):
        current_date = date.today()
        next_date = current_date + timedelta(days=i)

        print(f'+-({next_date.strftime("%d-%m-%Y")})----------------------------------+')

        with JSON_TASKS_PATH.open('r') as tasks:
            tasks_data = json.load(tasks)

        for key in tasks_data[next_date.strftime("%d-%m-%Y")]:
            output = '| '

            # Index of task
            if int(key) <= 9:
                output += '0'

            output += key + ': '

            # Adding actuall text

            text = tasks_data[next_date.strftime("%d-%m-%Y")][key]['text']

            while len(text) > 41:
                text = text.lstrip()

                if tasks_data[next_date.strftime("%d-%m-%Y")][key]['text'] != text:
                    output += '|     '

                output += text[0:41]
                output += ' |\n'

                text = text[41:]

            if tasks_data[next_date.strftime("%d-%m-%Y")][key]['text'] != text:
                output += '|     '

            text = text.lstrip()

            output += text

            if tasks_data[next_date.strftime("%d-%m-%Y")][key]['text'] != text:
                output += ''

            # 49 chars in total per line

            output += ' ' * (47 - len(text) - 6)

            output += ' |\n'

            output += '+-----------------------------------------------+'

            print(output)

def remove_repetitive_task():
    try:
        print("Index of repetitive task to be removed: ", end='')

        index = int(input())
    except KeyboardInterrupt:
        print()
        return

    with JSON_REPETITIVE_TASKS_PATH.open('r') as tasks:
        tasks_data = json.load(tasks)

    # Changing tasks.json

    fix_tasks(index)

    # Removing

    counter = 0

    for key, value in tasks_data.items():
        if key == str(index):
            details = tasks_data[key]

            tasks_data.pop(key)

            break

    # Rebuild the dictionary with sequential keys after removal
    new_tasks_data = {}
    for idx, (old_key, value) in enumerate(tasks_data.items()):
        new_tasks_data[str(idx)] = value
    tasks_data = new_tasks_data

    # Making backup if dumping fails

    temp_path = JSON_REPETITIVE_TASKS_PATH.with_suffix('.tmp')

    try:
        with temp_path.open('w') as temp_file:
            json.dump(tasks_data, temp_file, indent=4)
            temp_file.close()
    except Exception as e:
        print("An error occurred: ", e)

    # Fixing tasks.json

    try:
        temp_path.replace(JSON_REPETITIVE_TASKS_PATH)
    except Exception as e:
        print("An error occurred: ", e)
    finally:
        if temp_path.exists():
            temp_file.unlink()

    tasks_num = get_repetitive_task()
    set_repetitive_task(tasks_num - 1)

    print("Succesfuly removed task!")

def display_repetitive_tasks():
    with JSON_REPETITIVE_TASKS_PATH.open('r') as tasks:
        tasks_data = json.load(tasks)

    output = ''

    output += '+--(index)--+--(cycle)--+--(text)---------------+\n'

    for key in tasks_data:
        output += '|    '

        if len(key) <= 9:
            output += '0'
            
        output += key

        output += '     |'

        output += '    '

        if tasks_data[key]["cycle"] <= 9:
            output += ' '

        output += str(tasks_data[key]["cycle"])

        output += '     |'

        output += '  '

        text = tasks_data[key]["text"]

        print(text)

        while len(text) > 20:
            output += text[0:20]

            output += ' |\n'

            text = text[21:]

            output += '|           |           |  '

        output += text

        output += ' ' * (20 - len(text))

        output += ' |\n'

        output += '+-----------+-----------+-----------------------+\n'

    print(output)