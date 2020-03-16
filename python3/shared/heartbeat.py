import logging
import queue
import time
from shared import conversion, dbase
from shared.globals import MPQ_WS, MPQ_LN_SETUP, MPQ_STAT, MPQ_ACT, MPQ_ACT_CMD, STAT_LVL, LOG_LVL, MPQ_SNMPA2, \
    MPQ_SNMPA3, MPQ_SNMPA4, MPQ_SNMPA5, MPQ_SNMPN2, MPQ_SNMPN3, MPQ_SNMPN4, MPQ_SNMPN5, MPQ_CMD3, FLAG_LNRST, \
    AUTO_LNRST
from time import ctime, strftime

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'heartbeat'
logger = logging.getLogger(logfile)


class HeartBeat(
    object
):
    def __init__(
        self
    ):
        """
        Setup heartbeat properties
        """

        # Unit conversions
        self.unit_convert = conversion.Conversion()

        self.MPQ_SNMPA2 = MPQ_SNMPA2
        self.MPQ_SNMPA3 = MPQ_SNMPA3
        self.MPQ_SNMPA4 = MPQ_SNMPA4
        self.MPQ_SNMPA5 = MPQ_SNMPA5
        self.MPQ_SNMPN2 = MPQ_SNMPN2
        self.MPQ_SNMPN3 = MPQ_SNMPN3
        self.MPQ_SNMPN4 = MPQ_SNMPN4
        self.MPQ_SNMPN5 = MPQ_SNMPN5

        # Heartbeat listener status
        # This status is not tracked outside this library
        self.stat_list = STAT_LVL['op']

        # Set process/thread id's to False
        self.pid_websocket = False
        self.tid_snmp_agent = False
        self.tid_snmp_notify = False

        # Set base unit heartbeat status database entry to initial values
        self.stat_base = {
            'command_listener': STAT_LVL['undeter'],
            'couchdb': STAT_LVL['undeter'],
            'mariadb': STAT_LVL['undeter'],
            'email': STAT_LVL['undeter'],
            'file': STAT_LVL['undeter'],
            'influxdb': STAT_LVL['undeter'],
            'interface': STAT_LVL['undeter'],
            'logging': STAT_LVL['undeter'],
            'network': STAT_LVL['undeter'],
            'poll_data': STAT_LVL['undeter'],
            'poll_dispatch': STAT_LVL['undeter'],
            'snmp_agent': STAT_LVL['undeter'],
            'snmp_notify': STAT_LVL['undeter'],
            'tasks': STAT_LVL['undeter']
        }

        # Update base_status document in CouchDB config database
        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='upd_doc',
            cdb_name='config',
            cdb_doc='base_status',
            data_cdb_in=self.stat_base,
            logfile=logfile
        )

        if stat_cdb == STAT_LVL['crit']:
            self.stat_list = STAT_LVL['crit']

        # Get tasks document from CouchDB config database
        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='network',
            logfile=logfile
        )

        if stat_cdb == STAT_LVL['crit']:
            self.stat_list = STAT_LVL['crit']

        # Set network status in tasks database entry to initial values
        self.stat_net = {
            'network_interval': data_cdb_out['interval_bad'],
            'network_check_dtg': None
        }
        self.url_net = data_cdb_out['url_server']

        # Update tasks document in CouchDB config database
        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='upd_doc',
            cdb_name='config',
            cdb_doc='network',
            data_cdb_in=self.stat_net,
            logfile=logfile
        )

        if stat_cdb == STAT_LVL['crit']:
            self.stat_list = STAT_LVL['crit']

        # Set lane heartbeat statuses to initial values
        self.stat_ln = [
            None,
            None,
            None,
            None
        ]
        self.rst_ln = [
            0,
            0,
            0,
            0
        ]

        # Get all documents from CouchDB lanes database
        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='get_all',
            cdb_name='lanes',
            logfile=logfile
        )

        if stat_cdb == STAT_LVL['crit']:
            self.stat_list = STAT_LVL['crit']

        # Cycle through lanes and set initial values for lane statuses
        for addr_ln in range(0, 4):
            self.stat_ln[addr_ln] = {
                'addr_ln': addr_ln,
                'status': STAT_LVL['undeter'],
                'last_module': 0,
                'setup_id': 0.0
            }

            # Update lane document in CouchDB lanes database
            data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
                cdb_cmd='upd_doc',
                cdb_name='lanes',
                cdb_doc='lane{0}_status'.format(addr_ln),
                data_cdb_in=self.stat_ln[addr_ln],
                logfile=logfile
            )

            if stat1_cdb == STAT_LVL['crit']:
                self.stat_list = STAT_LVL['crit']
                break

            self.stat_ln[addr_ln]['poll'] = data_cdb_out[addr_ln]['poll']
            self.stat_ln[addr_ln]['last_dtg'] = data_cdb_out[addr_ln]['last_dtg']
            self.stat_ln[addr_ln]['setup_id'] = 0

        # Initialize empty poll value list
        self.poll_val = []

    def stat_listener(
        self
    ):
        """
        Processes all heartbeat messages prior to pushing into other status queues.

        mpq_record[0][0] = type
        mpq_record[0][1] = data
        """
        # Do not start loop if class initialization did not cleaning execute
        # Do not continue loop if any heartbeat function did not cleanly execute
        while not self.stat_list:

            # All JanusESS status information enters this point
            if not MPQ_STAT.empty():
                mpq_record = MPQ_STAT.get()

                # This status catches changes in heartbeat log levels and implements
                # inside multiprocessing process
                if mpq_record[0] == 'log_level':
                    if mpq_record[1] == 'DEBUG':
                        logger.setLevel(logging.DEBUG)
                    elif mpq_record[1] == 'INFO':
                        logger.setLevel(logging.INFO)
                    elif mpq_record[1] == 'ERROR':
                        logger.setLevel(logging.ERROR)
                    elif mpq_record[1] == 'WARNING':
                        logger.setLevel(logging.WARNING)
                    elif mpq_record[1] == 'CRITICAL':
                        logger.setLevel(logging.CRITICAL)

                # This heartbeat status tracks if websocket handler process is functioning.
                # The websocket handler is only called when user loads/reloads a webpage.
                # If websocket handler is functioning, then statuses are placed in MPQ_WS.
                elif mpq_record[0] == 'websocket':
                    if mpq_record[1] != self.pid_websocket:
                        self.pid_websocket = mpq_record[1]

                        # Since activity listener is multiprocess, must pass pid via queue
                        MPQ_ACT_CMD.put_nowait([
                            'websocket',
                            self.pid_websocket,
                        ])

                        if self.pid_websocket:
                            self.ws_restart_base()
                            self.ws_restart_net()
                            self.ws_restart_ch()
                            self.ws_restart_mod()

                # This heartbeat status tracks if SNMP agent thread is functioning.
                # If SNMP agent is functioning, then statuses are placed in SNMP_AGENT_MPQ.
                elif mpq_record[0] == 'snmp_agent':
                    if mpq_record[1] != self.tid_snmp_agent:
                        self.tid_snmp_agent = mpq_record[1]
                        if self.tid_snmp_agent:
                            self.snmp_agent_restart_base()
                            self.snmp_agent_restart_ch()
                            self.snmp_agent_restart_mod()

                # This heartbeat status tracks if SNMP notification dispatcher thread
                # is functioning.  If SNMP notification dispatcher is functioning,
                # then statuses are placed in SNMP_NOTIFY_MPQ.
                elif mpq_record[0] == 'snmp_notify':
                    if mpq_record[1] != self.tid_snmp_notify:
                        self.tid_snmp_notify = mpq_record[1]

                # All base unit process statuses are pushed to base() method
                # for processing
                elif mpq_record[0] == 'base':
                    self.base(mpq_record[1])
                    log = 'Heartbeat base status record: {0}.'.format(mpq_record[1])
                    logger.debug(log)

                # All network check statuses are pushed to network() method
                # for processing
                elif mpq_record[0] == 'network':
                    self.network(mpq_record[1])
                    log = 'Heartbeat network status record: {0}.'.format(mpq_record[1])
                    logger.debug(log)

                # All interface lane statuses are pushed to lane() method
                # for processing
                elif mpq_record[0] == 'lane':
                    print('HEARTBEAT LANE: {0}'.format(mpq_record[1]))
                    self.lane(mpq_record[1])
                    log = 'Heartbeat lane status record: {0}.'.format(mpq_record[1])
                    logger.debug(log)

                # All module statuses are pushed to module() method
                # for processing
                elif mpq_record[0] == 'module':
                    self.module(mpq_record[1])
                    log = 'Heartbeat module status record: {0}.'.format(mpq_record[1])
                    logger.debug(log)

                # All module sensor polling data are pushed to poll() method
                # for processing
                elif mpq_record[0] == 'poll':
                    # print('HEARTBEAT POLLING VALUE: {0}'.format(mpq_record[1]))
                    self.poll(mpq_record[1])
                    log = 'Heartbeat polling value record: {0}.'.format(mpq_record[1])
                    logger.debug(log)

            time.sleep(0.02)

    def act_listener(
        self,
    ):
        """
        Places activity messages into websocket queue as they are received.

        mpq_record[0] = dtg
        mpq_record[1] = status
        mpq_record[2] = message
        """
        log_level = 'DEBUG'
        pid_websocket = False

        while not self.stat_list:

            # All JanusESS status information enters this point
            if not MPQ_ACT_CMD.empty():
                mpq_record = MPQ_ACT_CMD.get()
                if mpq_record[0] == 'log_level':
                    if log_level != mpq_record[1]:
                        log_level = mpq_record[1]

                if mpq_record[0] == 'websocket':
                    if pid_websocket != mpq_record[1]:
                        pid_websocket = mpq_record[1]

            # Only retrieve MPQ_ACT if websocket handler is functioning.
            if pid_websocket:
                if not MPQ_ACT.empty():
                    mpq_record = MPQ_ACT.get()

                    # Compare activity logging level with activity statement, if activity
                    # statement has higher level, place it onto queue
                    if LOG_LVL[mpq_record[1]] >= LOG_LVL[log_level]:
                        try:
                            MPQ_WS.put([
                                'activity',
                                mpq_record[0][:19] + ' ' + mpq_record[1] + ': ' + mpq_record[2]
                            ])

                        except queue.Full:
                            log = 'Can not place item in activity queue, malformed record or queue is full.'
                            logger.exception(log)

            time.sleep(0.02)

    def base(
        self,
        mpq_record: list
    ):
        """
        Places base process statuses into websocket and SNMP queues if status has changed.

        mpq_record[0] = process
        mpq_record[1] = process status

        :param mpq_record: list
        """
        process = mpq_record[0]
        process_stat = mpq_record[1]

        # Only process record if process status has changed
        if process_stat != self.stat_base[process]:
            self.stat_base[process] = process_stat

            # Initialize base status database entry
            data_cdb_in = {
                process: self.stat_base[process]
            }

            # Update base_status document in CouchDB config database
            data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
                cdb_cmd='upd_doc',
                cdb_name='config',
                cdb_doc='base_status',
                data_cdb_in=data_cdb_in,
                logfile=logfile
            )

            if stat_cdb == STAT_LVL['crit']:
                log = 'Failed to update base_status document in CouchDB config database.'
                logger.critical(log)

            # Only place into MPQs if processes/threads are functioning.
            try:
                if self.pid_websocket:
                    MPQ_WS.put_nowait([
                        'base',
                        process,
                        self.stat_base[process]
                    ])

                # Filter out SNMP-related messages, SNMP can not report on itself.
                if (process != 'snmp_agent') and (process != 'snmp_notify'):
                    if self.tid_snmp_agent:
                        self.MPQ_SNMPA2.put_nowait([
                            process,
                            self.stat_base[process]
                        ])
                    if self.tid_snmp_notify:
                        self.MPQ_SNMPN2.put_nowait([
                            process,
                            self.stat_base[process]
                        ])

            except queue.Full:
                log = 'Can not place item in base status queue, queue is full.'
                logger.exception(log)

    def network(
        self,
        mpq_record: list
    ):
        """
        Places network status into websocket and SNMP queues if status has changed.

        mpq_record[0] = network url checked
        mpq_record[1] = check interval
        mpq_record[2] = dtg

        :param mpq_record: list
        """
        stat_change = False

        url = mpq_record[0]
        interval = mpq_record[1]
        check_dtg = mpq_record[2]

        # Only process record if key values have changed
        if url != self.url_net:
            self.url_net = url
            stat_change = True

        if interval != self.stat_net['network_interval']:
            self.stat_net['network_interval'] = interval
            stat_change = True

        if check_dtg != self.stat_net['network_check_dtg']:
            self.stat_net['network_check_dtg'] = check_dtg
            stat_change = True

        # If any key value has changed, process record
        if stat_change:

            # Initialize network check database entry
            data_cdb_in = {
                'network_interval': self.stat_net['network_interval'],
                'network_check_dtg': self.stat_net['network_check_dtg']
            }

            # Update tasks document in CouchDB config database
            data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
                cdb_cmd='upd_doc',
                cdb_name='config',
                cdb_doc='network',
                data_cdb_in=data_cdb_in,
                logfile=logfile
            )

            if stat_cdb == STAT_LVL['crit']:
                log = 'Failed to update tasks document in CouchDB config database.'
                logger.critical(log)

            # Only place into MPQ_WS if websocket handler processes is functioning.
            try:
                if self.pid_websocket:
                    MPQ_WS.put_nowait([
                        'network',
                        self.url_net,
                        self.stat_net['network_interval'],
                        self.stat_net['network_check_dtg']
                    ])

            except queue.Full:
                log = 'Can not place item in network queue, queue is full.'
                logger.exception(log)

    def lane(
        self,
        mpq_record: list
    ):
        """
        Places lane statues into websocket and SNMP queues if status has changed.

        mpq_record[0] = lane address
        mpq_record[1] = lane dictionary

        :param mpq_record: list
        """
        stat_change = False
        setup_change = False

        addr_ln = mpq_record[0]
        dict_ln = mpq_record[1]

        # Only process record if key values have changed
        for key in dict_ln.keys():
            if dict_ln[key] != self.stat_ln[addr_ln][key]:
                self.stat_ln[addr_ln][key] = dict_ln[key]
                stat_change = True
                if key == 'setup_id':
                    setup_change = True

        # If any key value has changed, process record
        if stat_change:

            # Update lane document in CouchDB lanes database
            data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
                cdb_cmd='upd_doc',
                cdb_name='lanes',
                cdb_doc='lane{0}_status'.format(addr_ln),
                data_cdb_in=self.stat_ln[addr_ln],
                logfile=logfile
            )

            if stat_cdb == STAT_LVL['crit']:
                log = 'Failed to update lane{0}_status document in CouchDB lanes database.'.\
                      format(addr_ln)
                logger.critical(log)

            if setup_change:
                MPQ_LN_SETUP.put_nowait([
                    addr_ln,
                    self.stat_ln[addr_ln]['status']
                ])

            if self.stat_ln[addr_ln]['poll']:
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'poll_data',
                        STAT_LVL['not_cfg']
                    ]
                ])

            # Only place into MPQs if processes/threads are functioning.
            try:
                if self.pid_websocket:
                    MPQ_WS.put([
                        'lane',
                        addr_ln,
                        self.stat_ln[addr_ln]['status'],
                        self.stat_ln[addr_ln]['last_module'],
                        self.stat_ln[addr_ln]['poll'],
                        self.stat_ln[addr_ln]['last_dtg'],
                        self.stat_ln[addr_ln]['setup_id']
                    ])

                if self.tid_snmp_agent:
                    self.MPQ_SNMPA3.put([
                        addr_ln,
                        self.stat_ln[addr_ln]['status'],
                        self.stat_ln[addr_ln]['last_module'],
                        self.stat_ln[addr_ln]['poll'],
                        self.stat_ln[addr_ln]['last_dtg']
                    ])
                if self.tid_snmp_notify:
                    self.MPQ_SNMPN3.put([
                        addr_ln,
                        self.stat_ln[addr_ln]['status'],
                        self.stat_ln[addr_ln]['last_module'],
                        self.stat_ln[addr_ln]['poll'],
                        self.stat_ln[addr_ln]['last_dtg']
                    ])

            except queue.Full:
                log = 'Can not place item in lane status queue, queue is full.'
                logger.exception(log)

    def module(
        self,
        mpq_record: list
    ):
        """
        Places module statues into websocket and SNMP queues if status has changed.

        mpq_record[0] = module id
        mpq_record[1] = lane address
        mpq_record[2] = module address
        mpq_record[3] = module status

        :param mpq_record: list
        """
        uid_mod = mpq_record[0]
        addr_ln = mpq_record[1]
        addr_mod = mpq_record[2]
        stat_mod = mpq_record[3]

        # Only process for valid module ids, a module with '0000' failed I2C write
        # during setup
        #
        # NOTE: Do not change '0000' here without also changing application.setup.module.setup()
        if (uid_mod != '0000000000000000000000000000000000000000000000000000000000000000') and \
                (uid_mod is not None):

            print('HEARTBEAT MODULE: {0}'.format(mpq_record))

            # Get stat_lane view from CouchDB modconfig database
            # This determines if lane status should be downgraded if all modules error.
            data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
                cdb_cmd='get_view',
                cdb_name='modconfig',
                cdb_doc='stat_lane{0}'.format(addr_ln),
                logfile=logfile
            )

            ln_reset_flag = False

            if not stat0_cdb and not isinstance(data0_cdb_out, int):
                # Cycle through modules until module is located
                for dict_mod in data0_cdb_out:
                    if (uid_mod == dict_mod['id']) and (addr_mod == dict_mod['key']):

                        type_mod = dict_mod['value']['mod_type']
                        ver_mod = dict_mod['value']['mod_ver']
                        loc_mod = dict_mod['value']['loc']
                        num_sensors = dict_mod['value']['num_sensors']

                        # Initialize module database entry
                        mod_errno = dict_mod['value']['errno']
                        data_cdb_in = {
                            'status': stat_mod
                        }

                        # If module is operational, ensure module config errno field is reset
                        if stat_mod == STAT_LVL['op']:
                            mod_errno = 0
                            data_cdb_in['errno'] = mod_errno

                        # Modules do not report statuses above STAT_LVL['op_err'], this allows
                        # for heartbeat to initiate module recover processes
                        #
                        # If module reports an operational error,
                        # increment module config errno field
                        if stat_mod == STAT_LVL['op_err']:
                            mod_errno += 1
                            data_cdb_in['errno'] = mod_errno
                            log = 'Lane {0} module {1} id {2} error incremented to {3}'.\
                                  format(addr_ln, addr_mod, uid_mod, mod_errno)
                            print(log)
                            logger.warning(log)

                        # If three attempts are made to communicate with module, set status to
                        # STAT_LVL['crit']
                        if mod_errno == 3:

                            print('Pre Auto lane reset var: {0}'.format(AUTO_LNRST))
                            if AUTO_LNRST[addr_ln] <= 3:
                                AUTO_LNRST[addr_ln] += 1
                                ln_reset_flag = True
                            else:
                                ln_reset_flag = False
                            print('Post Auto lane reset var: {0}'.format(AUTO_LNRST))

                            data_cdb_in['status'] = STAT_LVL['crit']
                            stat_mod = STAT_LVL['crit']
                            log = 'Lane {0} module {1} '.format(addr_ln, addr_mod, uid_mod) +\
                                  'id {0} error incremented to {1}, '.format(uid_mod, mod_errno) +\
                                  'now considered failed.'
                            logger.critical(log)

                        # Update module document in CouchDB modconfig database.
                        # This document must be updated prior to any module
                        # recovery actions are executed.
                        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
                            cdb_cmd='upd_doc',
                            cdb_name='modconfig',
                            cdb_doc=uid_mod,
                            data_cdb_in=data_cdb_in,
                            logfile=logfile
                        )

                        # Execute lane/module recovery routine if module failed
                        #
                        # TODO: When designed, add module re-setup function here
                        if (not stat1_cdb) and (mod_errno == 3) and \
                                (stat_mod == STAT_LVL['crit']):

                            # MPQ_CMD3.put_no_wait([
                            #     addr_ln
                            # ])
                            print('Reset lane called.')
                            if ln_reset_flag and not FLAG_LNRST[addr_ln]:
                                MPQ_CMD3.put_nowait([
                                    addr_ln
                                ])

                        # Only place into MPQs if processes/threads are functioning.
                        try:
                            if self.pid_websocket:
                                MPQ_WS.put([
                                    'module',
                                    addr_ln,
                                    addr_mod,
                                    stat_mod
                                ])

                            if addr_mod is not None:
                                if self.tid_snmp_agent:
                                    self.MPQ_SNMPA4.put([
                                        addr_ln,
                                        addr_mod,
                                        type_mod,
                                        ver_mod,
                                        loc_mod,
                                        stat_mod,
                                        num_sensors
                                    ])
                                if self.tid_snmp_notify:
                                    self.MPQ_SNMPN4.put([
                                        addr_ln,
                                        addr_mod,
                                        type_mod,
                                        ver_mod,
                                        loc_mod,
                                        stat_mod,
                                        num_sensors
                                    ])

                        except queue.Full:
                            log = 'Can not place item in module status queue, queue is full.'
                            logger.exception(log)

                        break

                # Cycle through modules to determine if lane is inop
                stat_ln = STAT_LVL['crit']
                for dict_mod in data0_cdb_out:
                    if dict_mod['value']['status'] <= STAT_LVL['op_err']:
                        stat_ln = STAT_LVL['op']
                        break

                if stat_ln:
                    self.stat_ln[addr_ln]['status'] = stat_ln
                    try:
                        if self.pid_websocket:
                            MPQ_WS.put([
                                'lane',
                                addr_ln,
                                self.stat_ln[addr_ln]['status'],
                                self.stat_ln[addr_ln]['last_module'],
                                self.stat_ln[addr_ln]['poll'],
                                self.stat_ln[addr_ln]['last_dtg'],
                                self.stat_ln[addr_ln]['setup_id']
                            ])

                        if self.tid_snmp_agent:
                            self.MPQ_SNMPA3.put([
                                addr_ln,
                                self.stat_ln[addr_ln]['status'],
                                self.stat_ln[addr_ln]['last_module'],
                                self.stat_ln[addr_ln]['poll'],
                                self.stat_ln[addr_ln]['last_dtg']
                            ])
                        if self.tid_snmp_notify:
                            self.MPQ_SNMPN3.put([
                                addr_ln,
                                self.stat_ln[addr_ln]['status'],
                                self.stat_ln[addr_ln]['last_module'],
                                self.stat_ln[addr_ln]['poll'],
                                self.stat_ln[addr_ln]['last_dtg']
                            ])

                    except queue.Full:
                        log = 'Can not place item in lane status queue, queue is full.'
                        logger.exception(log)

        else:
            MPQ_CMD3.put_no_wait([
                addr_ln
            ])
            print('Reset lane called.')

        if uid_mod is None:
            if self.tid_snmp_agent:
                self.MPQ_SNMPA4.put([
                    addr_ln,
                    addr_mod,
                    'Null',
                    'Null',
                    'Null',
                    stat_mod,
                    0
                ])

    def poll(
        self,
        mpq_record: list
    ):
        """
        Places polling values into websocket and SNMP queues as they are received.

        :param mpq_record: list

        mpq_record[0][0] = module id
        mpq_record[0][1] = customer id
        mpq_record[0][2] = base unit id
        mpq_record[0][3] = module location
        mpq_record[0][4] = lane address
        mpq_record[0][5] = module address

        mpq_record[1][0] = sensor address
        mpq_record[1][1] = alert type
        mpq_record[1][2] = alert enabled
        mpq_record[1][3] = sensor type
        mpq_record[1][4] = sensor value
        mpq_record[1][5] = sensor value dtg
        mpq_record[1][6] = sensor value unit
        mpq_record[1][7] = trigger
        mpq_record[1][8] = trigger interval
        mpq_record[1][9] = trigger step
        """
        from shared.messaging.smtp import send_mail

        uid_mod = mpq_record[0][0]
        mod_loc = mpq_record[0][3]
        addr_ln = mpq_record[0][4]
        addr_mod = mpq_record[0][5]
        addr_s = mpq_record[1][0]
        alert_type = mpq_record[1][1]
        s_type = mpq_record[1][3]
        converted_val = mpq_record[1][4]
        data_dtg = mpq_record[1][5]
        unit = mpq_record[1][6]
        trigger = mpq_record[1][7]
        trig_int = mpq_record[1][8]
        trig_step = mpq_record[1][9]

        # Cycle through poll_value list to search for matching module and sensor
        # If found process alert value
        mod_found = False
        message = False
        msg_type = None
        msg_args = None

        # Get lane_status document from CouchDB lanes database
        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='dataunits',
            logfile=logfile
        )

        # Convert sensor value to user-selected unit
        s_value, s_unit = self.unit_convert.convert(
            converted_val,
            unit,
            data_cdb_out[s_type]
        )

        # Convert low-threshold value to user-selected unit
        t_value, t_unit = self.unit_convert.convert(
            trigger,
            unit,
            data_cdb_out[s_type]
        )

        for dict_alert in self.poll_val:
            if dict_alert['mod_uid'] == uid_mod:

                # A new alert period is triggered
                if (dict_alert['sensors'][addr_s]['type'] == 'off') and (alert_type != 'off'):
                    dict_alert_hist = {
                        'trigger': t_value,
                        'value': s_value,
                        'unit': s_unit,
                        'data_dtg': data_dtg
                    }
                    dict_alert['sensors'][addr_s]['prev_value'] = s_value
                    dict_alert['sensors'][addr_s]['value'] = s_value
                    dict_alert['sensors'][addr_s]['type'] = alert_type
                    dict_alert['sensors'][addr_s]['data_dtg'] = data_dtg
                    dict_alert['sensors'][addr_s]['history'].append(dict_alert_hist)

                    # Email settings for reporting new alert period
                    msg_type = 'alert_new'
                    msg_args = [
                        [],
                        'polling'
                    ]
                    message = True

                # Service existing low alert
                elif (dict_alert['sensors'][addr_s]['type'] == 'low') and (alert_type == 'low'):

                    # Existing low alert is stable
                    if (dict_alert['sensors'][addr_s]['value'] >
                            (dict_alert['sensors'][addr_s]['prev_value'] - trig_step)) and \
                            (dict_alert['sensors'][addr_s]['value'] <
                                (dict_alert['sensors'][addr_s]['prev_value'] + trig_step)):

                        # Email setting for reporting stable low alert
                        msg_type = 'alert_stable'

                    # Existing low alert with increased value
                    elif dict_alert['sensors'][addr_s]['value'] >= \
                            (dict_alert['sensors'][addr_s]['prev_value'] + trig_step):
                        dict_alert['sensors'][addr_s]['prev_value'] = s_value
                        msg_type = 'alert_increased'

                    # Existing low alert with decreased value
                    elif dict_alert['sensors'][addr_s]['value'] <= \
                            (dict_alert['sensors'][addr_s]['prev_value'] - trig_step):
                        dict_alert['sensors'][addr_s]['prev_value'] = s_value
                        msg_type = 'alert_decreased'

                    # If trigger interval has elapsed, conduct reporting
                    if data_dtg >= (dict_alert['sensors'][addr_s]['data_dtg'] + trig_int):
                        dict_alert_hist = {
                            'trigger': t_value,
                            'value': s_value,
                            'unit': s_unit,
                            'data_dtg': data_dtg
                        }
                        dict_alert['sensors'][addr_s]['value'] = s_value
                        dict_alert['sensors'][addr_s]['type'] = alert_type
                        dict_alert['sensors'][addr_s]['data_dtg'] = data_dtg
                        dict_alert['sensors'][addr_s]['history'].append(dict_alert_hist)

                        msg_args = [
                            [],
                            dict_alert['sensors'][addr_s]['history'],
                            'polling'
                        ]
                        message = True

                # Service existing high alert
                elif (dict_alert['sensors'][addr_s]['type'] == 'high') and (alert_type == 'high'):

                    # Existing high alert is stable
                    if (dict_alert['sensors'][addr_s]['value'] >
                            (dict_alert['sensors'][addr_s]['prev_value'] - trig_step)) and \
                            (dict_alert['sensors'][addr_s]['value'] <
                                (dict_alert['sensors'][addr_s]['prev_value'] + trig_step)):
                        # Email setting for reporting stable high alert
                        msg_type = 'alert_stable'

                    # Existing high alert with increased value
                    elif dict_alert['sensors'][addr_s]['value'] >= \
                            (dict_alert['sensors'][addr_s]['prev_value'] + trig_step):
                        dict_alert['sensors'][addr_s]['prev_value'] = s_value
                        msg_type = 'alert_increased'

                    # Existing high alert with decreased value
                    elif dict_alert['sensors'][addr_s]['value'] <= \
                            (dict_alert['sensors'][addr_s]['prev_value'] - trig_step):
                        dict_alert['sensors'][addr_s]['prev_value'] = s_value
                        msg_type = 'alert_decreased'

                    # If trigger interval has elapsed, conduct reporting
                    if data_dtg >= (dict_alert['sensors'][addr_s]['data_dtg'] + trig_int):
                        dict_alert_hist = {
                            'trigger': t_value,
                            'value': s_value,
                            'unit': s_unit,
                            'data_dtg': data_dtg
                        }
                        dict_alert['sensors'][addr_s]['value'] = s_value
                        dict_alert['sensors'][addr_s]['type'] = alert_type
                        dict_alert['sensors'][addr_s]['data_dtg'] = data_dtg
                        dict_alert['sensors'][addr_s]['history'].append(dict_alert_hist)

                        msg_args = [
                            [],
                            dict_alert['sensors'][addr_s]['history'],
                            'polling'
                        ]
                        message = True

                # Existing alert period is ended
                elif (dict_alert['sensors'][addr_s]['type'] != 'off') and (alert_type == 'off'):
                    dict_alert['sensors'][addr_s]['prev_value'] = None
                    dict_alert['sensors'][addr_s]['value'] = None
                    dict_alert['sensors'][addr_s]['type'] = alert_type
                    dict_alert['sensors'][addr_s]['data_dtg'] = None
                    dict_alert['sensors'][addr_s]['history'] = []

                    # Report end of alert period
                    msg_type = 'alert_cancel'
                    msg_args = [
                        [],
                        'polling'
                    ]
                    message = True

                mod_found = True
                break

        # A new alert period is issued for a new module
        if not mod_found:
            dict_mod = {
                'mod_uid': uid_mod,
                'sensors': []
            }

            # Cycle through all possible sensors to build alert structure
            # Some sensors are either not installed or may never issue alert data
            for sensor_id in range(0, 17):
                dict_alert = {
                    'data_dtg': None,
                    'type': 'off',
                    'prev_value': None,
                    'value': None,
                    'unit': None,
                    'history': []
                }
                dict_mod['sensors'].append(dict_alert)

            # Update data for specific sensor number
            if alert_type != 'off':
                dict_mod['sensors'][addr_s]['data_dtg'] = data_dtg
                dict_mod['sensors'][addr_s]['type'] = alert_type
                dict_mod['sensors'][addr_s]['prev_value'] = s_value
                dict_mod['sensors'][addr_s]['value'] = s_value

                dict_history = {
                    'trigger': t_value,
                    'value': s_value,
                    'unit': s_unit,
                    'data_dtg': data_dtg
                }
                dict_mod['sensors'][addr_s]['history'].append(dict_history)

                # Email settings for reporting new alert period
                msg_type = 'alert_new'
                msg_args = [
                    mpq_record,
                    'polling'
                ]
                message = True

            self.poll_val.append(dict_mod)

        # If changes take place in alert status, send messaging message
        if message:
            msg_args[0] = [
                uid_mod,
                mod_loc,
                addr_ln,
                addr_mod,
                addr_s,
                alert_type,
                s_type,
                s_value,
                data_dtg,
                s_unit,
                t_value,
            ]
            send_mail(
                msg_type=msg_type,
                args=msg_args,
            )

        # Only place into MPQs if processes/threads are functioning.
        try:
            if self.pid_websocket:
                MPQ_WS.put([
                    'poll',
                    addr_ln,
                    addr_mod,
                    addr_s,
                    mod_loc,
                    s_type,
                    s_value,
                    s_unit,
                    strftime("%H:%M:%S", time.localtime(float(data_dtg))),
                    alert_type,
                    t_value,
                ])

            if self.tid_snmp_agent:
                self.MPQ_SNMPA5.put([
                    uid_mod,
                    addr_ln,
                    addr_mod,
                    addr_s,
                    s_type,
                    s_value,
                    s_unit,
                    str(ctime(float(data_dtg))),
                    alert_type,
                    t_value,
                ])

            if self.tid_snmp_notify and message:
                self.MPQ_SNMPN5.put([
                    uid_mod,
                    addr_ln,
                    addr_mod,
                    addr_s,
                    s_type,
                    s_value,
                    s_unit,
                    str(ctime(float(data_dtg))),
                    alert_type,
                    t_value,
                ])

        except queue.Full:
            log = 'Can not place item in poll value queue, queue is full.'
            logger.exception(log)

    def ws_restart_base(
        self
    ):
        """
        Places all base unit statuses into queue when websocket handler is started/restarted
        """
        # This method is only called when websocket is operating
        # Cycle through all base unit statuses and place status in MPQ_WS queue
        for process in self.stat_base.keys():
            try:
                MPQ_WS.put_nowait([
                    'base',
                    process,
                    self.stat_base[process]
                ])

            except queue.Full:
                log = 'Can not place item in websocket queue, queue is full.'
                logger.exception(log)

    def ws_restart_net(
        self
    ):
        """
        Places all network statuses into queue when websocket handler is started/restarted
        """
        # This method is only called when websocket is operating
        # Cycle through network check values and place values into MPQ_WS
        try:
            MPQ_WS.put_nowait([
                'network',
                self.url_net,
                self.stat_net['network_interval'],
                self.stat_net['network_check_dtg']
            ])

        except queue.Full:
            log = 'Can not place item in websocket queue, queue is full.'
            logger.exception(log)

    def ws_restart_ch(
        self
    ):
        """
        Places all lane statuses into queue when websocket handler is started/restarted
        """
        # This method is only called when websocket is operating
        # Cycle through all lanes and place lane values into MPQ_WS
        for addr_ln in self.stat_ln:
            try:
                MPQ_WS.put([
                    'lane',
                    addr_ln['addr_ln'],
                    addr_ln['status'],
                    addr_ln['last_module'],
                    addr_ln['poll'],
                    addr_ln['last_dtg'],
                    addr_ln['setup_id']
                ])

            except queue.Full:
                log = 'Can not place item in lane status queue, queue is full.'
                logger.exception(log)

    def ws_restart_mod(
        self
    ):
        """
        Places all module statuses into queue when websocket handler is started/restarted
        """
        # This method is only called when websocket is operating
        # Cycle through all lanes

        for addr_ln in self.stat_ln:

            # Only place module statuses into MPQ_WS for operational lanes
            if not addr_ln['status']:

                # Get stat_lane from CouchDB modconfig database
                data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
                    cdb_cmd='get_view',
                    cdb_name='modconfig',
                    cdb_doc='stat_lane{0}'.format(addr_ln['addr_ln']),
                    logfile=logfile
                )

                if not stat_cdb:

                    # Cycle through all modules and place status values into MPQ_WS
                    for dict_mod in data_cdb_out:
                        try:
                            MPQ_WS.put([
                                'module',
                                addr_ln['addr_ln'],
                                dict_mod['key'],
                                dict_mod['value']['status']
                            ])

                        except queue.Full:
                            log = 'Can not place item in module status queue, queue is full.'
                            logger.exception(log)

    def snmp_agent_restart_base(
        self
    ):
        """
        Places all base unit statuses into snmp agent queue when snmp agent is started/restarted
        """
        # This method is only called when SNMP Agent is operating
        # Cycle through all base unit statuses and place status in SNMP_AGENT_MPQ queue
        for process in self.stat_base.keys():
            if (process != 'snmp_agent') and (process != 'snmp_notify'):
                try:
                    self.MPQ_SNMPA2.put_nowait([
                        process,
                        self.stat_base[process]
                    ])

                except queue.Full:
                    log = 'Can not place item in websocket queue, queue is full.'
                    logger.exception(log)

    def snmp_agent_restart_ch(
        self
    ):
        """
        Places all lane statuses into snmp agent queue when snmp agent is started/restarted
        """
        # This method is only called when SNMP Agent is operating
        # Cycle through all lanes and place lane values in SNMP_AGENT_MPQ queue
        for addr_ln in self.stat_ln:
            try:
                self.MPQ_SNMPA3.put([
                    addr_ln['addr_ln'],
                    addr_ln['status'],
                    addr_ln['last_module'],
                    addr_ln['poll'],
                    addr_ln['last_dtg']
                ])

            except queue.Full:
                log = 'Can not place item in lane status queue, queue is full.'
                logger.exception(log)

    def snmp_agent_restart_mod(
        self
    ):
        """
        Places all module statuses into snmp agent queue when snmp agent is started/restarted
        """
        # This method is only called when SNMP Agent is operating
        # Cycle through all lanes
        for addr_ln in self.stat_ln:

            # Only place module statuses into SNMP_AGENT_MPQ for operational lanes
            if not addr_ln['status']:

                # Get stat_lane from CouchDB modconfig database
                data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
                    cdb_cmd='get_view',
                    cdb_name='modconfig',
                    cdb_doc='stat_lane{0}'.format(addr_ln['addr_ln']),
                    logfile=logfile
                )

                if not stat_cdb:

                    # Cycle through all modules and place status values into SNMP_AGENT_MPQ
                    for dict_mod in data_cdb_out:
                        try:
                            if dict_mod['key'] is not None:
                                self.MPQ_SNMPA4.put([
                                    addr_ln['addr_ln'],
                                    dict_mod['key'],
                                    dict_mod['value']['mod_type'],
                                    dict_mod['value']['mod_ver'],
                                    dict_mod['value']['loc'],
                                    dict_mod['value']['status'],
                                    dict_mod['value']['num_sensors']
                                ])

                        except queue.Full:
                            log = 'Can not place item in module status queue, queue is full.'
                            logger.exception(log)
