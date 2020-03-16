import logging
import requests
import struct
import time
from curses.ascii import isprint
from datetime import datetime
from interface.led import Control
from interface.memorymap import MMAP
from shared import dbase
from shared.messaging.smtp import send_mail
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT, TYPE_INTERFACE, MPQ_POLL_START, MPQ_POLL_STOP, \
    MPQ_POLL_COMPLETE, MPQ_POLL_LOG_DISP, MPQ_POLL_LOG_DATA, MPQ_CMD5

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'polling'
logger = logging.getLogger(logfile)


def dispatcher():
    """
    Automatically dispatches polling commands into MPQ_CMD5 priority queue
    """
    stat_cdb = STAT_LVL['op']
    stat_cdb_prev = STAT_LVL['not_cfg']

    cfg_poll = [
        STAT_LVL['not_cfg'],
        STAT_LVL['not_cfg'],
        STAT_LVL['not_cfg'],
        STAT_LVL['not_cfg']
    ]

    while not stat_cdb:
        # Cycle through all lanes
        for addr_ln in range(0, 4):

            # Change logging level since this operates in multiprocess
            # Cycle to last entry for most current log setting
            while not MPQ_POLL_LOG_DISP.empty():
                mpq_record = MPQ_POLL_LOG_DISP.get()
                if mpq_record[0] == 'DEBUG':
                    logger.setLevel(logging.DEBUG)
                elif mpq_record[0] == 'INFO':
                    logger.setLevel(logging.INFO)
                elif mpq_record[0] == 'ERROR':
                    logger.setLevel(logging.ERROR)
                elif mpq_record[0] == 'WARNING':
                    logger.setLevel(logging.WARNING)
                elif mpq_record[0] == 'CRITICAL':
                    logger.setLevel(logging.CRITICAL)

            # Set polling status flag for this lane if start command is issued
            # on MPQ_POLL_START
            if not MPQ_POLL_START.empty():
                mpq_record = MPQ_POLL_START.get()
                cfg_poll[mpq_record[0]] = STAT_LVL['op']

                MPQ_STAT.put_nowait([
                    'lane',
                    [
                        mpq_record[0],
                        {'poll': cfg_poll[mpq_record[0]]}
                    ]
                ])

                # Send polling start messaging with timeout in seconds
                send_mail(
                    msg_type='poll_start',
                    args=[mpq_record[0]],
                )

            # If polling status flag is set, execute polling for lane
            if not cfg_poll[addr_ln]:

                # Get lane_status document from CouchDB lanes database
                data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
                    cdb_cmd='get_doc',
                    cdb_name='lanes',
                    cdb_doc='lane{0}_status'.format(addr_ln),
                    logfile=logfile
                )

                # Check that both lane status and polling have not failed
                if (not stat0_cdb) and (data0_cdb_out['status'] < STAT_LVL['crit']) and \
                        (data0_cdb_out['poll'] < STAT_LVL['crit']):

                    # Get stat_lane view from CouchDB modconfig database
                    data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
                        cdb_cmd='get_view',
                        cdb_name='modconfig',
                        cdb_doc='stat_lane{0}'.format(addr_ln),
                        logfile=logfile
                    )

                    if not stat1_cdb:

                        # Cycle through all modules connected to lane
                        # If a module has not failed, initiate polling actions
                        for dict_mod in data1_cdb_out:
                            if dict_mod['value']['status'] < STAT_LVL['crit']:

                                # Developer code to check for speed
                                print('priority 5 interface added')
                                time_m = time.time()

                                # Immediate stop polling for this lane
                                # if stop command is issued on MPQ_POLL_STOP
                                if not MPQ_POLL_STOP.empty():
                                    mpq_record = MPQ_POLL_STOP.get()
                                    cfg_poll[mpq_record] = STAT_LVL['not_cfg']

                                    log = 'Lane {0} polling exit command executed.'. \
                                          format(mpq_record)
                                    logger.info(log)
                                    MPQ_ACT.put_nowait([
                                        datetime.now().isoformat(' '),
                                        'INFO',
                                        log
                                    ])
                                    MPQ_STAT.put_nowait([
                                        'lane',
                                        [
                                            mpq_record,
                                            {'poll': cfg_poll[mpq_record]}
                                        ]
                                    ])

                                    # Send polling stop messaging with timeout in seconds
                                    send_mail(
                                        msg_type='poll_stop',
                                        args=[mpq_record],
                                    )

                                    if mpq_record == addr_ln:
                                        break

                                # Issue request to poll this module
                                MPQ_CMD5.put([
                                    dict_mod['id'],
                                    addr_ln,
                                    dict_mod['key']
                                ])

                                # Immediate stop polling for this lane
                                # if stop command is issued on MPQ_POLL_STOP.
                                # Second check ensures quicker response time.
                                if not MPQ_POLL_STOP.empty():
                                    mpq_record = MPQ_POLL_STOP.get()
                                    cfg_poll[mpq_record] = STAT_LVL['not_cfg']

                                    log = 'Lane {0} polling exit command executed.'.format(mpq_record)
                                    logger.info(log)
                                    MPQ_ACT.put_nowait([
                                        datetime.now().isoformat(' '),
                                        'INFO',
                                        log
                                    ])
                                    MPQ_STAT.put_nowait([
                                        'lane',
                                        [
                                            mpq_record,
                                            {'poll': cfg_poll[mpq_record]}
                                        ]
                                    ])

                                    # Send polling stop messaging with timeout in seconds
                                    send_mail(
                                        msg_type='poll_stop',
                                        args=[mpq_record],
                                    )

                                    if mpq_record == addr_ln:
                                        break

                                log = 'Lane {0} module {1} poll added to job queue.'. \
                                    format(addr_ln, dict_mod['key'])
                                logger.info(log)
                                MPQ_ACT.put_nowait([
                                    datetime.now().isoformat(' '),
                                    'DEBUG',
                                    log
                                ])

                                # Determine if all module sensor data processing is
                                # complete prior to proceeding.  This pause is here
                                # to prevent the poll dispatcher from getting too far
                                # ahead of module sensor data processing.
                                while True:
                                    if not MPQ_POLL_COMPLETE.empty():
                                        mpq_record = MPQ_POLL_COMPLETE.get()
                                        if (mpq_record[0] == addr_ln) and \
                                                (mpq_record[1] == dict_mod['key']):
                                            log = 'Lane {0} module {1} automated poll completed.'.\
                                                  format(addr_ln, dict_mod['key'])
                                            logger.info(log)
                                            MPQ_ACT.put_nowait([
                                                datetime.now().isoformat(' '),
                                                'INFO',
                                                log
                                            ])
                                            break
                                    time.sleep(0.02)

                                # Developer code to check for speed
                                print('Module {0} cycle complete: {1}'.
                                      format(dict_mod['key'], round((time.time() - time_m), 3)))

                                log = 'Lane {0} module {1} poll dispatch cycle complete.'. \
                                      format(addr_ln, dict_mod['key'])
                                logger.info(log)
                                MPQ_ACT.put_nowait([
                                    datetime.now().isoformat(' '),
                                    'DEBUG',
                                    log
                                ])

                    else:
                        stat_cdb = stat1_cdb

                    last_dtg = time.strftime(
                        '%Y-%m-%d %H:%M:%S',
                        time.localtime(time.time())
                    )
                    MPQ_STAT.put_nowait([
                        'lane',
                        [
                            addr_ln,
                            {'last_dtg': last_dtg}
                        ]
                    ])
                    time.sleep(15)

                else:
                    stat_cdb = stat0_cdb

            time.sleep(1)
            # Determine any changes in CouchDB status and report for both
            # CouchDB and poll dispatcher.  CouchDB is only cause for change in
            # poll_dispatcher status
            if stat_cdb != stat_cdb_prev:
                stat_cdb_prev = stat_cdb
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
                        'poll_dispatch',
                        stat_cdb
                    ]
                ])

    log = 'Polling dispatcher failed due to CouchDB error.'
    logger.critical(log)
    MPQ_ACT.put_nowait([
        datetime.now().isoformat(' '),
        'CRITICAL',
        log
    ])


