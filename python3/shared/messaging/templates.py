import logging
from datetime import datetime
from shared.globals import STAT_LVL
from time import ctime
from shared import dbase

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'


logfile = 'janusess'
logger = logging.getLogger(logfile)


def message_templates(
    sms_enable: bool,
    msg_type: str,
    args: list
):
    """
    Retrieves message template and returns message dictionary

    :param sms_enable: bool
    :param msg_type: str
    :param args: list

    :return dict_smtp: dict
    :return stat_smtp_temp: STAT_LVL['op'] or STAT_LVL['crit']
    :return dict_sms: dict
    :return stat_sms_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_smtp_temp = STAT_LVL['op']
    dict_smtp = None

    # Get core document from CouchDB config database
    data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='core',
        logfile=logfile,
    )

    if not stat_cdb:

        # Determine message type and call function to build messaging body
        if msg_type == 'janusess_start':
            dict_smtp, stat_smtp_temp = smtp_janusess_start(
                dict_core=data_cdb_out,
                time_down=args[0]
            )
            if sms_enable and not stat_smtp_temp:
                dict_sms, stat_sms_temp = sms_janusess_start(
                    dict_core=data_cdb_out,
                    time_down=args[0]
                )
                dict_smtp.update(dict_sms)
                stat_smtp_temp = stat_sms_temp

        elif msg_type == 'poll_start':
            dict_smtp, stat_smtp_temp = smtp_poll_start(
                dict_core=data_cdb_out,
                addr_ln=args[0]
            )
            if sms_enable and not stat_smtp_temp:
                dict_sms, stat_sms_temp = sms_poll_start(
                    dict_core=data_cdb_out,
                    addr_ln=args[0]
                )
                dict_smtp.update(dict_sms)
                stat_smtp_temp = stat_sms_temp

        elif msg_type == 'poll_stop':
            dict_smtp, stat_smtp_temp = smtp_poll_stop(
                dict_core=data_cdb_out,
                addr_ln=args[0]
            )
            if sms_enable and not stat_smtp_temp:
                dict_sms, stat_sms_temp = sms_poll_stop(
                    dict_core=data_cdb_out,
                    addr_ln=args[0]
                )
                dict_smtp.update(dict_sms)
                stat_smtp_temp = stat_sms_temp

        elif msg_type == 'alert_new':
            dict_smtp, stat_smtp_temp = smtp_alert_new(
                dict_core=data_cdb_out,
                data_poll=args[0]
            )
            if sms_enable and not stat_smtp_temp:
                dict_sms, stat_sms_temp = sms_alert(
                    dict_core=data_cdb_out,
                    data_poll=args[0]
                )
                dict_smtp.update(dict_sms)
                stat_smtp_temp = stat_sms_temp

        elif msg_type == 'alert_decreased':
            dict_smtp, stat_smtp_temp = smtp_alert_decreased(
                dict_core=data_cdb_out,
                data_poll=args[0],
                dict_alert_hist=args[1]
            )
            if sms_enable and not stat_smtp_temp:
                dict_sms, stat_sms_temp = sms_alert(
                    dict_core=data_cdb_out,
                    data_poll=args[0]
                )
                dict_smtp.update(dict_sms)
                stat_smtp_temp = stat_sms_temp

        elif msg_type == 'alert_increased':
            dict_smtp, stat_smtp_temp = smtp_alert_increased(
                dict_core=data_cdb_out,
                data_poll=args[0],
                dict_alert_hist=args[1]
            )
            if sms_enable and not stat_smtp_temp:
                dict_sms, stat_sms_temp = sms_alert(
                    dict_core=data_cdb_out,
                    data_poll=args[0]
                )
                dict_smtp.update(dict_sms)
                stat_smtp_temp = stat_sms_temp

        elif msg_type == 'alert_stable':
            dict_smtp, stat_smtp_temp = smtp_alert_stable(
                dict_core=data_cdb_out,
                data_poll=args[0],
                dict_alert_hist=args[1]
            )
            if sms_enable and not stat_smtp_temp:
                dict_sms, stat_sms_temp = sms_alert(
                    dict_core=data_cdb_out,
                    data_poll=args[0]
                )
                dict_smtp.update(dict_sms)
                stat_smtp_temp = stat_sms_temp

        elif msg_type == 'alert_cancel':
            dict_smtp, stat_smtp_temp = smtp_alert_cancel(
                dict_core=data_cdb_out,
                data_poll=args[0]
            )
            if sms_enable and not stat_smtp_temp:
                dict_sms, stat_sms_temp = sms_alert_cancel(
                    dict_core=data_cdb_out,
                    data_poll=args[0]
                )
                dict_smtp.update(dict_sms)
                stat_smtp_temp = stat_sms_temp

        elif msg_type == 'status_dispatch':
            dict_smtp, stat_smtp_temp = smtp_status_dispatch(dict_core=data_cdb_out)
            if sms_enable and not stat_smtp_temp:
                dict_sms, stat_sms_temp = sms_status_dispatch(dict_core=data_cdb_out)
                dict_smtp.update(dict_sms)
                stat_smtp_temp = stat_sms_temp

        elif msg_type == 'error_dispatch':
            dict_smtp, stat_smtp_temp = smtp_error_dispatch(
                dict_core=data_cdb_out,
                log_entry=args[0]
            )
            if sms_enable and not stat_smtp_temp:
                dict_sms, stat_sms_temp = sms_error_dispatch(
                    dict_core=data_cdb_out,
                    log_entry=args[0]
                )
                dict_smtp.update(dict_sms)
                stat_smtp_temp = stat_sms_temp

    else:
        log = 'Failed to build JanusESS {0} messages due to CouchDB error.'.\
              format(msg_type)
        logger.debug(log)
        stat_smtp_temp = STAT_LVL['crit']

    return dict_smtp, stat_smtp_temp


def smtp_janusess_start(
        dict_core: dict,
        time_down: int
):
    """
    Prepares formatted SMTP message for JanusESS system start

    :param dict_core: dict
    :param time_down: int

    :return dict_smtp: dict
    :return stat_smtp_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_smtp_temp = STAT_LVL['op']
    dict_smtp = None

    # Get all documents from CouchDB lanes database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_all',
        cdb_name='lanes',
        logfile=logfile
    )

    if not stat0_cdb:

        body_smtp = """
JanusESS {0} (v{1}) start sequence complete at {2}.
System was down for {3} minute(s).
    
""".\
            format(
                dict_core['name'],
                dict_core['version'],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                time_down
            )

        # Cycle through lanes to build lane status message
        for addr_ln in range(0, 4):

            # If lane status is not configured, then add the following statement
            if data0_cdb_out[addr_ln]['status'] >= STAT_LVL['not_cfg']:
                body_smtp += """
========================
Lane {0} is not setup.
""".format(addr_ln)

            # If lane status is operational, then add the following statement
            elif data0_cdb_out[addr_ln]['status'] == STAT_LVL['op']:
                body_smtp += """
========================
Lane {0} is operational.
    
Modules connected:  {1}
------------------------
""".\
                    format(
                        addr_ln,
                        data0_cdb_out[addr_ln]['last_module']
                    )

                # Get lane status view from CouchDB modconfig database
                data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
                    cdb_cmd='get_view',
                    cdb_name='modconfig',
                    cdb_doc='stat_lane{0}'.format(addr_ln),
                    logfile=logfile,
                )

                if not stat1_cdb:
                    # Cycle through module statuses and add status messages to body
                    for addr_mod in data1_cdb_out:
                        stat_mod = ''
                        if addr_mod['value']['status'] == 0:
                            stat_mod = "Operational"

                        elif addr_mod['value']['status'] == 1:
                            stat_mod = "Operational Event"

                        elif addr_mod['value']['status'] == 2:
                            stat_mod = "Operational Error"

                        elif addr_mod['value']['status'] == 3:
                            stat_mod = "Critical Failure"

                        elif addr_mod['value']['status'] == 4:
                            stat_mod = "Not Setup"

                        elif addr_mod['value']['status'] == 5:
                            stat_mod = "Configuration Error"

                        elif addr_mod['value']['status'] == 6:
                            stat_mod = "Undetermined"

                        elif addr_mod['value']['status'] == 7:
                            stat_mod = "Not Tracked"

                        body_smtp += """
Module {0}: {1}""".\
                            format(
                                addr_mod['key'],
                                stat_mod
                            )

                # If polling is operational, add the following statements
                if data0_cdb_out[addr_ln]['poll'] < STAT_LVL['crit']:
                    body_smtp += """

Lane {0} polling unexpectedly stopped on {1}.
Polling will automatically restart.
    """.\
                        format(
                            addr_ln,
                            data0_cdb_out[addr_ln]['last_dtg']
                        )

                # If polling is not operational, add the following statement
                else:
                    body_smtp += """
                    
Lane {0} is not polling.
""".\
                        format(addr_ln)

        dict_smtp = {
            'smtp_subject': 'DO NOT REPLY JanusESS {0} (v{1}): NOTICE! JanusESS started'.
            format(
                dict_core['name'],
                dict_core['version']
            ),
            'smtp_body': body_smtp,
            'smtp_distribution': 's'
        }

        log = 'JanusESS start messages built.'
        logger.debug(log)

    else:
        log = 'Failed to build JanusESS start SMTP message due to CouchDB error.'
        logger.debug(log)
        stat_smtp_temp = STAT_LVL['crit']

    return dict_smtp, stat_smtp_temp


