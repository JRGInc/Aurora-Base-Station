import logging
import requests
import threading
import time
from application.setup import lane
from datetime import datetime
from interface.interface import Interface
from interface.memorymap import MMAP
from shared import dbase
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT, MPQ_POLL_COMPLETE, MPQ_IFACE_SETUP, MPQ_CMD0, MPQ_CMD1, \
    MPQ_CMD2, MPQ_CMD3, MPQ_CMD4, MPQ_CMD5, MPQ_POLL_START, MPQ_POLL_STOP, MPQ_SNMPN_STOP, MPQ_SNMPA_STOP


__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'command'
logger = logging.getLogger(logfile)


def listener():
    """
    Listener for commands to execute
    """
    from application.polling import flag, poll

    # Initialize operations and Janus interface libraries
    # Enable interrupts immediately
    obj_cmd = Command()
    obj_iface = Interface()
    obj_iface.interrupts_enable()

    # Send message to JanusESS main to proceed with JanusESS startup procedures
    MPQ_IFACE_SETUP.put_nowait(obj_iface.error_iface())

    stat_cmd_prev = STAT_LVL['not_cfg']

    # This while loop has no exit, JanusESS will not function without this
    # ongoing loop to check the following command queues in priority order:
    #
    #   MPQ_CMD0: User-initiated command requests
    #   MPQ_CMD1: Checks for neighbor-bus triggers
    #   MPQ_CMD2: User-initiated module sensor polling
    #   MPQ_CMD3: Lane/module initialization and setup routine
    #   MPQ_CMD4: Upload module configuration to module
    #   MPQ_CMD5: Recurring module sensor polling
    while True:
        stat_cmd = STAT_LVL['op']

        # User-initiated command requests
        if not MPQ_CMD0.empty():
            data_cmd0_in = MPQ_CMD0.get()
            log = 'Priority 0 command, command #{0} request received.'.\
                  format(data_cmd0_in['command'])
            logger.debug(log)

            log = 'Command {0} called.'.format(data_cmd0_in['command'])
            logger.info(log)

            if data_cmd0_in['command'] == 'log_level':
                if data_cmd0_in['args'][0] == 'DEBUG':
                    logger.setLevel(logging.DEBUG)
                elif data_cmd0_in['args'][0] == 'INFO':
                    logger.setLevel(logging.INFO)
                elif data_cmd0_in['args'][0] == 'ERROR':
                    logger.setLevel(logging.ERROR)
                elif data_cmd0_in['args'][0] == 'WARNING':
                    logger.setLevel(logging.WARNING)
                elif data_cmd0_in['args'][0] == 'CRITICAL':
                    logger.setLevel(logging.CRITICAL)

            else:
                try:
                    th_cmd0 = threading.Thread(
                        target=obj_cmd.exec_cmd,
                        args=(
                            data_cmd0_in['command'],
                            data_cmd0_in['args'],
                            data_cmd0_in['data'],
                        )
                    )
                    th_cmd0.start()

                except threading.ThreadError:
                    stat_cmd = STAT_LVL['op_err']
                    log = 'Could not start user-initiated command due to threading error.'
                    logger.exception(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'CRITICAL',
                        log
                    ])

            log = 'Priority 0 interface request concluded.'
            logger.info(log)

        # Checks for neighbor-bus triggers
        #
        # This command is only executed if a trigger flag is discovered during
        # recurring module sensor polling
        elif not MPQ_CMD1.empty():
            MPQ_CMD1.get()
            log = 'Priority 1 interface request received.'
            logger.debug(log)

            # Get all documents from CouchDB lanes database
            data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
                cdb_cmd='get_all',
                cdb_name='lanes',
                logfile=logfile
            )

            if not stat_cdb:
                # Cycle through lanes, if lane and lane
                # polling are operational, then continue procedure
                # to check module triggers
                for addr_ln in range(0, 4):
                    if (data_cdb_out[addr_ln]['status'] < STAT_LVL['crit']) \
                            and (data_cdb_out[addr_ln]['poll'] <
                                 STAT_LVL['crit']):

                        # Set four-port interface lane.  This function
                        # ignores single-port interface devices.
                        stat_iface = obj_iface.i2c_lane_set(addr_ln=addr_ln)

                        if not stat_iface:
                            # Get stat_chan view from CouchDB
                            # modconfig database
                            data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
                                cdb_cmd='get_view',
                                cdb_name='modconfig',
                                cdb_doc='stat_chan{0}'.format(addr_ln),
                                logfile=logfile,
                            )

                            # Cycle through each non-failed module connected
                            # to the lane
                            if not stat_cdb:
                                for dict_mod in data_cdb_out:
                                    if dict_mod['value']['status'] < STAT_LVL['crit']:

                                        # Call function to check an
                                        # individual module'strigger status
                                        evt_byte = MMAP[dict_mod['value']['mem_map_ver']]['M_EVT']
                                        stat_mod = flag.interrupt(
                                            obj_iface=obj_iface,
                                            addr_ln=addr_ln,
                                            addr_mod=dict_mod['key'],
                                            evt_byte=evt_byte
                                        )
                                        MPQ_STAT.put_nowait([
                                            'module', [
                                                dict_mod['id'],
                                                addr_ln,
                                                dict_mod['key'],
                                                stat_mod
                                            ]
                                        ])

                            else:
                                log = 'Could not check module interrupt flag due to CouchDB error.'
                                logger.critical(log)
                                MPQ_ACT.put_nowait([
                                    datetime.now().isoformat(' '),
                                    'CRITICAL',
                                    log
                                ])
                                stat_cmd = STAT_LVL['op_err']

                        else:
                            stat_cmd = STAT_LVL['op_err']
                            log = 'Could not complete priority 1 interface request ' + \
                                  'on lane {0} due to i2c lane '.format(addr_ln) +\
                                  'set error.'
                            logger.critical(log)
                            MPQ_ACT.put_nowait([
                                datetime.now().isoformat(' '),
                                'CRITICAL',
                                log
                            ])

                obj_iface.interrupt_clear_flag()
                log = 'Priority 1 interface request concluded.'
                logger.info(log)

            else:
                log = 'Could not complete priority 1 interface request due to CouchDB error.'
                logger.critical(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'CRITICAL',
                    log
                ])
                stat_cmd = STAT_LVL['op_err']

        # User-initiated module sensor polling
        #
        # This command only polls one module per request
        elif not MPQ_CMD2.empty():
            data_cmd2_in = MPQ_CMD2.get()
            uid_mod = data_cmd2_in[0]
            addr_ln = data_cmd2_in[1]
            addr_mod = data_cmd2_in[2]
            log = 'Lane {0} module {1} priority 2 interface request received.'.format(addr_ln, addr_mod)
            logger.info(log)

            # Set four-port interface lane.  This function ignores
            # single-port interface devices.
            stat_iface = obj_iface.i2c_lane_set(addr_ln=addr_ln)
            if not stat_iface:

                stat_poll_data, uid_mod_i2c = poll.get_data(
                    obj_iface=obj_iface,
                    uid_mod=uid_mod,
                    addr_ln=addr_ln,
                    addr_mod=addr_mod
                )

                if not stat_poll_data:
                    MPQ_STAT.put_nowait([
                        'base',
                        [
                            'poll_data',
                            STAT_LVL['op']
                        ]
                    ])

                    stat_iface, flag = obj_iface.interrupt_check_flag()
                    if flag:
                        MPQ_CMD1.put(True)

                    if not stat_iface:
                        log = 'Lane {0} module {1} on-demand poll completed.'.format(addr_ln, addr_mod)
                        logger.info(log)
                        MPQ_ACT.put_nowait([
                            datetime.now().isoformat(' '),
                            'INFO',
                            log
                        ])

                # USB reset interface board if bad data returned
                #
                # TODO: Need higher level tracking of this error
                # TODO: Do not wish to reset device more than once
                # TODO: If reset after first time fails, all
                # TODO:     related commands will be bypassed
                elif (stat_poll_data == STAT_LVL['op_err']) and \
                     (uid_mod_i2c != uid_mod):
                    obj_iface.setup()
                    obj_iface.interrupts_enable()

                    stat_cmd = STAT_LVL['op_err']

                    log = 'Resetting interface due to mismatch in module id: ' + \
                          'requested={0} vs polled={1}.'.format(uid_mod, uid_mod_i2c)
                    logger.warning(log)

            else:
                log = 'Could not complete priority 2 interface request on ' + \
                      'lane {0} module {1} '.format(addr_ln, addr_mod) +\
                      'due to i2c lane set error.'
                logger.critical(log)
                stat_cmd = STAT_LVL['op_err']

            log = 'Lane {0} module '.format(addr_ln) +\
                  '{0} priority 2 interface request concluded.'.format(addr_mod)
            logger.info(log)

        # Lane/module initialization and setup routine
        elif not MPQ_CMD3.empty():
            data_cmd3_in = MPQ_CMD3.get()
            addr_ln = data_cmd3_in[0]
            # FLAG_LNRST[addr_ln] = True
            log = 'Lane {0} priority 3 interface request received.'. \
                  format(addr_ln)
            logger.debug(log)

            log = 'Begin lane {0} network reset and initialization.'.\
                  format(addr_ln)
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'INFO',
                log
            ])

            # Call lane reset command to toggle GPIO pins
            stat_iface = lane.reset(
                obj_iface=obj_iface,
                addr_ln=addr_ln
            )

            if not stat_iface:
                # Call lane init command to setup any modules
                # connected to the lane
                stat_ch, stat_cdb = lane.init(
                    obj_iface=obj_iface,
                    addr_ln=addr_ln
                )

                if not stat_ch:
                    # Ensure that all interrupt flags are cleared prior
                    # to any other lane activity.  GPIO interrupts may
                    # get triggered during lane setup routines.
                    stat_iface = obj_iface.interrupt_clear_flag()

                    if not stat_iface:
                        log = 'Interrupt flags successfully cleared.'
                        logger.debug(log)
                        MPQ_ACT.put_nowait([
                            datetime.now().isoformat(' '),
                            'DEBUG',
                            log
                        ])

                        if not stat_cdb:
                            log = 'Lane {0} network reset and initialization complete.'.format(addr_ln)
                            logger.info(log)
                            MPQ_ACT.put_nowait([
                                datetime.now().isoformat(' '),
                                'INFO',
                                log
                            ])

                        else:
                            stat_cmd = STAT_LVL['op_err']
                            log = 'Lane {0} network reset and '.format(addr_ln) + \
                                  'initialization complete with CouchDB errors.'
                            logger.info(log)
                            MPQ_ACT.put_nowait([
                                datetime.now().isoformat(' '),
                                'WARNING',
                                log
                            ])

                    else:
                        stat_cmd = STAT_LVL['op_err']
                        log = 'Could not clear interrupt flags from interface due to interface error.'
                        logger.critical(log)
                        MPQ_ACT.put_nowait([
                            datetime.now().isoformat(' '),
                            'WARNING',
                            log
                        ])

                else:
                    stat_cmd = STAT_LVL['op_err']
                    log = 'Lane {0} network reset and initialization failed to complete.'.format(addr_ln)
                    logger.warning(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'CRITICAL',
                        log
                    ])

            else:
                stat_cmd = STAT_LVL['op_err']
                log = 'Could not initialize lane {0} network due to Neighbor Bus reset error.'.format(addr_ln)
                logger.critical(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'CRITICAL',
                    log
                ])

            # FLAG_LNRST[addr_ln] = False
            log = 'Lane {0} priority 3 interface request concluded.'.format(addr_ln)
            logger.info(log)

        # Upload module configuration to module
        elif not MPQ_CMD4.empty():
            while not MPQ_CMD4.empty():
                data_cmd4_in = MPQ_CMD4.get()
                uid_mod = data_cmd4_in[0]
                addr_ln = data_cmd4_in[1]
                addr_mod = data_cmd4_in[2]
                addr_mem = data_cmd4_in[3]
                data_iface_in = data_cmd4_in[4]

                log = 'Lane {0} module '.format(addr_ln) +\
                      '{0} priority 4 interface request received.'.format(addr_mod)
                logger.debug(log)

                stat_mod = STAT_LVL['op']

                # Set four-port interface lane.  This function ignores
                # single-port interface devices.
                stat_iface = obj_iface.i2c_lane_set(addr_ln=addr_ln)
                if not stat_iface:

                    stat_iface = obj_iface.i2c_write(
                        addr_ln=addr_ln,
                        addr_mod=addr_mod,
                        addr_mem=addr_mem,
                        data_iface_in=data_iface_in
                    )

                    if stat_iface:
                        stat_mod = STAT_LVL['crit']
                        stat_cmd = STAT_LVL['op_err']
                        log = 'Upload of module settings to lane {0} '.format(addr_ln) +\
                              'module {0} unsuccessful.'.format(addr_mod)
                        MPQ_ACT.put_nowait([
                            datetime.now().isoformat(' '),
                            'CRITICAL',
                            log
                        ])

                    else:
                        log = 'Upload of module settings to lane {0} '.format(addr_ln) +\
                              'module {0} successful.'.format(addr_mod)
                        MPQ_ACT.put_nowait([
                            datetime.now().isoformat(' '),
                            'INFO',
                            log
                        ])

                    logger.log(
                        logging.INFO if not stat_iface else logging.CRITICAL,
                        log
                    )
                    print(log)

                    MPQ_STAT.put_nowait([
                        'module',
                        [
                            uid_mod,
                            addr_ln,
                            addr_mod,
                            stat_mod
                        ]
                    ])

                else:
                    stat_cmd = STAT_LVL['op_err']
                    log = 'Could not complete priority 4 interface request on ' + \
                          'lane {0}, '.format(addr_ln) +\
                          'module {0} due to i2c lane set error.'.format(addr_mod)
                    logger.critical(log)

                log = 'Lane {0} module '.format(addr_ln) +\
                      '{0} priority 4 interface request concluded.'.format(addr_mod)
                logger.info(log)

        # Recurring module sensor polling
        #
        # While this command algorithm is essentially identical
        # to MPQ_CMD2 algorithm, it remains separate so that any
        # user-initiated polling request upon an individual
        # module will receive a much higher priority so that
        # execution takes place more quickly.
        elif not MPQ_CMD5.empty():
            time_a = time.time()
            data_cmd5_in = MPQ_CMD5.get()
            uid_mod = data_cmd5_in[0]
            addr_ln = data_cmd5_in[1]
            addr_mod = data_cmd5_in[2]
            log = 'Lane {0} module {1} '.format(addr_ln, addr_mod) +\
                  'priority 5 interface request received.'
            logger.info(log)

            # Set four-port interface lane.  This function ignores
            # single-port interface devices.
            stat_iface = obj_iface.i2c_lane_set(addr_ln=addr_ln)

            if not stat_iface:

                time_b = time.time()
                stat_poll_data, uid_mod_i2c = poll.get_data(
                    obj_iface=obj_iface,
                    uid_mod=uid_mod,
                    addr_ln=addr_ln,
                    addr_mod=addr_mod
                )
                print('Lane {0} module {1} priority 5 get_data time: {2}'.
                      format(addr_ln, addr_mod, round((time.time() - time_b), 3)))

                # Check for any interrupts on all lanes before polling again
                if not stat_poll_data:
                    MPQ_STAT.put_nowait([
                        'base',
                        [
                            'poll_data',
                            STAT_LVL['op']
                        ]
                    ])

                    stat_iface, flag = obj_iface.interrupt_check_flag()
                    if flag:
                        MPQ_CMD1.put(True)

                # USB reset interface board if bad data returned
                #
                # TODO: Need higher level tracking of this error
                # TODO: Do not wish to reset device more than once
                # TODO: If reset after first time fails, all
                # TODO:     related commands will be bypassed
                elif (stat_poll_data == STAT_LVL['op_err']) and \
                        (uid_mod_i2c != uid_mod):
                    obj_iface.setup()
                    obj_iface.interrupts_enable()

                    stat_cmd = STAT_LVL['op_err']

                    log = 'Resetting interface due to mismatch in module id: ' + \
                          'requested={0} vs polled={1}.'.format(uid_mod, uid_mod_i2c)
                    logger.warning(log)

                MPQ_POLL_COMPLETE.put_nowait([
                    addr_ln,
                    addr_mod
                ])

            else:
                stat_cmd = STAT_LVL['op_err']
                log = 'Could not complete priority 5 interface request on lane ' + \
                      '{0} module {1} '.format(addr_ln, addr_mod) +\
                      'due to i2c lane set error.'
                logger.critical(log)

            log = 'Lane {0} module {1} '.format(addr_ln, addr_mod) +\
                  'priority 5 interface request concluded.'
            logger.info(log)
            print('Lane {0} module {1} priority 5 time: {2}'.
                  format(addr_ln, addr_mod, round((time.time() - time_a), 3)))

        time.sleep(0.05)

        # If command listener status has changed, send heartbeat update
        if stat_cmd != stat_cmd_prev:
            stat_cmd_prev = stat_cmd
            MPQ_STAT.put_nowait([
                'base',
                [
                    'command_listener',
                    stat_cmd
                ]
            ])


