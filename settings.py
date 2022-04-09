import os
import json

DEBUG = os.getenv('DEBUG_MODE', True)

with open("structure.json", 'r') as structure_file:
    PROJECT_STRUCTURE = json.load(structure_file) or {}