def smtp_poll_start(
    dict_core: dict,
    addr_ln: int
):
    """
    Prepares formatted SMTP message for poll start

    :param dict_core: dict
    :param addr_ln: int

    :return dict_smtp: dict
    :return stat_smtp_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_smtp_temp = STAT_LVL['op']

    body_smtp = """
JanusESS {0} (v{1}) lane {2} polling operations started at {3}.
""".\
        format(
            dict_core['name'],
            dict_core['version'],
            addr_ln,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    dict_smtp = {
        'smtp_subject': 'DO NOT REPLY JanusESS {0} (v{1}): NOTICE! Lane {2} polling operations started'.
        format(
            dict_core['name'],
            dict_core['version'],
            addr_ln
        ),
        'smtp_body': body_smtp,
        'smtp_distribution': 's'
    }

    log = 'JanusESS lane {0} polling start SMTP message built.'.format(addr_ln)
    logger.debug(log)

    return dict_smtp, stat_smtp_temp


def smtp_poll_stop(
    dict_core: dict,
    addr_ln: int
):
    """
    Prepares formatted SMTP message for poll stop

    :param dict_core: dict
    :param addr_ln: int

    :return dict_smtp: dict
    :return stat_smtp_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_smtp_temp = STAT_LVL['op']

    body_smtp = """
JanusESS {0} (v{1}) lane {2} polling operations concluded at {3}.
""".\
        format(
            dict_core['name'],
            dict_core['version'],
            addr_ln,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    dict_smtp = {
        'smtp_subject': 'DO NOT REPLY JanusESS {0} (v{1}): NOTICE! Lane {2} polling operations concluded'.
        format(
            dict_core['name'],
            dict_core['version'],
            addr_ln
        ),
        'smtp_body': body_smtp,
        'smtp_distribution': 's'
    }

    log = 'JanusESS lane {0} polling stop SMTP message built.'.format(addr_ln)
    logger.debug(log)

    return dict_smtp, stat_smtp_temp


def smtp_alert_new(
    dict_core: dict,
    data_poll: list
):
    """
    Prepares formatted SMTP message for new sensor alert condition

    :param dict_core: dict
    :param data_poll: list

    data_poll[0] = module id
    data_poll[1] = module location
    data_poll[2] = lane address
    data_poll[3] = module address
    data_poll[4] = sensor address
    data_poll[5] = alert type
    data_poll[6] = sensor type
    data_poll[7] = sensor value
    data_poll[8] = sensor value dtg
    data_poll[9] = sensor value unit
    data_poll[10] = trigger

    :return dict_smtp: dict
    :return stat_smtp_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_smtp_temp = STAT_LVL['op']

    uid_mod = data_poll[0]
    loc_mod = data_poll[1]
    addr_ln = data_poll[2]
    addr_mod = data_poll[3]
    addr_s = data_poll[4]
    alert_type = data_poll[5]
    sensor_type = data_poll[6]
    converted_val = data_poll[7]
    poll_dtg = data_poll[8]
    unit = data_poll[9]
    trigger = data_poll[10]

    body_smtp = """
A new sensor extreme value alert has been generated:

{0:>12}:    {1:<24}
{2:>12}:    {3:>8} {4}
{5:>12}:    {6:>8} {4}

""".\
        format(
            'DTG',
            ctime(float(poll_dtg)),
            sensor_type,
            converted_val,
            unit,
            'TRIGGER',
            trigger
        )

    dict_smtp = {
        'smtp_subject': 'DO NOT REPLY JanusESS {0} (v{1}): ALERT! New {2} value from {3} sensor at {4}'.
        format(
            dict_core['name'],
            dict_core['version'],
            alert_type,
            sensor_type,
            loc_mod
        ),
        'smtp_body': body_smtp,
        'smtp_distribution': 'p'
    }

    log = 'New alert SMTP message for module ID: {0}, at lane {1} '.format(uid_mod, addr_ln) +\
          'module {0} sensor {1} built.'.format(addr_mod, addr_s)
    logger.debug(log)

    return dict_smtp, stat_smtp_temp


def smtp_alert_decreased(
        dict_core: dict,
        data_poll: list,
        dict_alert_hist: list
):
    """
    Prepares formatted SMTP message for decreased sensor alert condition

    :param dict_core: dict
    :param data_poll: list
    :param dict_alert_hist: list

    data_poll[0] = module id
    data_poll[1] = module location
    data_poll[2] = lane address
    data_poll[3] = module address
    data_poll[4] = sensor address
    data_poll[5] = alert type
    data_poll[6] = sensor type
    data_poll[7] = sensor value
    data_poll[8] = sensor value dtg
    data_poll[9] = sensor value unit
    data_poll[10] = trigger

    :return dict_smtp: dict
    :return stat_smtp_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_smtp_temp = STAT_LVL['op']

    uid_mod = data_poll[0]
    loc_mod = data_poll[1]
    addr_ln = data_poll[2]
    addr_mod = data_poll[3]
    addr_s = data_poll[4]
    alert_type = data_poll[5]
    sensor_type = data_poll[6]
    converted_val = data_poll[7]
    poll_dtg = data_poll[8]
    unit = data_poll[9]
    trigger = data_poll[10]

    body_smtp = """
Sensor extreme value alert condition has decreased:

{0:>12}:    {1:<24}
{2:>12}:    {3:>8} {4}
{5:>12}:    {6:>8} {4}

Alert history this period:
------------------------
""".\
        format(
            'DTG',
            ctime(float(poll_dtg)),
            sensor_type,
            converted_val,
            unit,
            'TRIGGER',
            trigger
        )

    for alert in dict_alert_hist:
        body_smtp += """
DTG: {0},    VALUE: {1} {2},    TRIGGER: {3} {4}""".\
            format(
                ctime(float(alert['data_dtg'])),
                alert['value'],
                alert['unit'],
                alert['trigger'],
                alert['unit']
            )

    body_smtp += '\n'

    dict_smtp = {
        'smtp_subject': 'DO NOT REPLY JanusESS {0} (v{1}): ALERT! {2} and decreasing value from {3} sensor at {4}'.
        format(
            dict_core['name'],
            dict_core['version'],
            alert_type,
            sensor_type,
            loc_mod
        ),
        'smtp_body': body_smtp,
        'smtp_distribution': 'p'
    }

    log = 'Alert decreased SMTP message for module ID: {0}, '.format(uid_mod) + \
          'at lane {0} module {1} sensor {2} built.'.format(addr_ln, addr_mod, addr_s)
    logger.debug(log)

    return dict_smtp, stat_smtp_temp


def smtp_alert_increased(
    dict_core: dict,
    data_poll: list,
    dict_alert_hist: list
):
    """
    Prepares formatted SMTP message for increased sensor alert condition

    :param dict_core: dict
    :param data_poll: list
    :param dict_alert_hist: list

    data_poll[0] = module id
    data_poll[1] = module location
    data_poll[2] = lane address
    data_poll[3] = module address
    data_poll[4] = sensor address
    data_poll[5] = alert type
    data_poll[6] = sensor type
    data_poll[7] = sensor value
    data_poll[8] = sensor value dtg
    data_poll[9] = sensor value unit
    data_poll[10] = trigger

    :return dict_smtp: dict
    :return stat_smtp_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_smtp_temp = STAT_LVL['op']

    uid_mod = data_poll[0]
    loc_mod = data_poll[1]
    addr_ln = data_poll[2]
    addr_mod = data_poll[3]
    addr_s = data_poll[4]
    alert_type = data_poll[5]
    sensor_type = data_poll[6]
    converted_val = data_poll[7]
    poll_dtg = data_poll[8]
    unit = data_poll[9]
    trigger = data_poll[10]

    body_smtp = """
Sensor extreme value alert condition has increased:

{0:>12}:    {1:<24}
{2:>12}:    {3:>8} {4}
{5:>12}:    {6:>8} {4}

Alert history this period:
------------------------
""".\
        format(
            'DTG',
            ctime(float(poll_dtg)),
            sensor_type,
            converted_val,
            unit,
            'TRIGGER',
            trigger
        )

    for alert in dict_alert_hist:
        body_smtp += """
DTG: {0},    VALUE: {1} {2},    TRIGGER: {3} {4}""". \
            format(
                ctime(float(alert['data_dtg'])),
                alert['value'],
                alert['unit'],
                alert['trigger'],
                alert['unit']
            )

    body_smtp += '\n'

    dict_smtp = {
        'smtp_subject': 'DO NOT REPLY JanusESS {0} (v{1}): ALERT! {2} and increasing value from {3} sensor at {4}'.
        format(
            dict_core['name'],
            dict_core['version'],
            alert_type,
            sensor_type,
            loc_mod
        ),
        'smtp_body': body_smtp,
        'smtp_distribution': 'p'
    }

    log = 'Alert increased SMTP message for module ID: {0}, '.format(uid_mod) + \
          'at lane {0} module {1} sensor {2} built.'.format(addr_ln, addr_mod, addr_s)
    logger.debug(log)

    return dict_smtp, stat_smtp_temp


def smtp_alert_stable(
    dict_core: dict,
    data_poll: list,
    dict_alert_hist: list
):
    """
    Prepares formatted SMTP message for stable sensor alert condition

    :param dict_core: dict
    :param data_poll: list
    :param dict_alert_hist: list

    data_poll[0] = module id
    data_poll[1] = module location
    data_poll[2] = lane address
    data_poll[3] = module address
    data_poll[4] = sensor address
    data_poll[5] = alert type
    data_poll[6] = sensor type
    data_poll[7] = sensor value
    data_poll[8] = sensor value dtg
    data_poll[9] = sensor value unit
    data_poll[10] = trigger

    :return dict_smtp: dict
    :return stat_smtp_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_smtp_temp = STAT_LVL['op']

    uid_mod = data_poll[0]
    loc_mod = data_poll[1]
    addr_ln = data_poll[2]
    addr_mod = data_poll[3]
    addr_s = data_poll[4]
    alert_type = data_poll[5]
    sensor_type = data_poll[6]
    converted_val = data_poll[7]
    poll_dtg = data_poll[8]
    unit = data_poll[9]
    trigger = data_poll[10]

    body_smtp = """
Sensor extreme value alert condition remains stable:

{0:>12}:    {1:<24}
{2:>12}:    {3:>8} {4}
{5:>12}:    {6:>8} {4}

Alert history this period:
------------------------
""".\
        format(
            'DTG',
            ctime(float(poll_dtg)),
            sensor_type,
            converted_val,
            unit,
            'TRIGGER',
            trigger
        )

    for alert in dict_alert_hist:
        body_smtp += """
DTG: {0},    VALUE: {1} {2},    TRIGGER: {3} {4}""". \
            format(
                ctime(float(alert['data_dtg'])),
                alert['value'],
                alert['unit'],
                alert['trigger'],
                alert['unit']
            )

    body_smtp += '\n'

    dict_smtp = {
        'smtp_subject': 'DO NOT REPLY JanusESS {0} (v{1}): ALERT! {2} and stable value from {3} sensor at {4}'.
        format(
            dict_core['name'],
            dict_core['version'],
            alert_type,
            sensor_type,
            loc_mod
        ),
        'smtp_body': body_smtp,
        'smtp_distribution': 'p'
    }

    log = 'Alert stable SMTP message for module ID: {0}, at lane {1} '.format(uid_mod, addr_ln) + \
          'module {0} sensor {1} built.'.format(addr_mod, addr_s)
    logger.debug(log)

    return dict_smtp, stat_smtp_temp


def smtp_alert_cancel(
    dict_core: dict,
    data_poll: list
):
    """
    Prepares formatted SMTP message for sensor alert rescind

    :param dict_core: dict
    :param data_poll: list

    data_poll[0] = module id
    data_poll[1] = module location
    data_poll[2] = lane address
    data_poll[3] = module address
    data_poll[4] = sensor address
    data_poll[5] = alert type
    data_poll[6] = sensor type
    data_poll[7] = sensor value
    data_poll[8] = sensor value dtg
    data_poll[9] = sensor value unit
    data_poll[10] = trigger

    :return dict_smtp: dict
    :return stat_smtp_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_smtp_temp = STAT_LVL['op']

    uid_mod = data_poll[0]
    loc_mod = data_poll[1]
    addr_ln = data_poll[2]
    addr_mod = data_poll[3]
    addr_s = data_poll[4]
    sensor_type = data_poll[6]
    converted_val = data_poll[7]
    poll_dtg = data_poll[8]
    unit = data_poll[9]
    trigger = data_poll[10]

    body_smtp = """
Sensor values back in normal range.

{0:>12}:    {1:<24}
{2:>12}:    {3:>8} {4}
{5:>12}:    {6:>8} {4}
""".\
        format(
            'DTG',
            ctime(float(poll_dtg)),
            sensor_type,
            converted_val,
            unit,
            'TRIGGER',
            trigger
        )

    dict_smtp = {
        'smtp_subject': 'DO NOT REPLY JanusESS {0} (v{1}): Alert cancelled for {2} sensor at {3}'.
        format(
            dict_core['name'],
            dict_core['version'],
            sensor_type,
            loc_mod
        ),
        'smtp_body': body_smtp,
        'smtp_distribution': 'p'
    }

    log = 'Alert cancel SMTP message for module ID: {0}, at lane {1} '.format(uid_mod, addr_ln) + \
          'module {0} sensor {1} built.'.format(addr_mod, addr_s)
    logger.debug(log)

    return dict_smtp, stat_smtp_temp


def smtp_status_dispatch(
    dict_core: dict
):
    """
    Prepares formatted SMTP message for statuses

    :param dict_core: dict

    :return dict_smtp: dict
    :return stat_smtp_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_smtp_temp = STAT_LVL['op']
    dict_smtp = None

    # Get tasks document from CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='update',
        logfile=logfile,
    )

    # Get tasks document from CouchDB config database
    data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='network',
        logfile=logfile,
    )

    # Get all documents from CouchDB lanes database
    data2_cdb_out, stat2_cdb, http2_cdb = dbase.cdb_request(
        cdb_cmd='get_all',
        cdb_name='lanes',
        logfile=logfile
    )

    if not stat0_cdb and not stat1_cdb and not stat2_cdb:
        body_smtp = """
JanusESS {0} (v{1}) system {2}-hour self test results:
""".\
            format(
                dict_core['name'],
                dict_core['version'],
                data0_cdb_out['updateemail_interval'],
            )

        body_smtp += """
========================
NETWORK CONNECTIVITY CHECK:		  every {0} min
LAST NETWORK CONNECTIVITY CHECK:  {1}
""".\
            format(
                data1_cdb_out['network_interval'],
                data1_cdb_out['network_check_dtg'],
            )

        # Cycle through lanes to build lane status message
        for addr_ln in range(0, 4):
            if data2_cdb_out[addr_ln]['status'] > STAT_LVL['op']:
                body_smtp += """
========================
Lane {0} is not setup.
""".format(addr_ln)

            elif data2_cdb_out[addr_ln]['status'] == STAT_LVL['op']:
                body_smtp += """
========================
Lane {0} is operational.

Modules connected:  {1}
------------------------
""".\
                    format(
                        addr_ln,
                        data2_cdb_out[addr_ln]['last_module']
                    )

                # Get lane status view from CouchDB modconfig database
                data3_cdb_out, stat3_cdb, http3_cdb = dbase.cdb_request(
                    cdb_cmd='get_view',
                    cdb_name='modconfig',
                    cdb_doc='stat_lane{0}'.format(addr_ln),
                    logfile=logfile,
                )

                if not stat3_cdb:
                    # Cycle through module statuses and add status messages to body
                    for addr_mod in data3_cdb_out:
                        stat_mod = ''
                        if addr_mod['value']['status'] == 0:
                            stat_mod = "Operational"

                        elif addr_mod['value']['status'] == 1:
                            stat_mod = "Operational Event"

                        elif addr_mod['value']['status'] == 2:
                            stat_mod = "Operational Error"

                        elif addr_mod['value']['status'] == 3:
                            stat_mod = "Critical Failure"

                        elif addr_mod['value']['status'] == 4:
                            stat_mod = "Not Setup"

                        elif addr_mod['value']['status'] == 5:
                            stat_mod = "Configuration Error"

                        elif addr_mod['value']['status'] == 6:
                            stat_mod = "Undetermined"

                        elif addr_mod['value']['status'] == 7:
                            stat_mod = "Not Tracked"

                        body_smtp += """
Module {0}: {1}""". \
                            format(
                                addr_mod['key'],
                                stat_mod
                            )

                # If polling is not setup, add the following statement
                if data2_cdb_out[addr_ln]['poll'] > STAT_LVL['crit']:
                    body_smtp += """
                    
Lane {0} polling is not operating.
""".format(addr_ln)

                # If polling is operational, add the following statement
                elif data2_cdb_out[addr_ln]['poll'] == STAT_LVL['op']:

                    body_smtp += """
                    
In progress polling discovered for lane {0}...

DTG of LAST POLL: {1}
""".\
                        format(
                            addr_ln,
                            data2_cdb_out[addr_ln]['last_dtg']
                        )

                # If polling failed, add the following statement
                elif data2_cdb_out[addr_ln]['status'] == STAT_LVL['crit']:
                    body_smtp += """
                    
Lane {0} polling experienced catastrophic error.
""".format(addr_ln)

        dict_smtp = {
            'smtp_subject': 'DO NOT REPLY JanusESS {0} (v{1}): NOTICE! {2}-hour system status check'.
            format(
                dict_core['name'],
                dict_core['version'],
                data0_cdb_out['updateemail_interval']
            ),
            'smtp_body': body_smtp,
            'smtp_distribution': 's'
        }

        log = '{0}-hour status messages built.'.format(data0_cdb_out['updateemail_interval'])
        logger.debug(log)

    else:
        log = 'Failed to build JanusESS status SMTP message due to CouchDB error.'
        logger.debug(log)
        stat_smtp_temp = STAT_LVL['crit']

    return dict_smtp, stat_smtp_temp


