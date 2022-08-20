import os
import json
import pathlib
import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=0)

DEBUG = os.getenv('DEBUG_MODE', True)

BASE_DIR = pathlib.Path(__file__).parent.parent

STRUCTURE_PATH = 'structure.json'

with open(BASE_DIR / STRUCTURE_PATH, 'r') as structure_file:
    PROJECT_STRUCTURE = json.load(structure_file) or {}

ACTIVE_TELEINTRFACE_MODULES = [
    'scramble_generator',
]

DATA_BASE = BASE_DIR / 'my-test.db'
