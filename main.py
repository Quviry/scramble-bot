import logging
import teleinterface
import settings
    
if __name__ == "__main__":
    if settings.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
        try:
            teleinterface.run()
        except Exception as e:
            logging.getLogger(__name__).error(e)
    else:
        logging.basicConfig(level=logging.INFO)
        teleinterface.run()
