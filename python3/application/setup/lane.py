import logging
import time
from application.setup import module
from datetime import datetime
from interface.memorymap import MMAP
from shared import dbase
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT, TYPE_INTERFACE, MPQ_SETUP_LOG_RESET, MPQ_SETUP_LOG_INIT

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'setup'
logger = logging.getLogger(logfile)


def reset(
    obj_iface: TYPE_INTERFACE,
    addr_ln: int
):
    """
    Resets lane

    :param obj_iface: Interface Object
    :param addr_ln: int

    :return stat_iface: STAT_LVL['op'] or STAT_LVL['crit']
    """
    # Change logging level since this operates in multiprocess
    # Cycle to last entry for most current log setting
    while not MPQ_SETUP_LOG_RESET.empty():
        mpq_record = MPQ_SETUP_LOG_RESET.get()
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

    # Write HIGH value to lane GPIO pin
    # Hold HIGH for 50 milliseconds
    stat_iface = obj_iface.gpio_write(
        addr_ln=addr_ln,
        data_iface_in=1,
        stat_en=False
    )
    time.sleep(0.050)

    # Write LOW value to lane GPIO pin
    # Hold LOW for 2 milliseconds
    if not stat_iface:
        stat_iface = obj_iface.gpio_write(
            addr_ln=addr_ln,
            data_iface_in=0,
            mode=False,
            stat_en=False
        )
        time.sleep(0.050)

    if stat_iface == STAT_LVL['crit']:
        log = 'Lane {0} network reset can not be completed due to interface errors.'.format(addr_ln)
        logger.critical(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'CRITICAL',
            log
        ])

    else:
        log = 'Lane {0} network reset complete.'.format(addr_ln)
        logger.info(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'DEBUG',
            log
        ])
    print(log)

    return stat_iface


