import logging
from shared import dbase
from shared.globals import MPQ_ACT_CMD, MPQ_STAT, MPQ_CMD0, MPQ_SETUP_LOG_RESET, MPQ_SETUP_LOG_INIT, \
    MPQ_POLL_LOG_DISP, MPQ_POLL_LOG_DATA, MPQ_FLAG_LOG, MPQ_LOG_LVL

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'server'
logger = logging.getLogger(logfile)


def core(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # This variable will get overwritten during success
    data_cdb_out = post_data

    # Update core document in CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='core',
        data_cdb_in={
            'name': post_data['sysname'],
            'customer': post_data['customerid']
        },
        logfile=logfile
    )

    # Get core document from CouchDB config database
    if not stat0_cdb:
        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='core',
            logfile=logfile,
        )
        if stat1_cdb:
            log = 'Could not update web GUI from CouchDB ' + \
                  'due to CouchDB error.'
            logger.warning(log)

        else:
            data_cdb_out = data1_cdb_out

    else:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def temp(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # This variable will get overwritten during success
    data_cdb_out = post_data

    # Convert posted data to usable form
    data_cdb_in = {
        'temperature': post_data['unit']
    }

    # Update logging document in CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='dataunits',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Get logging document from CouchDB config database
    if not stat0_cdb:
        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='dataunits',
            logfile=logfile,
        )

        if stat1_cdb:
            log = 'Could not update web GUI from CouchDB ' + \
                  'due to CouchDB error.'
            logger.warning(log)

        else:
            data_cdb_out = data1_cdb_out

    else:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def press(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # This variable will get overwritten during success
    data_cdb_out = post_data

    # Convert posted data to usable form
    data_cdb_in = {
        'pressure': post_data['unit']
    }

    # Update logging document in CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='dataunits',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Get logging document from CouchDB config database
    if not stat0_cdb:
        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='dataunits',
            logfile=logfile,
        )

        if stat1_cdb:
            log = 'Could not update web GUI from CouchDB ' + \
                  'due to CouchDB error.'
            logger.warning(log)

        else:
            data_cdb_out = data1_cdb_out

    else:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def log(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # Convert posted data to usable form
    data_cdb_in = {
        'activity': post_data['activity'],
        'janusess': post_data['janusess'],
        'command': post_data['command'],
        'conversion': post_data['conversion'],
        'heartbeat': post_data['heartbeat'],
        'interface': post_data['interface'],
        'polling': post_data['polling'],
        'server': post_data['server'],
        'setup': post_data['setup'],
        'tasks': post_data['tasks']
    }

    # Update logging document in CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='log',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Get logging document from CouchDB config database
    if stat0_cdb:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    # Set heartbeat activity logging level
    MPQ_ACT_CMD.put_nowait(['log_level', post_data['activity']])

    logs = [
        'activity',
        'janusess',
        'command',
        'conversion',
        'heartbeat',
        'interface',
        'polling',
        'server',
        'setup',
        'tasks'
    ]

    # Update multiprocess processes via various queues
    for log_file in logs:
        if log_file == 'command':
            MPQ_CMD0.put({
                'command': 'log_level',
                'args': [post_data['command']],
                'data': []
            })
        elif log_file == 'heartbeat':
            MPQ_STAT.put_nowait([
                'log_level',
                post_data['heartbeat']]
            )
        elif log_file == 'polling':
            MPQ_POLL_LOG_DISP.put_nowait([post_data['polling']])
            MPQ_POLL_LOG_DATA.put_nowait([post_data['polling']])
            MPQ_FLAG_LOG.put_nowait([post_data['polling']])

        # Already within server multiprocess, just set level
        elif log_file == 'server':
            if post_data['server'] == 'DEBUG':
                logger.setLevel(logging.DEBUG)
            elif post_data['server'] == 'INFO':
                logger.setLevel(logging.INFO)
            elif post_data['server'] == 'ERROR':
                logger.setLevel(logging.ERROR)
            elif post_data['server'] == 'WARNING':
                logger.setLevel(logging.WARNING)
            elif post_data['server'] == 'CRITICAL':
                logger.setLevel(logging.CRITICAL)

        elif log_file == 'setup':
            MPQ_SETUP_LOG_RESET.put_nowait([post_data['setup']])
            MPQ_SETUP_LOG_INIT.put_nowait([post_data['setup']])

        # All others get reported back to main, trickle to threads via shared memory
        else:
            MPQ_LOG_LVL.put_nowait([
                log_file,
                post_data[log_file]])

    return post_data


def compact(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # This variable will get overwritten during success
    data_cdb_out = post_data

    # Convert posted data to usable form
    data_cdb_in = {
        'dbcompact_firsttime': post_data['dbcompact_firsttime'],
        'dbcompact_interval': int(post_data['dbcompact_interval']),
    }

    # Update tasks document in CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='compact',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Get tasks document from CouchDB config database
    if not stat0_cdb:
        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='compact',
            logfile=logfile,
        )

        if stat1_cdb:
            log = 'Could not update web GUI from CouchDB ' + \
                  'due to CouchDB error.'
            logger.warning(log)

        else:
            data_cdb_out = data1_cdb_out

    else:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def update(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # This variable will get overwritten during success
    data_cdb_out = post_data

    # Convert posted data to usable form
    data_cdb_in = {
        'updateemail_firsttime': post_data['updateemail_firsttime'],
        'updateemail_interval': int(post_data['updateemail_interval']),
    }

    # Update tasks document in CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='update',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Get tasks document from CouchDB config database
    if not stat0_cdb:
        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='update',
            logfile=logfile,
        )

        if stat1_cdb:
            log = 'Could not update web GUI from CouchDB ' + \
                  'due to CouchDB error.'
            logger.warning(log)

        else:
            data_cdb_out = data1_cdb_out

    else:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def cloud(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # This variable will get overwritten during success
    data_cdb_out = post_data

    # Convert posted data to usable form
    data_cdb_in = {
        'url': post_data['url'],
        'enable': post_data['enable']
    }

    # Update cloud document in CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='cloud',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Get cloud document from CouchDB config database
    if not stat0_cdb:
        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='cloud',
            logfile=logfile,
        )

        if stat1_cdb:
            log = 'Could not update web GUI from CouchDB ' + \
                  'due to CouchDB error.'
            logger.warning(log)

        else:
            data_cdb_out = data1_cdb_out

    else:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def network(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # This variable will get overwritten during success
    data_cdb_out = post_data

    # Convert posted data to usable form
    data_cdb_in = {
        'url_server': post_data['url_server'],
        'interval_good': int(post_data['interval_good']),
        'interval_bad': int(post_data['interval_bad']),
        'url_timeout': int(post_data['url_timeout']),
    }

    # Update tasks document in CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='network',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Get tasks document from CouchDB config database
    if not stat0_cdb:
        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='network',
            logfile=logfile,
        )

        if stat1_cdb:
            log = 'Could not update web GUI from CouchDB ' + \
                  'due to CouchDB error.'
            logger.warning(log)

        else:
            data_cdb_out = data1_cdb_out

    else:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def email(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # This variable will get overwritten during success
    data_cdb_out = post_data

    # Convert posted data to usable form
    data_cdb_in = {'smtp_enable': post_data['smtp_enable']}

    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='email',
        logfile=logfile,
    )

    data_cdb_in['smtp_from'] = post_data['smtp_from']
    data_cdb_in['smtp_server'] = post_data['smtp_server']
    data_cdb_in['smtp_port'] = int(post_data['smtp_port'])

    if post_data['smtp_password'] == "":
        data_cdb_in['smtp_password'] = None

    else:
        data_cdb_in['smtp_password'] = post_data['smtp_password']

    data_cdb_in['smtp_timeout'] = int(post_data['smtp_timeout'])

    # Update email document in CouchDB config database
    data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='email',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Get email document from CouchDB config database
    if not stat1_cdb:
        data2_cdb_out, stat2_cdb, http2_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='email',
            logfile=logfile,
        )

        if stat2_cdb:
            log = 'Could not update web GUI from CouchDB ' + \
                  'due to CouchDB error.'
            logger.warning(log)

        else:
            data_cdb_out = data2_cdb_out

    else:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def email_list(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # This variable will get overwritten during success
    data_cdb_out = post_data

    data_cdb_in = {}

    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='email',
        logfile=logfile,
    )

    if not stat0_cdb:
        if post_data['smtp_address'] != '':
            data_cdb_in['smtp_list_{0}'.format(post_data['smtp_list'])] = \
                data0_cdb_out['smtp_list_{0}'.format(post_data['smtp_list'])]
            if post_data['smtp_choice'] == 'add':
                data_cdb_in['smtp_list_{0}'.format(post_data['smtp_list'])].append(post_data['smtp_address'])

            elif post_data['smtp_choice'] == 'delete':
                for index in data_cdb_in['smtp_list_{0}'.format(post_data['smtp_list'])]:
                    if index == post_data['smtp_address']:
                        data_cdb_in['smtp_list_{0}'.format(post_data['smtp_list'])].remove(index)

    # Update email document in CouchDB config database
    data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='email',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Get email document from CouchDB config database
    if not stat1_cdb:
        data2_cdb_out, stat2_cdb, http2_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='email',
            logfile=logfile,
        )

        if stat2_cdb:
            log = 'Could not update web GUI from CouchDB due to CouchDB error.'
            logger.warning(log)

        else:
            data_cdb_out = data2_cdb_out

    else:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def sms(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # This variable will get overwritten during success
    data_cdb_out = post_data

    # Convert posted data to usable form
    data_cdb_in = {'sms_enable': post_data['sms_enable']}

    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='sms',
        logfile=logfile,
    )

    # Update email document in CouchDB config database
    data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='sms',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Get email document from CouchDB config database
    if not stat1_cdb:
        data2_cdb_out, stat2_cdb, http2_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='sms',
            logfile=logfile,
        )

        if stat2_cdb:
            log = 'Could not update web GUI from CouchDB due to CouchDB error.'
            logger.warning(log)

        else:
            data_cdb_out = data2_cdb_out

    else:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def sms_list(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # This variable will get overwritten during success
    data_cdb_out = post_data

    # Convert posted data to usable form
    data_cdb_in = {}

    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='sms',
        logfile=logfile,
    )

    if not stat0_cdb:
        if post_data['sms_mobile'] != '':
            data_cdb_in['sms_list_{0}'.format(post_data['sms_list'])] = \
                data0_cdb_out['sms_list_{0}'.format(post_data['sms_list'])]
            if post_data['sms_gateway'] != 'delete':
                sms_address = post_data['sms_mobile'] + '@' + post_data['sms_gateway']
                data_cdb_in['sms_list_{0}'.format(post_data['sms_list'])].append(sms_address)

            elif post_data['sms_gateway'] == 'delete':
                for index in data_cdb_in['sms_list_{0}'.format(post_data['sms_list'])]:
                    mobile = index.split('@')[0]
                    if mobile == post_data['sms_mobile']:
                        data_cdb_in['sms_list_{0}'.format(post_data['sms_list'])].remove(index)

    # Update email document in CouchDB config database
    data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='sms',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Get email document from CouchDB config database
    if not stat1_cdb:
        data2_cdb_out, stat2_cdb, http2_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='sms',
            logfile=logfile,
        )

        if stat2_cdb:
            log = 'Could not update web GUI from CouchDB due to CouchDB error.'
            logger.warning(log)

        else:
            data_cdb_out = data2_cdb_out

    else:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def snmp(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # This variable will get overwritten during success
    data_cdb_out = post_data

    # Get snmp document from CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='snmp',
        logfile=logfile,
    )

    # Convert posted data to usable form
    data_cdb_in = {
        'agent_enable': post_data['agent_enable'],
        'notify_enable': post_data['notify_enable']
    }

    if post_data['server'] == '':
        data_cdb_in['server'] = None

    else:
        data_cdb_in['server'] = post_data['server']

    if post_data['port'] == '':
        data_cdb_in['port'] = None

    else:
        data_cdb_in['port'] = post_data['port']

    if post_data['community'] == '':
        data_cdb_in['community'] = None

    else:
        data_cdb_in['community'] = post_data['community']

    # Update snmp document in CouchDB config database
    data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='snmp',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Issue request to start/stop snmp agent
    if not stat0_cdb and not stat1_cdb:
        if data0_cdb_out['agent_enable'] != post_data['agent_enable']:
            if post_data['agent_enable']:
                MPQ_CMD0.put_nowait({
                    'command': 3,
                    'args': [],
                    'data': []
                })
            else:
                MPQ_CMD0.put_nowait({
                    'command': 4,
                    'args': [],
                    'data': []
                })

        # Issue request to start/stop snmp notifier
        if data0_cdb_out['notify_enable'] != post_data['notify_enable']:
            if post_data['notify_enable']:
                MPQ_CMD0.put_nowait({
                    'command': 5,
                    'args': [post_data['server'],
                             post_data['port'],
                             post_data['community']
                             ],
                    'data': []
                })
            else:
                MPQ_CMD0.put_nowait({
                    'command': 6,
                    'args': [],
                    'data': []
                })

        # Get snmp document from CouchDB config database
        data2_cdb_out, stat2_cdb, http2_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='snmp',
            logfile=logfile,
        )

        if stat2_cdb:
            log = 'Could not update web GUI from CouchDB due to CouchDB error.'
            logger.warning(log)

        else:
            data_cdb_out = data2_cdb_out

    else:
        log = 'Could not update config due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out

