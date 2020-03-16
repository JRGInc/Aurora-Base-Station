import logging
import requests
from datetime import datetime
from shared import dbase
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT, MPQ_NETINT

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'tasks'
logger = logging.getLogger(logfile)


def check():
    """
    Connects to network address

    :return stat_cdb: STAT_LVL['op'] or STAT_LVL['crit']
    :return stat_net: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_net = STAT_LVL['op']

    # Get tasks document from CouchDB config database
    data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='network',
        logfile=logfile
    )

    if not stat_cdb:
        check_int = data_cdb_out['network_interval']

        try:
            # Issue GET request to internet server
            http_resp = requests.get(
                'http://{0}'.format(data_cdb_out['url_server']),
                timeout=data_cdb_out['url_timeout']
            )

            # Check for any HTTP response code, address exists even if returns error.
            if http_resp.status_code:
                check_int = data_cdb_out['interval_good']
                log = 'Network check succeeded.  Next check in {0} minutes'.format(check_int)
                logger.info(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'DEBUG',
                    log
                ])
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'network',
                        STAT_LVL['op']
                    ]
                ])

        except requests.exceptions.ConnectionError:
            check_int = data_cdb_out['interval_bad']
            log = 'URL {0} did not respond on network.'.format(data_cdb_out['url_server'])
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])

            log = 'Next network check accelerated to {0} minutes.'.format(check_int)
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])

            MPQ_STAT.put_nowait([
                'base',
                [
                    'network',
                    STAT_LVL['crit']
                ]
            ])
            stat_net = STAT_LVL['op_err']

        MPQ_STAT.put_nowait([
            'network',
            [
                data_cdb_out['url_server'],
                check_int,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
        ])
        MPQ_NETINT.put_nowait(check_int)

    else:
        log = 'Could not complete network check due to CouchDB document retrieval error.'
        logger.warning(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'WARNING',
            log
        ])
        stat_net = STAT_LVL['op_err']

    if not stat_net:
        MPQ_STAT.put_nowait([
            'base',
            [
                'tasks',
                stat_net
            ]
        ])
