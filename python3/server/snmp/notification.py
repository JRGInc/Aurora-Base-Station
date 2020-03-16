import logging
import time
from datetime import datetime
from pysnmp.hlapi import *
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT, MPQ_SNMPN2, MPQ_SNMPN3, MPQ_SNMPN4, MPQ_SNMPN5, MPQ_SNMPN_STOP

logfile = 'server'
logger = logging.getLogger(logfile)


class SNMPNotify(
    object
):
    """
    SNMP Notifier

    This class operates an SNMP notifier independently from any SNMP services loaded
    and executed by the operating system.  To prevent conflicts it may be best to
    disable operating system-based SNMP services.
    """

    def __init__(
        self,
        host_ip: str,
        host_port: int,
        host_community: str
    ):
        """
        Retrieves and publishes module sensor data

        :param host_ip: str
        :param host_port: int
        :param host_community: str
        """
        self.host_ip = host_ip
        self.host_port = host_port
        self.host_community = host_community

    def listener(
        self
    ):
        """
        Listens for notification activity and assigns to appropriate process
        """
        log = 'SNMP notification listener started.'
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
                'snmp_notify',
                STAT_LVL['op']
            ]
        ])

        # Poll SNMP agent queues for values to update variables
        while True:
            if not MPQ_SNMPN_STOP.empty():
                MPQ_SNMPN_STOP.get()
                break

            if not MPQ_SNMPN2.empty():
                mpq_record = MPQ_SNMPN2.get()
                self.base(mpq_record=mpq_record)

            if not MPQ_SNMPN3.empty():
                mpq_record = MPQ_SNMPN3.get()
                self.lane(mpq_record=mpq_record)

            if not MPQ_SNMPN4.empty():
                mpq_record = MPQ_SNMPN4.get()
                self.module(mpq_record=mpq_record)

            if not MPQ_SNMPN5.empty():
                mpq_record = MPQ_SNMPN5.get()
                self.poll_val(mpq_record=mpq_record)

            time.sleep(0.1)

        MPQ_STAT.put_nowait([
            'snmp_notify',
            False
        ])

        log = 'SNMP notification listener stopped.'
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
                'snmp_notify',
                STAT_LVL['not_cfg']
            ]
        ])

    def notify(
        self,
        mib_identity: str,
        mib_object: dict,
        notify_msg: dict
    ):
        """
        Dispatches prebuilt mib object

        :param mib_identity: str
        :param mib_object: dict
        :param notify_msg: dict
        """
        log = notify_msg['start']
        logger.debug(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'INFO',
            log
        ])

        error_indication, error_status, error_index, var_binds = next(
            sendNotification(
                SnmpEngine(),
                CommunityData(self.host_community),
                UdpTransportTarget((
                    self.host_ip,
                    self.host_port
                )),
                ContextData(),
                'inform',
                NotificationType(
                    ObjectIdentity(
                        'JANUSESS-MIB',
                        mib_identity + 'Notify'
                    ).
                    addMibSource('/opt/Janus/ESS/python3/server/snmp/mibs'),
                    objects=mib_object
                )
            )
        )

        if error_indication:
            log = notify_msg['error'] + str(error_indication)
            logger.warning(log)
            print(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'snmp_notify',
                    STAT_LVL['op_err']
                ]
            ])

        else:
            log = notify_msg['end']
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
                    'snmp_notify',
                    STAT_LVL['op']
                ]
            ])

    def base(
        self,
        mpq_record: list
    ):
        """
        Prepares base status for notification trap

        mpq_record[0] = process
        mpq_record[1] = process status

        :param mpq_record: list
        """
        if mpq_record[1]:
            mib_identity = 'baseProcess'
            msg_append = [
                ' is operational with no errors',
                ' experienced operational events',
                ' experienced operational errors',
                ' experienced critical errors',
                ' is not setup/running',
                ' experienced configuration errors',
                ' has undetermined status',
                ' is not tracked',
            ]
            msg = mpq_record[0] + msg_append[mpq_record[1]]

            notify_msg = {
                'start': 'SNMP base {0} trap notification sequence started'.
                         format(mpq_record[0]),
                'error': 'SNMP base {0} trap notification error: '.
                         format(mpq_record[0]),
                'end': 'SNMP base {0} trap notification sequence completed'.
                       format(mpq_record[0])
            }

            mib_object = {
                ('JANUSESS-MIB', mib_identity): mpq_record[1],
                ('JANUSESS-MIB', 'notifyMessage'): msg
            }

            self.notify(
                mib_identity=mib_identity,
                mib_object=mib_object,
                notify_msg=notify_msg
            )

    def lane(
        self,
        mpq_record: list
    ):
        """
        Prepares lane status for notification trap

        mpq_record[0] = lane address
        mpq_record[1] = lane status
        mpq_record[2] = last module
        mpq_record[3] = polling status
        mpq_record[4] = last poll dtg

        :param mpq_record: list
        """
        mib_identity = 'laneStatus'
        msg_append = [
            ' is operational with no errors',
            ' experienced operational events',
            ' experienced operational errors',
            ' experienced critical errors',
            ' is not setup/running',
            ' experienced configuration errors',
            ' has undetermined status',
            ' is not tracked',
        ]

        # Two notifications may be issued: bad lane status and bad polling status
        if mpq_record[1]:
            msg = 'Lane {0}'.format(mpq_record[0]) + msg_append[mpq_record[1]]
            mib_object = {
                ('JANUSESS-MIB', 'laneStatus'): mpq_record[1],
                ('JANUSESS-MIB', 'laneLastModule'): mpq_record[2],
                ('JANUSESS-MIB', 'lanePollStatus'): mpq_record[3],
                ('JANUSESS-MIB', 'lanePollLastDTG'): mpq_record[4],
                ('JANUSESS-MIB', 'notifyMessage'): msg
            }

            notify_msg = {
                'start': 'SNMP lane {0} trap notification sequence started'.
                         format(mpq_record[0]),
                'error': 'SNMP lane {0} trap notification error: '.
                         format(mpq_record[0]),
                'end': 'SNMP lane {0} trap notification sequence completed'.
                       format(mpq_record[0])
            }

            self.notify(
                mib_identity=mib_identity,
                mib_object=mib_object,
                notify_msg=notify_msg
            )

        if mpq_record[3]:
            msg = 'Lane {0} polling'.format(mpq_record[0]) + msg_append[mpq_record[3]]
            mib_object = {
                ('JANUSESS-MIB', 'laneStatus'): mpq_record[1],
                ('JANUSESS-MIB', 'laneLastModule'): mpq_record[2],
                ('JANUSESS-MIB', 'lanePollStatus'): mpq_record[3],
                ('JANUSESS-MIB', 'lanePollLastDTG'): mpq_record[4],
                ('JANUSESS-MIB', 'notifyMessage'): msg
            }

            notify_msg = {
                'start': 'SNMP lane {0} trap notification sequence started'.
                         format(mpq_record[0]),
                'error': 'SNMP lane {0} trap notification error: '.
                         format(mpq_record[0]),
                'end': 'SNMP lane {0} trap notification sequence completed'.
                       format(mpq_record[0])
            }

            self.notify(
                mib_identity=mib_identity,
                mib_object=mib_object,
                notify_msg=notify_msg
            )

    def module(
        self,
        mpq_record: list
    ):
        """
        Prepares module status for notification trap

        mpq_record[0] = lane address
        mpq_record[1] = module address
        mpq_record[2] = module type
        mpq_record[3] = module version
        mpq_record[4] = module location
        mpq_record[5] = module status
        mpq_record[6] = number sensors

        :param mpq_record: list
        """
        if mpq_record[5]:

            mib_identity = 'moduleStatus'
            msg_append = [
                ' is operational with no errors',
                ' experienced operational events',
                ' experienced operational errors',
                ' experienced critical errors',
                ' is not setup/running',
                ' experienced configuration errors',
                ' has undetermined status',
                ' is not tracked',
            ]
            msg = 'Link ' + str(mpq_record[0]) + ' module ' + str(mpq_record[1]) + \
                  msg_append[mpq_record[5]]

            notify_msg = {
                'start': 'SNMP lane {0} module {1} '.format(mpq_record[0], mpq_record[1]) +
                         'trap notification sequence started',
                'error': 'SNMP lane {0} module {1} '.format(mpq_record[0], mpq_record[1]) +
                         'trap notification error: ',
                'end': 'SNMP lane {0} module {1} '.format(mpq_record[0], mpq_record[1]) +
                       'trap notification sequence completed'
            }

            mib_object = {
                ('JANUSESS-MIB', 'moduleLocation'): mpq_record[4],
                ('JANUSESS-MIB', 'moduleType'): mpq_record[2],
                ('JANUSESS-MIB', 'moduleVersion'): mpq_record[3],
                ('JANUSESS-MIB', 'moduleNumberSensors'): mpq_record[6],
                ('JANUSESS-MIB', 'moduleStatus'): mpq_record[2],
                ('JANUSESS-MIB', 'notifyMessage'): msg
            }

            self.notify(
                mib_identity=mib_identity,
                mib_object=mib_object,
                notify_msg=notify_msg
            )

    def poll_val(
        self,
        mpq_record: list
    ):
        """
        Prepares poll value for notification trap

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

        :param mpq_record: list
        """

        # TODO: Add missing fields to record and remove CouchDB request
        mib_process = False
        msg = None

        if mpq_record[8] == 'low':
            msg = 'The value equals or exceeded the lower threshold.'
            mib_process = 1

        # Sensor value is greater than upper trigger
        elif mpq_record[8] == 'high':
            msg = 'The value equals or exceeded the upper threshold.'
            mib_process = 2

        if mib_process:
            mib_identity = 'sensorAlert'

            notify_msg = {
                'start': 'SNMP lane {0} module {1} '.format(mpq_record[1], mpq_record[2]) +
                         'sensor {0} poll value trap notification sequence started'.
                         format(mpq_record[3]),
                'error': 'SNMP lane {0} module {1} '.format(mpq_record[1], mpq_record[2]) +
                         'sensor {0} poll value trap notification error: '.format(mpq_record[3]),
                'end': 'SNMP lane {0} module {1} '.format(mpq_record[1], mpq_record[2]) +
                       'sensor {0} poll value trap notification sequence completed'.
                       format(mpq_record[3])
            }

            val_s_parts = str(float(mpq_record[5])).split('.')

            # The JANUSESS-MIB only allows single decimal place
            if len(val_s_parts[1]) >= 2:
                val_s_parts[1] = float(val_s_parts[1]) / pow(10, len(val_s_parts[1]))

            val_s = val_s_parts[0] + str(val_s_parts[1])

            # Sensor trigger processing
            val_trig_parts = str(float(mpq_record[9])).split('.')

            # The JANUSESS-MIB only allows single decimal place
            if len(val_trig_parts[1]) >= 2:
                val_trig_parts[1] = float(val_trig_parts[1]) / pow(10, len(val_trig_parts[1]))
            val_trig = val_trig_parts[0] + str(val_trig_parts[1])

            if mpq_record[6] is None:
                mpq_record[6] = 'No Unit'

            mib_object = {
                ('JANUSESS-MIB', 'sensorAlertType'): mib_process,
                ('JANUSESS-MIB', 'sensorValue'): val_s,
                ('JANUSESS-MIB', 'sensorAlertThreshold'): val_trig,
                ('JANUSESS-MIB', 'sensorUnit'): mpq_record[6],
                ('JANUSESS-MIB', 'sensorDescr'): mpq_record[4],
                ('JANUSESS-MIB', 'sensorDTG'): mpq_record[7],
                ('JANUSESS-MIB', 'notifyMessage'): msg
            }

            self.notify(
                mib_identity=mib_identity,
                mib_object=mib_object,
                notify_msg=notify_msg
            )