def get_data(
    obj_iface: TYPE_INTERFACE,
    uid_mod: str,
    addr_ln: int,
    addr_mod: int
):
    """
    Retrieves and publishes module sensor data

    :param obj_iface: Interface Object
    :param uid_mod: str
    :param addr_ln: int
    :param addr_mod: int
    """
    # Change logging level since this operates in multiprocess
    # Cycle to last entry for most current log setting
    while not MPQ_POLL_LOG_DATA.empty():
        mpq_record = MPQ_POLL_LOG_DATA.get()
        if mpq_record[0] == 'DEBUG':
            logger.setLevel(logging.DEBUG)
        elif mpq_record[0] == 'INFO':
            logger.setLevel(logging.INFO)
        elif mpq_record[0] == 'ERROR':
            logger.setLevel(logging.ERROR)
        elif mpq_record[0] == 'WARNING':
            logger.setLevel(logging.WARNING)
        elif mpq_record[0] == 'CRITICAL':
            logger.setLevel(logging.CRITICAL)

    time_a = time.time()
    log = 'Retrieving lane {0} module {1} id {2} data.'.format(addr_ln, addr_mod, uid_mod)
    logger.info(log)

    stat_poll_data = STAT_LVL['op']
    uid_mod_i2c = ''
    uid_mod_i2c_print = ''

    # Retrieve memory map version of module with I2C address of 0x7F.
    # If module responds, proceed to module setup actions, otherwise
    # mod_last_found flag is set.
    high_mmap = len(MMAP) - 1
    addr_mem = MMAP[high_mmap]['M_CFG_ALL'][0]
    data_len = MMAP[high_mmap]['M_CFG_ALL'][1]
    data0_iface_out, stat0_iface = obj_iface.i2c_read(
        addr_ln=addr_ln,
        addr_mod=addr_mod,
        addr_mem=addr_mem,
        data_len=data_len,
        stat_en=False
    )
    print('RAW POLL DATA: {0}'.format(data0_iface_out))
    print('Lane {0} module {1} get_data i2c config time: {2}'.
          format(addr_ln, addr_mod, round((time.time() - time_a), 3)))
    if stat0_iface:
        log = 'Lane {0} module {1} poll can '.format(addr_ln, addr_mod) + \
              'not be completed due to I2C interface error.'
        logger.critical(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'CRITICAL',
            log
        ])
        print(log)
        MPQ_STAT.put_nowait([
            'base',
            [
                'poll_data',
                STAT_LVL['op_err']
            ]
        ])
        MPQ_STAT.put_nowait([
            'module',
            [
                uid_mod,
                addr_ln,
                addr_mod,
                STAT_LVL['op_err']
            ]
        ])
        stat_poll_data = STAT_LVL['op_err']

    else:
        # Build module id string from I2C data
        mod_uid_end = MMAP[data0_iface_out[2]]['M_UID'][0] + \
                      MMAP[data0_iface_out[2]]['M_UID'][1] - 1
        mod_uid_begin = MMAP[data0_iface_out[2]]['M_UID'][0] - 1
        for addr_mem in range(mod_uid_end, mod_uid_begin, -1):
            uidmod_i2c = str(hex(data0_iface_out[addr_mem]))[2:]
            if len(uidmod_i2c) == 1:
                uidmod_i2c = '0' + uidmod_i2c
            uid_mod_i2c += uidmod_i2c

        # Check that module ids match, then proceed with data collection and reporting
        uid_mod_print = ''.join(char for char in uid_mod.strip() if isprint(char))
        uid_mod_i2c_print = ''.join(char for char in uid_mod_i2c.strip() if isprint(char))
        if uid_mod_i2c_print == uid_mod_print:

            time_b = time.time()
            # Get module document from CouchDB modconfig database
            data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
                cdb_cmd='get_doc',
                cdb_name='modconfig',
                cdb_doc=uid_mod_print,
                logfile=logfile
            )

            # Get cloud document from CouchDB config database
            data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
                cdb_cmd='get_doc',
                cdb_name='config',
                cdb_doc='cloud',
                logfile=logfile
            )

            # Get core document from CouchDB config database
            data2_cdb_out, stat2_cdb, http2_cdb = dbase.cdb_request(
                cdb_cmd='get_doc',
                cdb_name='config',
                cdb_doc='core',
                logfile=logfile
            )
            print(
                'Lane {0} module {1} get_data database time: {2}'.
                format(addr_ln, addr_mod, round((time.time() - time_b), 3)))
            if not stat0_cdb and not stat1_cdb and not stat2_cdb:
                module_stat = STAT_LVL['op']

                poll_data_mod = []
                poll_head_mod = [
                    uid_mod_i2c_print,
                    data2_cdb_out['customer'],
                    data2_cdb_out['name'],
                    data0_cdb_out['loc'],
                    addr_ln,
                    addr_mod,
                ]

                # Retrieves sensor polling value from module
                time_c = time.time()
                data_iface_out, stat_iface = obj_iface.i2c_read(
                    addr_ln=addr_ln,
                    addr_mod=addr_mod,
                    addr_mem=MMAP[data0_iface_out[2]]['S_ALL_VAL'][0],
                    data_len=MMAP[data0_iface_out[2]]['S_ALL_VAL'][1]
                )
                print('Lane {0} module {1} get_data i2c sensor time: {2}'.
                      format(addr_ln, addr_mod, round((time.time() - time_c), 3)))
                print(data_iface_out)
                if not stat_iface:

                    # Cycle through all sensors installed on the module
                    led_ctl = Control()
                    for addr_s in range(0, int(data0_cdb_out['num_sensors'])):
                        sensor = 'S{0}'.format(addr_s)

                        log = 'Retrieving lane {0} module {1} sensor {2} data.'.\
                              format(addr_ln, addr_mod, addr_s)
                        logger.debug(log)

                        # Initialize polling data packet
                        data_dtg = time.time()
                        poll_data_s = [addr_s]

                        # Convert raw values to floating point number, and add to packet
                        val_raw = struct.pack(
                            'BBBB',
                            int(data_iface_out[3 + (addr_s * 4)]),
                            int(data_iface_out[2 + (addr_s * 4)]),
                            int(data_iface_out[1 + (addr_s * 4)]),
                            int(data_iface_out[0 + (addr_s * 4)])
                        )
                        val_convert = round(
                            struct.unpack('>f', val_raw)[0],
                            data0_cdb_out[sensor]['precision']
                        )

                        if (val_convert >= data0_cdb_out[sensor]['min']) or \
                                (val_convert <= data0_cdb_out[sensor]['max']):

                            trig_low = round(
                                float(data0_cdb_out[sensor]['trig_low']),
                                data0_cdb_out[sensor]['precision']
                            )
                            trig_high = round(
                                float(data0_cdb_out[sensor]['trig_high']),
                                data0_cdb_out[sensor]['precision']
                            )

                            # Determine triggers
                            if val_convert < trig_low:
                                poll_data_s.append('low')
                                poll_data_s.append(True)
                                trigger = trig_low
                                module_stat = STAT_LVL['s_evt']
                                led_ctl.effect(
                                    'sensor_low',
                                    uid_mod_print,
                                    addr_ln,
                                    addr_mod
                                )

                            elif val_convert > trig_high:
                                poll_data_s.append('high')
                                poll_data_s.append(True)
                                trigger = trig_high
                                module_stat = STAT_LVL['s_evt']
                                led_ctl.effect(
                                    'sensor_high',
                                    uid_mod_print,
                                    addr_ln,
                                    addr_mod
                                )

                            else:
                                poll_data_s.append('off')
                                poll_data_s.append(False)
                                trigger = 0.0

                            poll_data_s.append(data0_cdb_out[sensor]['type'])
                            poll_data_s.append(val_convert)
                            poll_data_s.append(data_dtg)
                            poll_data_s.append(data0_cdb_out[sensor]['unit'])
                            poll_data_s.append(trigger)
                            poll_data_s.append(data0_cdb_out[sensor]['trig_int'])
                            poll_data_s.append(data0_cdb_out[sensor]['trig_step'])

                            poll_data_mod.append(poll_data_s)
                            MPQ_STAT.put_nowait([
                                'poll',
                                [
                                    poll_head_mod,
                                    poll_data_s
                                ]
                            ])

                    time_e = time.time()
                    store_data(data1_cdb_out, poll_head_mod, poll_data_mod)
                    print('Lane {0} module {1} get_data store data time: {2}'.
                          format(addr_ln, addr_mod, round((time.time() - time_e), 3)))

                else:
                    log = 'Lane {0} module {1} '.format(addr_ln, addr_mod) + \
                          'data not added to storage queue due to I2C errors.'
                    logger.critical(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'CRITICAL',
                        log
                    ])
                    stat_poll_data = STAT_LVL['op_err']
                    module_stat = STAT_LVL['op_err']

            else:
                log = 'Lane {0} module {1} '.format(addr_ln, addr_mod) + \
                      'data not added to storage queue due to CouchDB errors.'
                logger.critical(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'CRITICAL',
                    log
                ])
                stat_poll_data = STAT_LVL['op_err']
                module_stat = STAT_LVL['op_err']

            log = 'Completed lane {0} module {1} poll.'.format(addr_ln, addr_mod)
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'DEBUG',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'poll_data',
                    stat_poll_data
                ]
            ])

            MPQ_STAT.put_nowait([
                'module',
                [
                    uid_mod_print,
                    addr_ln,
                    addr_mod,
                    module_stat
                ]
            ])

        else:
            stat_poll_data = STAT_LVL['op_err']
            log = 'Lane {0} module {1} poll can '.format(addr_ln, addr_mod) + \
                  'not be completed due to mismatch in module id: ' + \
                  'requested={0} vs polled={1}.'.format(uid_mod_print, uid_mod_i2c_print)

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
                    'poll_data',
                    stat_poll_data
                ]
            ])
            MPQ_STAT.put_nowait([
                'module',
                [
                    uid_mod_print,
                    addr_ln,
                    addr_mod,
                    STAT_LVL['op_err']
                ]
            ])

    return stat_poll_data, uid_mod_i2c_print


