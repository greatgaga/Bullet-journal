from pathlib import Path
import json
import datetime
import sys

"""

# loading configuration from JSON file

#BASE_DIR = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))

BASE_DIR = Path(__file__).resolve().parent.parent 
CONFIG_FILE = BASE_DIR / "data" / "config.json"

with CONFIG_FILE.open("r") as f:
    config = json.load(f)


PROMPT_TEXTS_PATH = Path(config["PROMPT_TEXTS_PATH"])
WELCOME_TEXT_PATH = Path(config["WELCOME_TEXT_PATH"])
HELP_TEXT_PATH = Path(config["HELP_TEXT_PATH"])
JSONS_PATH = Path(config["JSONS_PATH"])
JSONS_CONFIG_PATH = Path(config["JSONS_CONFIG_PATH"])
JSON_TASKS_PATH = Path(config["JSON_TASKS_PATH"])
JSON_REPETITIVE_TASKS_PATH = Path(config["JSON_REPETITIVE_TASKS_PATH"])


PROMPT_TEXTS_PATH = (BASE_DIR / config["PROMPT_TEXTS_PATH"]).resolve()
WELCOME_TEXT_PATH = (BASE_DIR / config["WELCOME_TEXT_PATH"]).resolve()
HELP_TEXT_PATH = (BASE_DIR / config["HELP_TEXT_PATH"]).resolve()
JSONS_PATH = (BASE_DIR / config["JSONS_PATH"]).resolve()
JSONS_CONFIG_PATH = (BASE_DIR / config["JSONS_CONFIG_PATH"]).resolve()
JSON_TASKS_PATH = (BASE_DIR / config["JSON_TASKS_PATH"]).resolve()
JSON_REPETITIVE_TASKS_PATH = (BASE_DIR / config["JSON_REPETITIVE_TASKS_PATH"]).resolve()

# Checking if number of tasks changed from last login

TASK_NUM = config["TASK_NUM"]

with JSONS_CONFIG_PATH.open('r') as config_file:
    config_data = json.load(config_file)

config_data["TASK_NUM"] = 0

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

# Fixing date from last login

with JSONS_CONFIG_PATH.open('r') as tasks:
    date_data = json.load(tasks)
    tasks.close()

date_data["LAST_DATE"] = datetime.date.today().strftime("%d-%m-%Y")

with JSONS_CONFIG_PATH.open('w') as tasks:
    json.dump(date_data, tasks, indent=4)
    tasks.close()

LAST_DATE = date_data["LAST_DATE"]
"""

from pathlib import Path
import json
import datetime
import sys

if getattr(sys, 'frozen', False):
    # Running as .exe → use folder where .exe is located
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    # Running as .py → go up from src/ to client/
    BASE_DIR = Path(__file__).resolve().parent.parent

# Load configuration file
CONFIG_FILE = BASE_DIR / "data" / "config.json"
with CONFIG_FILE.open("r") as f:
    config = json.load(f)

# Resolve all paths from config.json relative to BASE_DIR
PROMPT_TEXTS_PATH = (BASE_DIR / config["PROMPT_TEXTS_PATH"]).resolve()
WELCOME_TEXT_PATH = (BASE_DIR / config["WELCOME_TEXT_PATH"]).resolve()
HELP_TEXT_PATH = (BASE_DIR / config["HELP_TEXT_PATH"]).resolve()
JSONS_PATH = (BASE_DIR / config["JSONS_PATH"]).resolve()
JSONS_CONFIG_PATH = (BASE_DIR / config["JSONS_CONFIG_PATH"]).resolve()
JSON_TASKS_PATH = (BASE_DIR / config["JSON_TASKS_PATH"]).resolve()
JSON_REPETITIVE_TASKS_PATH = (BASE_DIR / config["JSON_REPETITIVE_TASKS_PATH"]).resolve()

# Update task count
TASK_NUM = config["TASK_NUM"]
with JSONS_CONFIG_PATH.open('r') as config_file:
    config_data = json.load(config_file)
config_data["TASK_NUM"] = 0
with JSONS_CONFIG_PATH.open('w') as config_file:
    json.dump(config_data, config_file, indent=4)

# Update repetitive task count
REPETITIVE_TASK_NUM = config["REPETITIVE_TASK_NUM"]
with JSON_REPETITIVE_TASKS_PATH.open('r') as tasks:
    tasks_data = json.load(tasks)
task_num_actual = len(tasks_data)

if REPETITIVE_TASK_NUM != task_num_actual:
    with JSONS_CONFIG_PATH.open('r') as config_file:
        config_data = json.load(config_file)
    config_data["REPETITIVE_TASK_NUM"] = task_num_actual
    with JSONS_CONFIG_PATH.open('w') as config_file:
        json.dump(config_data, config_file, indent=4)

# Update last login date
"""
date_data["LAST_DATE"] = datetime.date.today().strftime("%d-%m-%Y")
with JSONS_CONFIG_PATH.open('w') as tasks:
    json.dump(date_data, tasks, indent=4)
"""

with JSONS_CONFIG_PATH.open('r') as tasks:
    date_data = json.load(tasks)

LAST_DATE = date_data["LAST_DATE"]