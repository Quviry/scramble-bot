import logging
import teleinterface
from importlib import reload
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    teleinterface.run()
