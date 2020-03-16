import logging
import time
from datetime import datetime
from shared.globals import MPQ_ACT, MPQ_STAT

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'tasks'
logger = logging.getLogger(logfile)


def clear():
    """
    Produces timed status reports
    """
    # Clear queues at most every 24 hours to prevent filling up.
    # There is no better way to clear a multiprocessing queue other than run a loop.
    log = 'Attempting to clear activity and status queues.'
    logger.debug(log)
    MPQ_ACT.put_nowait([
        datetime.now().isoformat(' '),
        'DEBUG',
        log
    ])

    while not MPQ_STAT.empty():
        MPQ_STAT.get()
        time.sleep(0.001)

    while not MPQ_ACT.empty():
        MPQ_ACT.get()
        time.sleep(0.001)

    log = 'Activity and status queues cleared.'
    logger.info(log)
    MPQ_ACT.put_nowait([
        datetime.now().isoformat(' '),
        'INFO',
        log
    ])
