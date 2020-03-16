import logging
from datetime import datetime
from shared import dbase
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'tasks'
logger = logging.getLogger(logfile)


def compact():
    """
    Calls compact() for multiple CouchDB databases

    :return stat_cdb: STAT_LVL['op'] or STAT_LVL['crit']
    """
    logger.debug('Compacting databases.')

    # Get list of databases from CouchDB
    data0_cdb_out, stat_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_dbs',
        logfile=logfile
    )

    if not stat_cdb and data0_cdb_out:

        # Cycle through all CouchDB databases and compact each one
        for cdb_name in range(2, len(data0_cdb_out)):
            data1_cdb_out, stat_cdb, http1_cdb = dbase.cdb_request(
                cdb_cmd='cpt_dbs',
                cdb_name=data0_cdb_out[cdb_name],
                logfile=logfile
            )

            if not stat_cdb:
                log = 'Compact of {0} database completed.'.format(data0_cdb_out[cdb_name])
                logger.debug(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'INFO',
                    log
                ])

            else:
                log = 'Could not compact {0} database due to CouchDB ' +\
                      'compact error.'.format(data0_cdb_out[cdb_name])
                logger.warning(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'WARNING',
                    log
                ])

        log = 'Database compact operations concluded.'
        logger.info(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'INFO',
            log
        ])

    else:
        log = 'Database compact operations could not take place to a CouchDB error.'
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
            stat_cdb
        ]
    ])
    MPQ_STAT.put_nowait([
        'base',
        [
            'tasks',
            stat_cdb
        ]
    ])


def archive(
    cdb_list: list
):
    """
    Calls archive() for critical databases every minute

    :param cdb_list: list

    :return stat_cdb: STAT_LVL['op'] or STAT_LVL['crit']
    """
    logger.debug('Archiving databases.')

    # Cycle through all databases in the list
    for cdb_name in cdb_list:

        # Archive CouchDB database to JSON file
        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='ark_dbs',
            cdb_name=cdb_name,
            logfile=logfile
        )

        if not stat_cdb:
            log = 'Archive of {0} database succeeded.'.format(cdb_name)
            logger.debug(log)

        else:
            log = 'Archive of {0} database failed.'.format(cdb_name)
            logger.warning(log)
            MPQ_STAT.put_nowait([
                'base',
                [
                    'couchdb',
                    STAT_LVL['op_err']
                ]
            ])
            MPQ_STAT.put_nowait([
                'tasks',
                [
                    'couchdb',
                    STAT_LVL['op_err']
                ]
            ])
