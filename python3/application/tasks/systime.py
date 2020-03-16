import logging
import time
from datetime import datetime
from shared import dbase
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'tasks'
logger = logging.getLogger(logfile)


def down():
    """
    Determines JanusESS down time

    :return time_down: int
    """
    # Get time document from CouchDB config database
    data_cdb_out, stat_cdb, code_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='time',
        logfile=logfile
    )
    time_down = 0

    if not stat_cdb:
        # The following condition checks that system time is valid
        if float(time.time()) > float(data_cdb_out['time']):

            # Compute JanusESS down time
            time_down = round(
                (int(float(time.time())) - int(float(data_cdb_out['time']))) / 60,
                0
            )
            log = 'JanusESS downtime was {0} minutes'.format(time_down)
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'INFO',
                log
            ])

    else:
        log = 'Could not determine JanusESS down time due to CouchDB document retrieval error.'
        logger.warning(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'WARNING',
            log
        ])

    return time_down


def store():
    """
    Stores core time in file

    :return stat_time: STAT_LVL['op'] or STAT_LVL['op_err']
    :return stat_cdb: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_time = STAT_LVL['op']

    # Update time document in CouchDB config database
    data_cdb_out, stat_cdb, code_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='time',
        data_cdb_in={'time': str(time.time())},
        logfile=logfile
    )

    if stat_cdb:
        log = 'Could not save time due to CouchDB document update error.'
        logger.warning(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'WARNING',
            log
        ])
        MPQ_STAT.put_nowait([
            'base',
            [
                'couchdb',
                STAT_LVL['op_err']
            ]
        ])

    log = 'Time storage complete.'
    logger.info(log)
    MPQ_ACT.put_nowait([
        datetime.now().isoformat(' '),
        'INFO',
        log
    ])

    if not stat_time:
        MPQ_STAT.put_nowait([
            'base',
            [
                'tasks',
                stat_time
            ]
        ])
