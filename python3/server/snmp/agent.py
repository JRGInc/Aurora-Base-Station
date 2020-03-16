import abc
import logging
import queue
import threading
import time
from datetime import datetime
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asyncore.dgram import udp, udp6
from pysnmp.smi import builder
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT, MPQ_SNMPA2, MPQ_SNMPA3, MPQ_SNMPA4, MPQ_SNMPA5, MPQ_SNMPA_STOP

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'server'
logger = logging.getLogger(logfile)


class SNMPAgent(
    object
):
    """
    SNMP Agent

    This class operates an SNMP agent independently from any SNMP services loaded
    and executed by the operating system.  To prevent conflicts it may be best to
    disable operating system-based SNMP services.
    """

    def __init__(
        self
    ):
        """
        Sets object attributes
        """
        self.mib_instr_base = None
        self.mib_instr_lane = None
        self.mib_instr_module = None
        self.mib_instr_sensor = None
        self.mib_instr_poll = None
        self.sym_id_base = None
        self.sym_id_ln = None
        self.sym_id_mod = None
        self.sym_id_s = None
        self.sym_base = None
        self.sym_ln = None
        self.sym_mod = None
        self.sym_s = None
        self.eng_snmp = None
        self.ctx_snmp = None
        self.mib_builder = None

    def engine(
        self
    ):
        """
        Setup SNMP engine and context
        """
        log = 'SNMP agent engine initialization sequence begun.  ' +\
              'This may take a minute or two.'
        logger.info(log)
        print(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'INFO',
            log
        ])

        # Create SNMP engine with auto generated engineID and pre-bound
        # to socket transport dispatcher
        self.eng_snmp = engine.SnmpEngine()

        # Transport setup

        # UDP over IPv4 at 0.0.0.0:8900
        config.addTransport(
            self.eng_snmp,
            udp.domainName,
            udp.UdpTransport().openServerMode(
                iface=(
                    '',
                    8900
                )
            )
        )
        # UDP over IPv6 at [::]:8900
        config.addTransport(
            self.eng_snmp,
            udp6.domainName,
            udp6.Udp6Transport().openServerMode(
                iface=(
                    '::',
                    8900
                )
            )
        )

        # SNMPv2c setup

        # SecurityName <-> CommunityName mapping.
        config.addV1System(
            snmpEngine=self.eng_snmp,
            communityIndex='agent',
            communityName='janusess'
        )
        # Allow full MIB access for this user / securityModels at VACM
        # MIB 1.3.6.1.4.1.9934 refers to Janus Research Group
        # MIB 1.3.6.1.4.1.9934.0 refers to JanusESS Project
        config.addVacmUser(
            snmpEngine=self.eng_snmp,
            securityModel=2,
            securityName='agent',
            securityLevel='noAuthNoPriv',
            readSubTree=(1, 3, 6, 1, 4, 1, 9934, 0)
        )

        # Get default SNMP context this SNMP engine serves
        self.ctx_snmp = context.SnmpContext(snmpEngine=self.eng_snmp)

        # Create custom Managed Object Instance
        self.mib_builder = self.ctx_snmp.getMibInstrum().getMibBuilder()
        mib_sources = self.mib_builder.getMibSources() + \
            (
                builder.DirMibSource('/opt/Janus/ESS/python3/server/snmp/mibs'),
            )
        self.mib_builder.setMibSources(*mib_sources)

        # JANUS-MIB defines and locates all Janus Research Group projects
        # JANUSESS-MIB defines all JanusESS project entries
        self.mib_builder.loadModules(
            'JANUS-MIB',
            'JANUSESS-MIB'
        )

        self.config_base()
        self.config_lane()
        self.config_module()
        self.config_sensor()

        # Register SNMP Applications at the SNMP engine for particular SNMP context
        cmdrsp.GetCommandResponder(
            self.eng_snmp,
            self.ctx_snmp
        )
        cmdrsp.NextCommandResponder(
            self.eng_snmp,
            self.ctx_snmp
        )
        cmdrsp.BulkCommandResponder(
            self.eng_snmp,
            self.ctx_snmp
        )

        dispatcher = threading.Thread(
            target=self.dispatcher,
            args=()
        )
        dispatcher.start()
        MPQ_STAT.put_nowait([
            'snmp_agent',
            dispatcher.ident
        ])

        log = 'SNMP agent engine sequence concluded.'
        logger.info(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'INFO',
            log
        ])
        MPQ_STAT.put_nowait([
            'base',
            [
                'snmp_agent',
                STAT_LVL['op']
            ]
        ])

        log = 'SNMP agent listener started.'
        logger.info(log)
        print(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'INFO',
            log
        ])

        # Poll SNMP agent queues for values to update variables
        while True:
            if not MPQ_SNMPA_STOP.empty():
                MPQ_SNMPA_STOP.get()
                self.eng_snmp.transportDispatcher.closeDispatcher()
                break

            if not MPQ_SNMPA2.empty():
                mpq_record = MPQ_SNMPA2.get()
                self.base(mpq_record=mpq_record)

            if not MPQ_SNMPA3.empty():
                mpq_record = MPQ_SNMPA3.get()
                self.lane(mpq_record=mpq_record)

            if not MPQ_SNMPA4.empty():
                mpq_record = MPQ_SNMPA4.get()
                self.module(mpq_record=mpq_record)

            if not MPQ_SNMPA5.empty():
                mpq_record = MPQ_SNMPA5.get()
                self.sensor(mpq_record=mpq_record)

            time.sleep(0.1)

        MPQ_STAT.put_nowait([
            'snmp_agent',
            False
        ])
        log = 'SNMP agent dispatcher stopped.'
        logger.info(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'INFO',
            log
        ])

        log = 'SNMP agent listener stopped.'
        logger.info(log)
        print(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'INFO',
            log
        ])
        MPQ_STAT.put_nowait([
            'base',
            [
                'snmp_agent',
                STAT_LVL['not_cfg']
            ]
        ])

    def dispatcher(
        self
    ):
        # Register an imaginary never-ending job to keep I/O dispatcher running forever
        self.eng_snmp.transportDispatcher.jobStarted(1)

        # Run I/O dispatcher which would receive queries and send responses
        try:
            log = 'SNMP agent dispatcher started.'
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'INFO',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'snmp_agent',
                    STAT_LVL['op']
                ]
            ])
            self.eng_snmp.transportDispatcher.runDispatcher()

        except queue.Full:
            log = 'SNMP agent dispatcher experienced critical error.'
            logger.critical(log)
            print(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'snmp_agent',
                    STAT_LVL['crit']
                ]
            ])
            self.eng_snmp.tr0ansportDispatcher.closeDispatcher()
            raise

    def config_base(
        self
    ):
        """
        Configures base symbols and initial values
        """
        (
            entry,
            command_listener,
            couchdb,
            email,
            file,
            influxdb,
            interface,
            logging,
            network,
            poll_data,
            poll_dispatch,
            tasks
        ) = self.mib_builder.importSymbols(
            'JANUSESS-MIB',
            'baseEntry',
            'baseCommandListener',
            'baseCouchDB',
            'baseEmail',
            'baseFile',
            'baseInfluxDB',
            'baseInterface',
            'baseLogging',
            'baseNetwork',
            'basePollData',
            'basePollDispatch',
            'baseTasks'
        )
        self.sym_base = {
            'entry': entry,
            'command_listener': command_listener,
            'couchdb': couchdb,
            'email': email,
            'file': file,
            'influxdb': influxdb,
            'interface': interface,
            'logging': logging,
            'network': network,
            'poll_data': poll_data,
            'poll_dispatch': poll_dispatch,
            'tasks': tasks
        }
        self.mib_instr_base = self.ctx_snmp.getMibInstrum()
        sym_id_base = self.sym_base['entry'].getInstIdFromIndices(0)
        self.mib_instr_base.writeVars(
            (
                (
                    self.sym_base['command_listener'].name + sym_id_base,
                    STAT_LVL['not_cfg']
                ),
                (
                    self.sym_base['couchdb'].name + sym_id_base,
                    STAT_LVL['not_cfg']
                ),
                (
                    self.sym_base['email'].name + sym_id_base,
                    STAT_LVL['not_cfg']
                ),
                (
                    self.sym_base['file'].name + sym_id_base,
                    STAT_LVL['not_cfg']
                ),
                (
                    self.sym_base['influxdb'].name + sym_id_base,
                    STAT_LVL['not_cfg']
                ),
                (
                    self.sym_base['interface'].name + sym_id_base,
                    STAT_LVL['not_cfg']
                ),
                (
                    self.sym_base['logging'].name + sym_id_base,
                    STAT_LVL['not_cfg']
                ),
                (
                    self.sym_base['network'].name + sym_id_base,
                    STAT_LVL['not_cfg']
                ),
                (
                    self.sym_base['poll_data'].name + sym_id_base,
                    STAT_LVL['not_cfg']
                ),
                (
                    self.sym_base['poll_dispatch'].name + sym_id_base,
                    STAT_LVL['not_cfg']
                ),
                (
                    self.sym_base['tasks'].name + sym_id_base,
                    STAT_LVL['not_cfg']
                )
            )
        )

    def config_lane(
        self
    ):
        """
        Configures lane symbols and initial values
        """
        (
            entry,
            status,
            last_module,
            poll_status,
            poll_last_dtg
        ) = self.mib_builder.importSymbols(
            'JANUSESS-MIB',
            'laneEntry',
            'laneStatus',
            'laneLastModule',
            'lanePollStatus',
            'lanePollLastDTG'
        )

        self.sym_ln = {
            'entry': entry,
            'lane_status': status,
            'lane_last_module': last_module,
            'lane_poll_status': poll_status,
            'lane_poll_last_dtg': poll_last_dtg
        }
        self.mib_instr_lane = self.ctx_snmp.getMibInstrum()
        for addr_ln in range(0, 4):
            sym_id_ln = self.sym_ln['entry'].getInstIdFromIndices(addr_ln)
            self.mib_instr_lane.writeVars(
                (
                    (
                        self.sym_ln['lane_status'].name + sym_id_ln,
                        STAT_LVL['undeter']
                    ),
                    (
                        self.sym_ln['lane_last_module'].name + sym_id_ln,
                        -1
                    ),
                    (
                        self.sym_ln['lane_poll_status'].name + sym_id_ln,
                        STAT_LVL['undeter']
                    ),
                    (
                        self.sym_ln['lane_poll_last_dtg'].name + sym_id_ln,
                        '0'
                    )
                 )
            )

    def config_module(
        self
    ):
        """
        Configures module symbols and initial values
        """
        (
            entry,
            type_mod,
            version,
            location,
            status,
            num_sensors
        ) = self.mib_builder.importSymbols(
            'JANUSESS-MIB',
            'moduleEntry',
            'moduleType',
            'moduleVersion',
            'moduleLocation',
            'moduleStatus',
            'moduleNumberSensors'
        )
        self.sym_mod = {
            'entry': entry,
            'module_type': type_mod,
            'module_version': version,
            'module_location': location,
            'module_status': status,
            'module_num_sensors': num_sensors
        }
        self.mib_instr_module = self.ctx_snmp.getMibInstrum()
        for addr_ln in range(0, 4):
            for addr_mod in range(0, 127):
                sym_id_mod = self.sym_mod['entry'].getInstIdFromIndices(
                    addr_ln,
                    addr_mod
                )
                self.mib_instr_module.writeVars(
                    (
                        (
                            self.sym_mod['module_type'].name + sym_id_mod,
                            'Null'
                        ),
                        (
                            self.sym_mod['module_version'].name + sym_id_mod,
                            'Null'
                        ),
                        (
                            self.sym_mod['module_location'].name + sym_id_mod,
                            'Null'
                        ),
                        (
                            self.sym_mod['module_status'].name + sym_id_mod,
                            STAT_LVL['undeter']
                        ),
                        (
                            self.sym_mod['module_num_sensors'].name + sym_id_mod,
                            0
                        )
                    )
                )

    def config_sensor(
        self
    ):
        """
        Configures sensor symbols and initial values
        """
        (
            entry,
            descr,
            unit,
            value,
            alert_threshold,
            alert_type,
            poll_dtg
        ) = self.mib_builder.importSymbols(
            'JANUSESS-MIB',
            'sensorEntry',
            'sensorDescr',
            'sensorUnit',
            'sensorValue',
            'sensorAlertThreshold',
            'sensorAlertType',
            'sensorDTG'
        )
        self.sym_s = {
            'entry': entry,
            'sensor_descr': descr,
            'sensor_unit': unit,
            'sensor_value': value,
            'sensor_alert_threshold': alert_threshold,
            'sensor_alert_type': alert_type,
            'sensor_dtg': poll_dtg
        }
        self.mib_instr_sensor = self.ctx_snmp.getMibInstrum()
        for addr_ln in range(0, 4):
            for addr_mod in range(0, 127):
                for addr_s in range(0, 5):
                    sym_id_s = self.sym_s['entry'].getInstIdFromIndices(
                        addr_ln,
                        addr_mod,
                        addr_s
                    )
                    mib_instr = self.ctx_snmp.getMibInstrum()
                    mib_instr.writeVars(
                        (
                            (
                                self.sym_s['sensor_descr'].name + sym_id_s,
                                'Null'
                            ),
                            (
                                self.sym_s['sensor_unit'].name + sym_id_s,
                                'Null'
                            ),
                            (
                                self.sym_s['sensor_value'].name + sym_id_s,
                                0
                            ),
                            (
                                self.sym_s['sensor_alert_threshold'].name + sym_id_s,
                                0
                            ),
                            (
                                self.sym_s['sensor_alert_type'].name + sym_id_s,
                                0
                            ),
                            (
                                self.sym_s['sensor_dtg'].name + sym_id_s,
                                0
                            )
                        )
                    )

    @abc.abstractmethod
    def base(
        self,
        mpq_record: list
    ):
        """
        Updates base values

        :param mpq_record: base status list

        mpq_record[0] = process
        mpq_record[1] = process status
        """
        sym_id_base = self.sym_base['entry'].getInstIdFromIndices(0)

        # writeVars requires to fields to update, so enter record twice
        self.mib_instr_base.writeVars(
           (
               (
                   self.sym_base[mpq_record[0]].name + sym_id_base,
                   mpq_record[1]
               ),
               (
                   self.sym_base[mpq_record[0]].name + sym_id_base,
                   mpq_record[1])
           )
        )

    @abc.abstractmethod
    def lane(
        self,
        mpq_record: list
    ):
        """
        Updates lane values

        :param mpq_record: lane status list

        mpq_record[0] = lane address
        mpq_record[1] = lane status
        mpq_record[2] = last module
        mpq_record[3] = polling status
        mpq_record[4] = last poll dtg
        """
        sym_id_ln = self.sym_ln['entry'].getInstIdFromIndices(mpq_record[0])
        self.mib_instr_lane.writeVars(
            (
                (
                    self.sym_ln['lane_status'].name + sym_id_ln,
                    mpq_record[1]
                ),
                (
                    self.sym_ln['lane_last_module'].name + sym_id_ln,
                    mpq_record[2]
                ),
                (
                    self.sym_ln['lane_poll_status'].name + sym_id_ln,
                    mpq_record[3]
                ),
                (
                    self.sym_ln['lane_poll_last_dtg'].name + sym_id_ln,
                    mpq_record[4]
                )
            )
        )

    @abc.abstractmethod
    def module(
        self,
        mpq_record: list
    ):
        """
        Updates module values

        :param mpq_record: module status list

        mpq_record[0] = lane address
        mpq_record[1] = module address
        mpq_record[2] = module type
        mpq_record[3] = module version
        mpq_record[4] = module location
        mpq_record[5] = module status
        mpq_record[6] = number sensors
        """
        sym_id_mod = self.sym_mod['entry'].getInstIdFromIndices(
            mpq_record[0],
            mpq_record[1]
        )

        self.mib_instr_module.writeVars(
            (
                (
                    self.sym_mod['module_type'].name + sym_id_mod,
                    mpq_record[2]
                ),
                (
                    self.sym_mod['module_version'].name + sym_id_mod,
                    mpq_record[3]
                ),
                (
                    self.sym_mod['module_location'].name + sym_id_mod,
                    mpq_record[4]
                ),
                (
                    self.sym_mod['module_status'].name + sym_id_mod,
                    mpq_record[5]
                ),
                (
                    self.sym_mod['module_num_sensors'].name + sym_id_mod,
                    mpq_record[6]
                )
             )
        )

    @abc.abstractmethod
    def sensor(
        self,
        mpq_record: list
    ):
        """
        Updates sensor values

        :param mpq_record: sensor status list

        mpq_record[0] = module id
        mpq_record[1] = lane address
        mpq_record[2] = module address
        mpq_record[3] = sensor address
        mpq_record[4] = sensor type
        mpq_record[5] = sensor value
        mpq_record[6] = sensor value unit
        mpq_record[7] = sensor value dtg
        mpq_record[8] = alert type
        mpq_record[9] = trigger
        """
        # writeVars requires to fields to update, so enter record twice
        sym_id_s = self.sym_s['entry'].getInstIdFromIndices(
            mpq_record[1],
            mpq_record[2],
            mpq_record[3]
        )
        if mpq_record[8] == 'low':
            alert_type = 1

        elif mpq_record[8] == 'high':
            alert_type = 2

        else:
            alert_type = 0

        mib_instr = self.ctx_snmp.getMibInstrum()

        mib_instr.writeVars(
            (
                (
                    self.sym_s['sensor_descr'].name + sym_id_s,
                    mpq_record[4]
                ),
                (
                    self.sym_s['sensor_unit'].name + sym_id_s,
                    mpq_record[6]
                ),
                (
                    self.sym_s['sensor_value'].name + sym_id_s,
                    mpq_record[5]
                ),
                (
                    self.sym_s['sensor_alert_threshold'].name + sym_id_s,
                    mpq_record[9]
                ),
                (
                    self.sym_s['sensor_alert_type'].name + sym_id_s,
                    alert_type
                ),
                (
                    self.sym_s['sensor_dtg'].name + sym_id_s,
                    mpq_record[7]
                )
            )
        )