def smtp_error_dispatch(
    dict_core: dict,
    log_entry: logging.LogRecord
):
    """
    Prepares formatted SMTP message for errors and critical failures

    :param dict_core: dict
    :param log_entry: str

    :return dict_smtp: dict
    :return stat_smtp_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_smtp_temp = STAT_LVL['op']

    body_smtp = """
JanusESS {0} (v{1}) experienced an execution error that needs urgent attention.
""".\
        format(
            dict_core['name'],
            dict_core['version']
        )

    body_smtp += """
========================
ERROR MESSAGE:
    
{0} * {1}: "<function '{2}' from '{3}'>: {4}
""". \
        format(
            ctime(float(log_entry.created)),
            log_entry.levelname,
            log_entry.funcName,
            log_entry.filename,
            log_entry.msg
        )

    dict_smtp = {
        'smtp_subject': 'DO NOT REPLY JanusESS {0} (v{1}): {2}! Program experienced execution flag'.
        format(
            dict_core['name'],
            dict_core['version'],
            log_entry.levelname
        ),
        'smtp_body': body_smtp,
        'smtp_distribution': 'e'
    }

    log = 'JanusESS error SMTP message built.'
    logger.debug(log)

    return dict_smtp, stat_smtp_temp


def sms_janusess_start(
    dict_core: dict,
    time_down: int
):
    """
    Prepares formatted SMS message for JanusESS system start

    :param dict_core: dict
    :param time_down: int

    :return dict_sms: dict
    :return stat_sms_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_sms_temp = STAT_LVL['op']
    dict_sms = None

    # Get all documents from CouchDB lanes database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_all',
        cdb_name='lanes',
        logfile=logfile
    )

    if not stat0_cdb:

        body_sms = "Started {0} hr--down {1} min. ". \
            format(
                datetime.now().strftime("%H:%M"),
                int(time_down)
            )

        # Cycle through lanes to build lane status message
        for addr_ln in range(0, 4):

            # If lane status is not configured, then add the following statement
            if data0_cdb_out[addr_ln]['status'] >= STAT_LVL['not_cfg']:
                body_sms += "Ln {0} inop. ".format(addr_ln)

            # If lane status is operational, then add the following statement
            elif data0_cdb_out[addr_ln]['status'] == STAT_LVL['op']:
                body_sms += "Ln {0} op, {1} mod ". \
                    format(
                        addr_ln,
                        data0_cdb_out[addr_ln]['last_module']
                    )

                # If polling is operational, add the following statements
                if data0_cdb_out[addr_ln]['poll'] < STAT_LVL['crit']:
                    body_sms += "(poll). "

                # If polling is not operational, add the following statement
                else:
                    body_sms += "(not poll). "

        dict_sms = {
            'sms_subject': '{0} Status'.format(dict_core['name']),
            'sms_body': body_sms,
            'sms_distribution': 's'
        }

        log = 'JanusESS start SMS message built.'
        logger.debug(log)

    else:
        log = 'Failed to build JanusESS start SMS message due to CouchDB error.'
        logger.debug(log)
        stat_sms_temp = STAT_LVL['crit']

    return dict_sms, stat_sms_temp


