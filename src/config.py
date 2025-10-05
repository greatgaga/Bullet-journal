from pathlib import Path
from funcs import *
import json

# loading configuration from JSON file
CONFIG_FILE = Path(__file__).parent.parent / "data/config.json"

with CONFIG_FILE.open("r") as f:
    config = json.load(f)

PROMPT_TEXTS_PATH = Path(config["PROMPT_TEXTS_PATH"])
WELCOME_TEXT_PATH = Path(config["WELCOME_TEXT_PATH"])
JSONS_PATH = Path(config["JSONS_PATH"])
JSONS_CONFIG_PATH = Path(config["JSONS_CONFIG_PATH"])
JSON_TASKS_PATH = Path(config["JSON_TASKS_PATH"])
JSON_REPETITIVE_TASKS_PATH = Path(config["JSON_REPETITIVE_TASKS_PATH"])

# Checking if number of tasks changed from last login

TASK_NUM = config["TASK_NUM"]

with JSON_TASKS_PATH.open('r') as tasks:
    tasks_data = json.load(tasks)
    tasks.close()

task_num_actuall = len(tasks_data)

if TASK_NUM != task_num_actuall:
    TASK_NUM = task_num_actuall

    with JSONS_CONFIG_PATH.open('r') as config_file:
        config_data = json.load(config_file)
    
    config_data["TASK_NUM"] = task_num_actuall

    with JSONS_CONFIG_PATH.open('w') as config_file:
        json.dump(config_data, config_file, indent=4)

# Checking if number of repetitive tasks have changed from last login

REPETITIVE_TASK_NUM = config["REPETITIVE_TASK_NUM"]

with JSON_REPETITIVE_TASKS_PATH.open('r') as tasks:
    tasks_data = json.load(tasks)
    tasks.close()

task_num_actuall = len(tasks_data)

if REPETITIVE_TASK_NUM != task_num_actuall:
    REPETITIVE_TASK_NUM = task_num_actuall

    with JSONS_CONFIG_PATH.open('r') as config_file:
        config_data = json.load(config_file)
    
    config_data["REPETITIVE_TASK_NUM"] = task_num_actuall

    with JSONS_CONFIG_PATH.open('w') as config_file:
        json.dump(config_data, config_file, indent=4)