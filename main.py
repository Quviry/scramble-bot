import logging
import pathlib

from controls import teleinterface
from controls.settings import DEBUG, PROJECT_STRUCTURE
from engine.promise_structure import promise_structure

if __name__ == "__main__":

    promise_structure(PROJECT_STRUCTURE)
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    teleinterface.run()
