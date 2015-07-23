"""
This is a standard logging script designed to provide basic feedback as
to the current operation of the CloudStation application.
"""

import logging
import os


location_of_main_gui_script = os.getcwd()

# The log is positioned adjacent to the main GUI script.
logging.basicConfig(filename='Resources//' + 'CloudStation Parser Log.txt',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


def add_information_message_to_log(message):
    """ This function adds standard information messages to the log.
    """
    logging.info(message)


def add_warning_message_to_log(message):
    """ This function adds warning messages to the log.
    """
    logging.warning(message)


def add_critical_message_to_log(message):
    """ This function adds critical messages to the log.
    """
    logging.critical(message)