class Command(object):
    """
    Execution of user-initiated commands
    """

    def __init__(self):
        """
        Sets object attributes
        """
        self.args = None
        self.data = None

    def exec_cmd(
        self,
        cmd: str,
        args: list,
        data: list
    ):
        """
        Starts command subprocess

        :param cmd: str
        :param args: list
        :param data: list
        """
        self.args = args
        self.data = data

        if cmd == 0:
            self.poll_start()
        elif cmd == 1:
            self.poll_stop()
        elif cmd == 2:
            self.poll_clear()
        elif cmd == 3:
            self.snmp_agent_start()
        elif cmd == 4:
            self.snmp_agent_stop()
        elif cmd == 5:
            self.snmp_notify_start()
        elif cmd == 6:
            self.snmp_notify_stop()

    def poll_start(self):
        """
        Starts polling

        self.args[0] = addr_ln
        self.args[1] = poll status
        self.args[2] = continuous
        self.args[3] = interval
        self.args[4] = count
        """
        logfile = 'polling'
        logger = logging.getLogger(logfile)

        # Issues request to poll dispatcher to begin polling on this lane
        MPQ_POLL_START.put_nowait(self.args)

        log = 'Lane {0} polling start request issued.'.format(self.args[0])
        logger.info(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'INFO',
            log
        ])

    def poll_stop(self):
        """
        Stops polling

        self.args[0] = addr_ln
        """
        logfile = 'polling'
        logger = logging.getLogger(logfile)

        # Send request to poll dispatcher to immediately stop
        # polling on this lane
        MPQ_POLL_STOP.put_nowait(self.args[0])

        log = 'Lane {0} polling stop request issued.'.format(self.args[0])
        logger.info(log)
        print(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'INFO',
            log
        ])

    def poll_clear(self):
        """
        Clears operation polling CouchDB

        self.args[0] = addr_ln
        """
        logfile = 'polling'
        logger = logging.getLogger(logfile)

        log = 'Attempting to clear lane {0} '.format(self.args[0]) +\
              'poll data from polling database.'
        logger.debug(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'DEBUG',
            log
        ])

        # Build and issue InfluxDB command to delete pertinent data
        data_idb_in = 'q=DROP SERIES WHERE "chan"=\'{0}\''.format(self.args[0])
        http_resp = requests.post(
            'http://localhost:8086/query?db=JanusESS',
            headers={'Content-type': 'application/x-www-form-urlencoded'},
            data=data_idb_in
        )

        # Determine result of command and issue status
        if http_resp.status_code == 200:
            log = 'Clear lane {0} poll data successful.'.\
                  format(self.args[0])
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'INFO',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'influxdb',
                    STAT_LVL['op']
                ]
            ])
        else:
            log = 'Could not clear lane {0} poll data due '.format(self.args[0]) +\
                  'to InfluxDB query error.'
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'influxdb',
                    STAT_LVL['op_err']
                ]
            ])

    @staticmethod
    def snmp_agent_start():
        """
        Starts SNMP agent
        """
        from server.snmp import agent

        # SNMP agent must be placed in thread rather than
        # multiprocess process because dynamic variables are
        # shared between main process and the agent
        obj_snmpa = agent.SNMPAgent()
        try:
            th_snmpa = threading.Thread(
                target=obj_snmpa.engine,
                args=()
            )
            th_snmpa.start()
            MPQ_STAT.put_nowait([
                'snmp_notify',
                th_snmpa.ident
            ])

        except threading.ThreadError:
            log = 'Could not start SNMP agent due to threading error.'
            logger.exception(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
            MPQ_STAT.put_nowait([
                'snmp_notify',
                False
            ])

    @staticmethod
    def snmp_agent_stop():
        """
        Stops SNMP agent
        """
        MPQ_SNMPA_STOP.put_nowait(None)

    def snmp_notify_start(self):
        """
        Starts SNMP notify

        self.args[0] = host ip
        self.args[1] = host port
        self.args[1] = host community
        """
        from server.snmp import notification

        # SNMP notifier must be placed in thread rather than
        # multiprocess process because dynamic variables are shared
        # between main process and the agent
        obj_snmpn = notification.SNMPNotify(
            self.args[0],
            self.args[1],
            self.args[2]
        )
        try:
            th_snmpn = threading.Thread(
                target=obj_snmpn.listener,
                args=()
            )
            th_snmpn.start()
            MPQ_STAT.put_nowait([
                'snmp_notify',
                th_snmpn.ident
            ])

        except threading.ThreadError:
            log = 'Could not start SNMP notifier due to threading error.'
            logger.exception(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
            MPQ_STAT.put_nowait([
                'snmp_notify',
                False
            ])

    @staticmethod
    def snmp_notify_stop():
        """
        Stops SNMP notify
        """
        MPQ_SNMPN_STOP.put_nowait(None)