def sms_poll_start(
    dict_core: dict,
    addr_ln: int
):
    """
    Prepares formatted SMS message for poll start

    :param dict_core: dict
    :param addr_ln: int

    :return dict_sms: dict
    :return stat_sms_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_sms_temp = STAT_LVL['op']

    body_sms = "Ln {0} poll start {1} hr.". \
        format(
            addr_ln,
            datetime.now().strftime('%H:%M')
        )

    dict_sms = {
        'sms_subject': '{0} Poll'.format(dict_core['name']),
        'sms_body': body_sms,
        'sms_distribution': 's'
    }

    log = 'JanusESS lane {0} polling start SMS message built.'.format(addr_ln)
    logger.debug(log)

    return dict_sms, stat_sms_temp


def sms_poll_stop(
    dict_core: dict,
    addr_ln: int
):
    """
    Prepares formatted SMS message for poll stop

    :param dict_core: dict
    :param addr_ln: int

    :return dict_sms: dict
    :return stat_sms_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_sms_temp = STAT_LVL['op']

    body_sms = "Ln {0} poll stop {1} hr.". \
        format(
            addr_ln,
            datetime.now().strftime('%H:%M')
        )

    dict_sms = {
        'sms_subject': '{0} Poll'.format(dict_core['name']),
        'sms_body': body_sms,
        'sms_distribution': 's'
    }

    log = 'JanusESS lane {0} polling stop SMS message built.'.format(addr_ln)
    logger.debug(log)

    return dict_sms, stat_sms_temp