def init(
    obj_iface: TYPE_INTERFACE,
    addr_ln: int
):
    """
    Initializes lane

    :param obj_iface: Interface Object
    :param addr_ln: int

    :return mod_last: 0 (if STAT_LVL['crit'])
    :return mod_last: int (if STAT_LVL['op'])
    :return stat_ln: json (if STAT_LVL['op'] or STAT_LVL['not_cfg'])
    :return stat_iface: STAT_LVL['op'] or STAT_LVL['crit']
    :return stat_cdb: STAT_LVL['op'] or STAT_LVL['crit']
    """
    # Change logging level since this operates in multiprocess
    # Cycle to last entry for most current log setting
    while not MPQ_SETUP_LOG_INIT.empty():
        mpq_record = MPQ_SETUP_LOG_INIT.get()
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

    stat_ln = STAT_LVL['op']
    count_mod = 0

    # Each module with an entry in CouchDB modconfig database
    # has a setup_id field that uniquely identifies the latest
    # time that it was placed on a lane and setup.
    setup_id = time.time()

    # Set lane GPIO pin to READ mode so that interrupts can
    # be captured.  This also places pin into HIGH state.
    data_iface_out, stat_iface = obj_iface.gpio_read(
        addr_ln=addr_ln,
        mode=True,
        stat_en=True
    )

    if not stat_iface:

        mod_last_found = False

        # Sets the lane on a four-lane interface, default
        # return of operational if interface is single lane
        stat_iface = obj_iface.i2c_lane_set(addr_ln=addr_ln)

        if not stat_iface:
            # This loop cycles through each connected module with address
            # of 0x7F until mod_last_found flag is set

            while not mod_last_found and (count_mod <= 126):

                # Retrieve memory to end of mod_uid from module with I2C address of 0x7F.
                # If module responds, proceed to module setup actions, otherwise
                # mod_last_found flag is set.
                time_a = time.time()
                high_mmap = len(MMAP) - 1
                addr_mem = MMAP[high_mmap]['M_CFG_ALL'][0]
                data_len = MMAP[high_mmap]['M_CFG_ALL'][1]

                data_iface_out, stat_iface = obj_iface.i2c_read(
                    addr_ln=addr_ln,
                    addr_mod=0x7F,
                    addr_mem=addr_mem,
                    data_len=data_len,
                    stat_en=False
                )

                print('lane {0} module {1} i2c_read mod_config: {2}'.
                      format(addr_ln, (count_mod + 1), round((time.time() - time_a), 3)))
                print(data_iface_out)
                # Check for proper memory map version
                if not stat_iface and (data_iface_out[2] <= high_mmap):

                    # Call module setup routine and return module id and status
                    module.setup(
                        obj_iface=obj_iface,
                        setup_id=setup_id,
                        cfg_bytes=data_iface_out,
                        addr_ln=addr_ln,
                        addr_mod=(count_mod + 1)
                    )

                    # Increment counter before moving to another module
                    count_mod += 1

                    # Skip assigning I2C address #70 to module, on four-port interface
                    # this address used to set the lane
                    if count_mod == 70:
                        count_mod += 1

                    print('Full lane {0} module {1} setup: {2}'.
                          format(addr_ln, (count_mod - 1), round((time.time() - time_a), 3)))

                # If module has improper memory map version, or if module throws error
                # on I2C read, halt lane setup routine
                #
                # Impossible to differentiate from error thrown from reading connected module
                # or error thrown by reading non-existent module, treat both as the same and
                # end lane setup routine on this module.
                else:
                    mod_last_found = True

        else:
            log = 'Could not setup lane due to interface and/or CouchDB error.'
            logger.warning(log)

        if count_mod >= 1:
            log = 'Lane {0} initialized.'.format(addr_ln)
            logger.info(log)
            print(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'INFO',
                log
            ])

            log = 'Lane {0} last module is {1}.'.format(addr_ln, count_mod)
            logger.info(log)
            print(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'INFO',
                log
            ])

        else:
            log = 'No modules found for lane {0}.'.format(addr_ln)
            logger.warning(log)
            print(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])
            stat_ln = STAT_LVL['not_cfg']

    else:
        log = 'Could not complete priority 3 interface request on ' + \
              'lane {0} due to i2c lane set error.'.format(addr_ln)
        logger.critical(log)
        stat_ln = STAT_LVL['not_cfg']

    MPQ_STAT.put_nowait([
        'lane',
        [
            addr_ln,
            {
                'status': stat_ln,
                'last_module': count_mod,
                'setup_id': setup_id
            }
        ]
    ])

    # Get stat_lane view from CouchDB modconfig database
    data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
        cdb_cmd='get_view',
        cdb_name='modconfig',
        cdb_doc='stat_lane{0}'.format(addr_ln),
        logfile=logfile
    )

    mdb_sql = """
SELECT
    *
FROM
    aurora.lanes
WHERE
    lane={0}
""".format(addr_ln)

    data_mdb_out, stat_mdb, mdb_err = dbase.mdb_request(
        mdb_sql=mdb_sql,
        logfile=logfile
    )
    print(stat_mdb)
    print(mdb_err)
    print(data_mdb_out)

    if not stat_cdb:
        # Iterate through modules in view, determine which modules were
        # previously connected to this lane but are no longer connected.
        # Set their lane and module addresses to NULL and their status
        # to unconfigured.
        for dict_mod in data_cdb_out:
            if dict_mod['value']['setup_id'] != setup_id:
                data_cdb_in = {
                    'lane_addr': None,
                    'mod_addr': None,
                    'status': STAT_LVL['not_cfg'],
                    'errno': 0
                }

                # Update module document in CouchDB modconfig database
                data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
                    cdb_cmd='upd_doc',
                    cdb_name='modconfig',
                    cdb_doc=dict_mod['id'],
                    data_cdb_in=data_cdb_in,
                    logfile=logfile
                )

                if stat_cdb:
                    log = 'Could not update module configurations due to CouchDB error.'
                    logger.warning(log)

                print('UPDATED STATUS ON NON-EXISTENT MODULE: {0}'.format(dict_mod['id']))

    else:
        log = 'Could not update module configurations due to CouchDB error.'
        logger.warning(log)

    return stat_ln, stat_cdb
