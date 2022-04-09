import logging
import teleinterface
from settings import DEBUG, PROJECT_STRUCTURE
import promise_structure

if __name__ == "__main__":

    promise_structure.promise_structure(PROJECT_STRUCTURE)

    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
        try:
            teleinterface.run()
        except Exception as e:
            logging.getLogger(__name__).error(e)
    else:
        logging.basicConfig(level=logging.INFO)
        teleinterface.run()