def sms_alert(
    dict_core: dict,
    data_poll: list
):
    """
    Prepares formatted SMS message for new sensor alert condition

    :param dict_core: dict
    :param data_poll: list

    data_poll[0] = module id
    data_poll[1] = module location
    data_poll[2] = lane address
    data_poll[3] = module address
    data_poll[4] = sensor address
    data_poll[5] = alert type
    data_poll[6] = sensor type
    data_poll[7] = sensor value
    data_poll[8] = sensor value dtg
    data_poll[9] = sensor value unit
    data_poll[10] = trigger

    :return dict_sms: dict
    :return stat_sms_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_sms_temp = STAT_LVL['op']
    uid_mod = data_poll[0]
    loc_mod = data_poll[1]
    addr_ln = data_poll[2]
    addr_mod = data_poll[3]
    addr_s = data_poll[4]
    sensor_type = data_poll[6]
    converted_val = data_poll[7]
    poll_dtg = data_poll[8]
    unit = data_poll[9]
    trigger = data_poll[10]

    body_sms = "{0} issue {1}, {2} hr, val: {3}{4}, limit: {5}{4}". \
        format(
            sensor_type.title(),
            loc_mod,
            ctime(float(poll_dtg))[11:19],
            converted_val,
            unit,
            trigger
        )

    dict_sms = {
        'sms_subject': '{0} Alert'.format(dict_core['name']),
        'sms_body': body_sms,
        'sms_distribution': 'p'
    }

    log = 'Alert SMS message for module ID: {0}, at lane {1} '.format(uid_mod, addr_ln) + \
          'module {0} sensor {1} built.'.format(addr_mod, addr_s)
    logger.debug(log)

    return dict_sms, stat_sms_temp


def sms_alert_cancel(
    dict_core: dict,
    data_poll: list
):
    """
    Prepares formatted SMS message for sensor alert rescind

    :param dict_core: dict
    :param data_poll: list

    data_poll[0] = module id
    data_poll[1] = module location
    data_poll[2] = lane address
    data_poll[3] = module address
    data_poll[4] = sensor address
    data_poll[5] = alert type
    data_poll[6] = sensor type
    data_poll[7] = sensor value
    data_poll[8] = sensor value dtg
    data_poll[9] = sensor value unit
    data_poll[10] = trigger

    :return dict_sms: dict
    :return stat_sms_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_sms_temp = STAT_LVL['op']

    uid_mod = data_poll[0]
    loc_mod = data_poll[1]
    addr_ln = data_poll[2]
    addr_mod = data_poll[3]
    addr_s = data_poll[4]
    sensor_type = data_poll[6]
    converted_val = data_poll[7]
    poll_dtg = data_poll[8]
    unit = data_poll[9]
    trigger = data_poll[10]

    body_sms = "{0} cancel {1}, {2} hr, val: {3}{4}, limit: {5}{4}". \
        format(
            sensor_type.title(),
            loc_mod,
            ctime(float(poll_dtg))[11:19],
            converted_val,
            unit,
            trigger
        )

    dict_sms = {
        'sms_subject': '{0} Alert'.format(dict_core['name']),
        'sms_body': body_sms,
        'sms_distribution': 'p'
    }

    log = 'Alert cancel SMS message for module ID: {0}, at lane {1} '.format(uid_mod, addr_ln) + \
          'module {0} sensor {1} built.'.format(addr_mod, addr_s)
    logger.debug(log)

    return dict_sms, stat_sms_temp