def store_data(
    cloud: dict,
    poll_head: list,
    poll_data: list
):
    """
    Stores module poll data in CouchDB

    :param cloud: dict
    :param poll_head: list
    :param poll_data: list
    """
    loc_mod = poll_head[3]
    loc_mod = loc_mod.replace(' ', '\ ')
    loc_mod = loc_mod.replace(',\ ', '\,\ ')
    addr_ln = poll_head[4]
    addr_mod = poll_head[5]

    data_idb_in = ''
    data_idb_in_head = '{0},'.format(str(poll_head[0])) + \
        'customer={0},'.format(poll_head[1]) + \
        'base={0},'.format(poll_head[2]) + \
        'location={0},'.format(loc_mod) + \
        'lane={0},'.format(poll_head[4]) + \
        'module={0},'.format(poll_head[5])

    for poll_data_s in poll_data:
        s_type = poll_data_s[3]
        s_type = s_type.replace(' ', '\ ')
        s_type = s_type.replace(',\ ', '\,\ ')

        data_idb_in = data_idb_in + data_idb_in_head + \
            'sensor={0},'.format(poll_data_s[0]) + \
            'alert_type={0},'.format(poll_data_s[1]) + \
            'alert={0} '.format(poll_data_s[2]) + \
            '{0}={1} '.format(s_type, str(poll_data_s[4])) + \
            '{0}'.format(int(poll_data_s[5] * 1000000000)) +\
            "\n"

    # Store data packet to local InfluxDB JanusESS database
    try:
        http0_resp = requests.post(
            'http://localhost:8086/write?db=JanusESS',
            headers={'Content-type': 'application/octet-stream'},
            data=data_idb_in,
            timeout=2.0  # Set higher for portability to rPi v3
        )

        # Returns HTTP status codes
        if http0_resp.status_code == 204:
            log = 'Uploaded of lane {0} module {1} '.format(addr_ln, addr_mod) +\
                  'data to local InfluxDB server successful.'
            logger.debug(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'DEBUG',
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
            log = 'Could not upload lane {0} module {1} '.format(addr_ln, addr_mod) + \
                  'data to local InfluxDB server due to query error.'
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

    except requests.exceptions.ConnectionError:
        log = 'Local InfluxDB server did not respond to request.'
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
                'influxdb',
                STAT_LVL['crit']
            ]
        ])

    except requests.exceptions.ReadTimeout:
        log = 'Local InfluxDB server timed out on request.'
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
                'influxdb',
                STAT_LVL['op_err']
            ]
        ])

    # If cloud storage is enabled, store data to cloud InfluxDB JanusESS database
    if cloud['enable']:

        # Store data packet to cloud InfluxDB JanusESS database
        server = 'http://' + cloud['url'] + ':8086/write?db=JanusESS'
        try:
            http1_resp = requests.post(
                server,
                headers={'Content-type': 'application/octet-stream'},
                data=data_idb_in,
                timeout=1
            )

            # Returns HTTP status codes
            if http1_resp.status_code == 204:
                log = 'Uploaded of lane {0} module {1} '.format(addr_ln, addr_mod) + \
                      'data to remote InfluxDB server {0} successful.'.format(cloud['url'])
                logger.debug(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'DEBUG',
                    log
                ])

            else:
                log = 'Could not upload lane {0} module {1} '.format(addr_ln, addr_mod) + \
                      'data to remote InfluxDB server due to query error.'
                logger.warning(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'WARNING',
                    log
                ])

        except requests.exceptions.ConnectionError:
            log = 'Remote InfluxDB server {0} did not respond to request.'.format(cloud['url'])
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])

        except requests.exceptions.ReadTimeout:
            log = 'Remote InfluxDB server {0} timed out on request.'.format(cloud['url'])
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])

    log = 'Completed storage of lane {0} module {1} data.'.format(addr_ln, addr_mod)
    logger.info(log)
