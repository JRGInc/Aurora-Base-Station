import logging
import os

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'aurora'
logger = logging.getLogger(logfile)


def restart():
    """
    POST handler
    """
    logger.info("System shutdown called.")
    os.system("sudo shutdown -r now")


def shutdown():
    """
    POST handler
    """
    logger.info("System shutdown called.")
    os.system("sudo shutdown -h now")