def sms_status_dispatch(
    dict_core: dict
):
    """
    Prepares formatted SMS message for statuses

    :param dict_core: dict

    :return dict_sms: dict
    :return stat_sms_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_sms_temp = STAT_LVL['op']
    dict_sms = None

    # Get tasks document from CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='update',
        logfile=logfile,
    )

    # Get tasks document from CouchDB config database
    data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='network',
        logfile=logfile,
    )

    # Get all documents from CouchDB lanes database
    data2_cdb_out, stat2_cdb, http2_cdb = dbase.cdb_request(
        cdb_cmd='get_all',
        cdb_name='lanes',
        logfile=logfile
    )

    if not stat0_cdb and not stat1_cdb and not stat2_cdb:
        body_sms = "{0}-hour update: ".format(data0_cdb_out['updateemail_interval'])

        # Cycle through lanes to build lane status message
        for addr_ln in range(0, 4):
            if data2_cdb_out[addr_ln]['status'] > STAT_LVL['op']:
                body_sms += "Ln {0} is inop. ".format(addr_ln)

            elif data2_cdb_out[addr_ln]['status'] == STAT_LVL['op']:
                body_sms += "Ln {0} is op, {1} mod ". \
                    format(
                        addr_ln,
                        data2_cdb_out[addr_ln]['last_module']
                    )

                # If polling is not setup, add the following statement
                if data2_cdb_out[addr_ln]['poll'] > STAT_LVL['crit']:
                    body_sms += "(not poll). ".format(addr_ln)

                # If polling is operational, add the following statement
                elif data2_cdb_out[addr_ln]['poll'] == STAT_LVL['op']:

                    body_sms += "(poll). ".format(addr_ln)

                # If polling failed, add the following statement
                elif data2_cdb_out[addr_ln]['status'] == STAT_LVL['crit']:
                    body_sms += "(poll failed). ".format(addr_ln)

        dict_sms = {
            'sms_subject': '{0} Status'.format(dict_core['name']),
            'sms_body': body_sms,
            'sms_distribution': 's'
        }

        log = '{0}-hour status SMS messaging built.'.format(data0_cdb_out['updateemail_interval'])
        logger.debug(log)

    else:
        log = 'Failed to build JanusESS start SMS message due to CouchDB error.'
        logger.debug(log)
        stat_sms_temp = STAT_LVL['crit']

    return dict_sms, stat_sms_temp


def sms_error_dispatch(
    dict_core: dict,
    log_entry: logging.LogRecord
):
    """
    Prepares formatted SMS message for errors and critical failures

    :param dict_core: dict
    :param log_entry: str

    :return dict_sms: dict
    :return stat_sms_temp: STAT_LVL['op'] or STAT_LVL['crit']
    """
    stat_sms_temp = STAT_LVL['op']

    body_sms = "<function '{1}' from '{2}'>: {3}". \
        format(
            dict_core['name'],
            log_entry.funcName,
            log_entry.filename,
            log_entry.msg
        )

    dict_sms = {
        'sms_subject': '{0} Error'.format(dict_core['name']),
        'sms_body': body_sms,
        'sms_distribution': 'e'
    }

    log = 'JanusESS error SMS message built.'
    logger.debug(log)

    return dict_sms, stat_sms_temp
