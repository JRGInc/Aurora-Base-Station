import logging
from datetime import datetime
from shared.messaging.smtp import send_mail
from shared.globals import MPQ_ACT, MPQ_STAT, STAT_LVL

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'tasks'
logger = logging.getLogger(logfile)


def update(
    interval: int
):
    """
    Produces timed status reports

    :param interval: int
    """
    log = 'Conducting {0}-hour system status check.'.format(interval)
    logger.info(log)
    MPQ_ACT.put_nowait([
        datetime.now().isoformat(' '),
        'INFO',
        log
    ])

    # Only issue messaging if recent network check shows it is up
    send_mail(
        msg_type='status_dispatch',
        args=[],
    )

    log = '{0}-hour status check completed.'.format(interval)
    logger.info(log)
    MPQ_ACT.put_nowait([
        datetime.now().isoformat(' '),
        'INFO',
        log
    ])
    MPQ_STAT.put_nowait([
        'base',
        [
            'tasks',
            STAT_LVL['op']
        ]
    ])
