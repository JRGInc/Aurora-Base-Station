#!/usr/bin/env python3
__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

# Initialize Application processes
if __name__ == '__main__':
    import distro
    import logging.config
    import multiprocessing
    import os
    import threading
    import time
    from application.polling import poll
    from application.tasks import appdbase, network, systime, tasks
    from datetime import datetime
    from server.webserver import FlaskServer
    from shared import command, dbase, heartbeat
    from shared.globals import STAT_LVL, MPQ_ACT, MPQ_ACT_CMD, MPQ_STAT, MPQ_LN_SETUP, MPQ_CMD0, MPQ_CMD3, \
        MPQ_IFACE_SETUP, MPQ_LOG_LVL
    from shared.log.config import Logging
    from shared.messaging.smtp import send_mail
    from tendo import singleton

    # Configure logging
    log_config_obj = Logging()
    logging.config.dictConfig(log_config_obj.config)

    # Prevent a second instance of this script from running
    me = singleton.SingleInstance()

    # Get os information, differentiate between Ubuntu and Raspbian
    op_sys = distro.linux_distribution(full_distribution_name=False)

    # Inject initial empty log entries for easy-to-spot visual markers in
    # logs to show where JanusESS was started/restarted
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

    for log_file in logs:
        logger = logging.getLogger(log_file)
        for i in range(1, 6):
            logger.info('')

        log = 'JanusESS logging started'
        logger.info(log)

    # Set log file for JanusESS start sequence actions
    logfile = 'janusess'
    logger = logging.getLogger(logfile)
    MPQ_STAT.put_nowait([
        'base',
        [
            'logging',
            STAT_LVL['op']
        ]
    ])

    # Check to determine if CouchDB is operating
    dbase.cdb_check()
    dbase.mdb_check()

    # A simple check for corrupted primary CouchDB databases
    # This check is not a guarantee that databases are corruption-free
    # If any cannot be restored, then prevent JanusESS start
    db_list = [
        'config',
        'lanes',
        'modules',
        'modconfig'
    ]
    stat_cdb_dbases = dbase.recover(db_list=db_list)
    appdbase.compact()

    # Get log document from CouchDB config database
    data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='log',
        logfile=logfile
    )

    # Load custom log level from CouchDB into logger dictionary.
    # This must happen prior to any multiprocessing calls.
    # After multiprocessing calls must pass log level through queue to process.
    if not stat_cdb:
        for log_file in logs:
            if data_cdb_out[log_file] == 'DEBUG':
                logging.getLogger(log_file).setLevel(logging.DEBUG)
            elif data_cdb_out[log_file] == 'INFO':
                logging.getLogger(log_file).setLevel(logging.INFO)
            elif data_cdb_out[log_file] == 'ERROR':
                logging.getLogger(log_file).setLevel(logging.ERROR)
            elif data_cdb_out[log_file] == 'WARNING':
                logging.getLogger(log_file).setLevel(logging.WARNING)
            elif data_cdb_out[log_file] == 'CRITICAL':
                logging.getLogger(log_file).setLevel(logging.CRITICAL)

    # Set heartbeat activity logging level
    MPQ_ACT_CMD.put_nowait([
        'log_level',
        data_cdb_out['activity']
    ])

    # Reset log file for remaining JanusESS start sequence actions
    logfile = 'janusess'
    logger = logging.getLogger(logfile)

    # Clear old process id flags from CouchDB before
    # JanusESS processes are started
    data_cdb_in = {
        'janusess': os.getpid(),
        'command_listener': False,
        'heartbeat_activity': False,
        'heartbeat_status': False,
        'poll_dispatch': False,
        'tasks': False,
        'tornado_redirect_application': False,
        'tornado_redirectssl_application': False,
        'tornado_main_application': False,
        'tornado_websocket_application': False,
        'tornado_websocket_handler': False,
    }

    # Update base_pid document in CouchDB config document
    data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='config',
        cdb_doc='base_pid',
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Must complete network check prior to any actions that are trapped
    # by an try/except routine.  If except statement is thrown will result
    # in email--JanusESS needs to determine state of network before first
    # email is sent.
    network.check()

    # Initialize process ID CouchDB entry and begin heartbeat status listener process
    # to monitor statuses of JanusESS processes.  Must start this immediately after
    # network check to ensure that network check status is updated in CouchDB prior
    # to any other processes which are trapped by try/except routines.
    data_cdb_in = {}
    obj_hb = heartbeat.HeartBeat()
    stat_hb_stat = STAT_LVL['op']
    try:
        mp_hb_stat = multiprocessing.Process(
            target=obj_hb.stat_listener,
            args=()
        )
        mp_hb_stat.start()
        data_cdb_in['heartbeat_status'] = mp_hb_stat.pid

        log = 'Heartbeat status listener process started.'
        logger.debug(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'DEBUG',
            log
        ])

    except multiprocessing.ProcessError:
        log = 'Can not start heartbeat status listener due to multiprocessing error.'
        logger.exception(log)
        stat_hb_stat = STAT_LVL['not_cfg']

    # Start Tornado webserver main and websocket application processes
    flask_obj = FlaskServer()
    flask_obj.webserver()

    # Begin heartbeat activity listener process to monitor statuses of JanusESS processes.
    # Since this is a GUI-based process, do not start until after Tornado webserver is started.
    stat_hb_act = STAT_LVL['op']
    try:
        mp_hb_act = multiprocessing.Process(
            target=obj_hb.act_listener,
            args=()
        )
        mp_hb_act.start()
        data_cdb_in['heartbeat_activity'] = mp_hb_act.pid

        log = 'Heartbeat activity listener process started.'
        logger.debug(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'DEBUG',
            log
        ])

    except multiprocessing.ProcessError:
        log = 'Can not start heartbeat activity listener due to multiprocessing error.'
        logger.exception(log)
        stat_hb_act = STAT_LVL['not_cfg']

    # Check to determine if InfluxDB is operating
    dbase.idb_check()

    # If CouchDB, InfluxDB, and heartbeat checks show that they are
    # operational, continue to start JanusESS processes
    if not stat_cdb_dbases and not stat_hb_stat and not stat_hb_act:

        # Determine system downtime from last JanusESS operation
        time_down = systime.down()

        # Start task scheduler for regular tasks:
        #   Time keeper (every minute)
        #   CouchDB database archive (every minute)
        #   Network checks (every 30 minutes if network sensed, 5 otherwise)
        #   CouchDB compacts (interval defined by user)
        #   JanusESS status messaging updates (interval defined by user)
        try:
            th_sched = threading.Thread(
                target=tasks.task_scheduler,
                args=(
                    db_list,
                )
            )
            th_sched.start()
            data_cdb_in['tasks'] = th_sched.ident

        except threading.ThreadError:
            log = 'Can not start task scheduler due to threading error.'
            logger.exception(log)
            print(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'tasks',
                    STAT_LVL['cfg_err']
                ]
            ])

        # Start command listener to monitor command queues:
        #   MPQ_CMD0: User-initiated command requests
        #   MPQ_CMD1: Checks for neighbor-bus triggers
        #   MPQ_CMD2: User-initiated module sensor polling
        #   MPQ_CMD3: Lane/module initialization and setup routine
        #   MPQ_CMD4: Upload module configuration to module
        #   MPQ_CMD5: Recurring module sensor polling
        #
        # This process should be started prior to requests placed
        # into any of the six queues, otherwise queues will fill up
        try:
            mp_cmd = multiprocessing.Process(
                target=command.listener,
                args=()
            )
            mp_cmd.start()
            data_cdb_in['command_listener'] = mp_cmd.pid

        except multiprocessing.ProcessError:
            log = 'Can not start command listener due to multiprocessing error.'
            logger.exception(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'command_listener',
                    STAT_LVL['cfg_err']
                ]
            ])

        # Get snmp document from CouchDB config database
        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='snmp',
            logfile=logfile
        )

        if not stat_cdb:
            # If SNMP agent was previously enabled, request to start SNMP agent
            if data_cdb_out['agent_enable']:
                MPQ_CMD0.put({
                    'command': 3,
                    'args': [],
                    'data': []
                })
            else:
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'snmp_agent',
                        STAT_LVL['not_cfg']
                    ]
                ])

            # If SNMP notify was previously enabled, request to start SNMP notify
            if data_cdb_out['notify_enable']:
                MPQ_CMD0.put({
                    'command': 5,
                    'args': [
                        data_cdb_out['server'],
                        data_cdb_out['port'],
                        data_cdb_out['community']
                    ],
                    'data': []
                })
            else:
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'snmp_notify',
                        STAT_LVL['not_cfg']
                    ]
                ])

        else:
            log = 'Could not start SNMP services due to CouchDB ' +\
                  'retrieval error.'
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'snmp_agent',
                    STAT_LVL['cfg_err']
                ]
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'snmp_notify',
                    STAT_LVL['cfg_err']
                ]
            ])

        err_iface = STAT_LVL['not_cfg']
        for check in range(0, 20):
            if not MPQ_IFACE_SETUP.empty():
                err_iface = MPQ_IFACE_SETUP.get()
                break
            time.sleep(0.05)

        time.sleep(1)

        # Issue command to initialize and setup each lane
        if not err_iface:
            for addr_ln in range(0, 4):
                MPQ_CMD3.put([
                    addr_ln
                ])

        else:
            log = 'Failed to detect and initialize Janus interface board.'
            logger.critical(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
            print(log)

        log = 'Delaying completion of JanusESS startup until interface lane(s) setup is complete.'
        logger.info(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'INFO',
            log
        ])
        print(log)

        # Monitor MPQ_LN_SETUP to determine if all lanes are setup.
        # MPQ_LN_SETUP will issue a list of [stat, lane] during JanusESS
        # startup.
        #
        # TODO: Determine length of ln setup time for 126-module chain
        # TODO: Multiply this length by 16 (4 ch x 4 chks per second)
        # TODO: Use this value as range end point on for loop
        for check in range(0, 940):
            if not MPQ_LN_SETUP.empty():
                addr_ln, stat_ln = MPQ_LN_SETUP.get()
                if stat_ln == 0:
                    log = 'Setup of interface lane {0} complete.'.format(addr_ln)
                    logger.info(log)
                    print(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'DEBUG',
                        log
                    ])

                elif (stat_ln > 0) and (stat_ln <= 3):
                    log = 'Interface lane {0} experienced errors.'.format(addr_ln)
                    logger.warning(log)
                    print(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'WARNING',
                        log
                    ])

                else:
                    log = 'Interface lane {0} is not setup.'.format(addr_ln)
                    logger.warning(log)
                    print(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'WARNING',
                        log
                    ])

                if not err_iface and (addr_ln == 3):
                    log = 'Setup processes of all interface lanes complete, starting poll dispatcher.'
                    logger.info(log)
                    print(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'INFO',
                        log
                    ])
                    break

            time.sleep(0.05)

        # Determine if interrupted module sensor polling was interrupted
        # Cycle through all lanes and determine if any polling was interrupted

        # Get all documents from CouchDB lanes database
        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='get_all',
            cdb_name='lanes',
            logfile=logfile
        )

        if not stat_cdb:
            for addr_ln in range(0, 4):
                if data_cdb_out[addr_ln]['status'] == STAT_LVL['op']:

                    if data_cdb_out[addr_ln]['poll'] == STAT_LVL['op']:

                        log = 'JanusESS lane {0} polling inadvertently stopped after this '.format(addr_ln) + \
                              'poll: {0}'.format(data_cdb_out[addr_ln]['last_dtg'])
                        logger.warning(log)
                        MPQ_ACT.put_nowait([
                            datetime.now().isoformat(' '),
                            'WARNING',
                            log
                        ])
                        print(log)

                        log = 'Restarting lane {0} polling.'.format(addr_ln)
                        logger.info(log)
                        MPQ_ACT.put_nowait([
                            datetime.now().isoformat(' '),
                            'INFO',
                            log
                        ])
                        print(log)

                    else:

                        log = 'Starting lane {0} polling.'.format(addr_ln)
                        logger.info(log)
                        MPQ_ACT.put_nowait([
                            datetime.now().isoformat(' '),
                            'INFO',
                            log
                        ])
                        print(log)

                    # Issue request to start polling
                    MPQ_CMD0.put_nowait({
                        'command': 0,
                        'args': [addr_ln],
                        'data': []
                    })

                else:
                    log = 'Not restarting lane {0} polling because lane is not properly set up.'.\
                        format(addr_ln)
                    logger.warning(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'WARNING',
                        log
                    ])
                    print(log)

                    MPQ_STAT.put_nowait([
                        'lane',
                        [
                            addr_ln,
                            {'poll': STAT_LVL['not_cfg']}
                        ]
                    ])
                    log = 'Cleared lane {0} poll configuration.'.format(addr_ln)
                    logger.warning(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'WARNING',
                        log
                    ])
                    print(log)

        else:
            log = 'Could not determine interrupted polling statuses due to CouchDB error.'
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'INFO',
                log
            ])

        # Start poll dispatcher process to dispatch recurring module sensor polling
        try:
            mp_poll = multiprocessing.Process(
                target=poll.dispatcher,
                args=()
            )
            mp_poll.start()
            data_cdb_in['poll_dispatch'] = mp_poll.pid

        except multiprocessing.ProcessError:
            log = 'Can not start poll dispatcher due to multiprocessing error.'
            logger.exception(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'poll_dispatch',
                    STAT_LVL['cfg_err']
                ]
            ])

        # Update base_pid document in CouchDB config database
        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='upd_doc',
            cdb_name='config',
            cdb_doc='base_pid',
            data_cdb_in=data_cdb_in,
            logfile=logfile
        )

        if stat_cdb:
            log = 'Could not set PID values in process status document due to CouchDB error.'
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])

        # Send JanusESS start messaging with timeout in seconds
        send_mail(
            msg_type='janusess_start',
            args=[time_down]
        )

        log = 'JanusESS startup completed.'
        logger.debug(log)
        print(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'INFO',
            log
        ])

        # Update log settings, this wil trickle to all threads via shared memory
        while True:
            if not MPQ_LOG_LVL.empty():
                mpq_record = MPQ_LOG_LVL.get()
                if mpq_record[1] == 'DEBUG':
                    logging.getLogger(mpq_record[0]).setLevel(logging.DEBUG)
                elif mpq_record[1] == 'INFO':
                    logging.getLogger(mpq_record[0]).setLevel(logging.INFO)
                elif mpq_record[1] == 'ERROR':
                    logging.getLogger(mpq_record[0]).setLevel(logging.ERROR)
                elif mpq_record[1] == 'WARNING':
                    logging.getLogger(mpq_record[0]).setLevel(logging.WARNING)
                elif mpq_record[1] == 'CRITICAL':
                    logging.getLogger(mpq_record[0]).setLevel(logging.CRITICAL)

            time.sleep(0.002)

    if stat_cdb_dbases:
        log = 'Could not start JanusESS due to CouchDB database corruption.'
        logger.critical(log)
        print(log)

    if stat_hb_stat:
        log = 'Could not start JanusESS due to heartbeat status multiprocessing error.'
        logger.critical(log)
        print(log)

    if stat_hb_act:
        log = 'Could not start JanusESS due to heartbeat activity multiprocessing error.'
        logger.critical(log)
        print(log)
