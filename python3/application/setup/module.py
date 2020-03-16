import logging
import struct
import time
from curses.ascii import isprint
from datetime import datetime
from interface.memorymap import MMAP
from shared import dbase
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT, TYPE_INTERFACE


__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'setup'
logger = logging.getLogger(logfile)


def setup(
    obj_iface: TYPE_INTERFACE,
    setup_id: float,
    cfg_bytes: list,
    addr_ln: int,
    addr_mod: int
):
    """
    Stores module memory map entry in CouchDB

    :param obj_iface: Interface Object
    :param setup_id: int
    :param cfg_bytes: list
    :param addr_ln: int
    :param addr_mod: int

    :return uid_mod: '0000' (if STAT_LVL['crit'])
    :return uid_mod: 16-byte str (if STAT_LVL['op'])
    :return stat_mod: STAT_LVL['op'] or STAT_LVL['not_cfg']
    """
    time_a = time.time()
    stat_mod = STAT_LVL['not_cfg']

    # Parse I2C data to build proper module id
    uid_mod = ''
    mod_uid_end = MMAP[cfg_bytes[2]]['M_UID'][0] + MMAP[cfg_bytes[2]]['M_UID'][1] - 1
    mod_uid_begin = MMAP[cfg_bytes[2]]['M_UID'][0] - 1
    for addr_mem in range(mod_uid_end, mod_uid_begin, -1):
        uid_mod_mem = str(hex(cfg_bytes[addr_mem]))[2:]
        if len(uid_mod_mem) == 1:
            uid_mod_mem = '0' + uid_mod_mem
        uid_mod += uid_mod_mem

    uid_mod_print = ''.join(char for char in uid_mod.strip() if isprint(char))

    print('lane {0} module {1} build mod_uid: {2}'.
          format(addr_ln, addr_mod, round((time.time() - time_a), 3)))

    # Check for data packet that has no content
    if ((uid_mod_print != '00000000000000000000000000000000') and
            (uid_mod_print != '0000000000000000000000000000000000000000000000000000000000000000')):

        # Assign I2C address to module, module will be present on I2C chain but inert
        # until properly setup.  If not properly setup modules on I2C chain after
        # this module will still be visible.
        time_b = time.time()
        stat_iface = obj_iface.i2c_write(
            addr_ln=addr_ln,
            addr_mod=0x7F,
            addr_mem=MMAP[cfg_bytes[2]]['M_ADDR'][0],
            data_iface_in=[addr_mod]
        )
        print('lane {0} module {1} i2c_write mod addr: {2}'.
              format(addr_ln, addr_mod, round((time.time() - time_b), 3)))

        # Proceed to setup actions if I2C write was successful
        if not stat_iface:
            # Set I2C comms flag to false so that module communications do not take place
            # until the base unit has a properly setup module in CouchDB modconfig database
            mod_comms = False

            # Get module document from CouchDB modconfig database, document will exist
            # if module was previously attached to base unit
            time_c = time.time()
            data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
                cdb_cmd='get_doc',
                cdb_name='modconfig',
                cdb_doc=uid_mod_print,
                logfile=logfile,
                attempts=1
            )
            print('lane {0} module {1} couch get mod_config: {2}'.
                  format(addr_ln, addr_mod, round((time.time() - time_c), 3)))

            # If module document exists in CouchDB modconfig database, proceed
            # to quick setup actions
            if not stat0_cdb and data0_cdb_out:

                time_d = time.time()
                # Set global default values and cycle through sensors to set
                # module sensor values for module document update in CouchDB
                # modconfig database
                data_cdb_in = {
                    'setup_id': setup_id,
                    'lane_addr': addr_ln,
                    'mod_addr': addr_mod,
                    'status': STAT_LVL['not_cfg'],
                    'errno': 0,
                }

                # Update module document in CouchDB modconfig database
                data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
                    cdb_cmd='upd_doc',
                    cdb_name='modconfig',
                    cdb_doc=uid_mod_print,
                    data_cdb_in=data_cdb_in,
                    logfile=logfile
                )

                if stat1_cdb:
                    log = 'Module configuration data could not be updated for ' +\
                          'lane {0} module {1} during setup, '.format(addr_ln, addr_mod) +\
                          'module remains inoperative.'
                    logger.warning(log)

                # If module update in CouchDB modconfig database was successful continue with
                # setup actions
                else:
                    # If number of sensors is 0, then module type and version was not located in
                    # CouchDB modules database during the module's very first setup.  This block
                    # checks if module type and version was since uploaded to modules database and
                    # attempts to complete module setup.
                    #
                    # TODO: Remove this block and update_module when mod self-rpting is en'd
                    if not data0_cdb_out['num_sensors']:
                        print('update module')
                        # Call function to update module document in
                        # CouchDB modconfig database
                        data0_cdb_out['num_sensors'] = update_module(
                            uid_mod_print=uid_mod_print,
                            data_cdb_in=data0_cdb_out,
                            addr_ln=addr_ln,
                            addr_mod=addr_mod
                        )

                    if data0_cdb_out['num_sensors']:
                        data0_cdb_out['mod_addr'] = addr_mod
                        data0_cdb_out['lane_addr'] = addr_ln
                        mod_comms = True

                    else:
                        log = 'Could not get module configuration due to CouchDB error.'
                        logger.warning(log)

                print('lane {0} module {1} couch update existing mod_config: {2}'.
                      format(addr_ln, addr_mod, round((time.time() - time_d), 3)))

            # If module document does not exist in CouchDB modconfig database, proceed
            # to long setup actions
            else:
                time_e = time.time()
                log = 'No module configuration data found for lane {0} '.format(addr_ln) + \
                      'module {0}, proceeding with setup of new module.'.format(addr_mod)
                logger.info(log)
                print(log)

                # Parse I2C data to get properly formatted module type
                mod_type = str(cfg_bytes[3])
                if len(str(mod_type)) == 1:
                    mod_type = '00' + mod_type
                elif len(str(mod_type)) == 2:
                    mod_type = '0' + mod_type

                # Parse I2C data to get properly formatted module version
                mod_ver = str(cfg_bytes[4])
                if len(str(mod_ver)) == 1:
                    mod_ver = '00' + mod_ver
                elif len(str(mod_ver)) == 2:
                    mod_ver = '0' + mod_ver

                # Build initial values for module setup
                data_cdb_in = {
                    "_id": uid_mod_print,
                    'lane_addr': addr_ln,
                    'mod_addr': addr_mod,
                    'mod_type': mod_type,
                    'mod_ver': mod_ver,
                    'setup_id': setup_id,
                }

                # Call function to store new module document in CouchDB modconfig database
                stat_store, data0_cdb_out = new_module(data_in=data_cdb_in)

                # If store of new module document is successful, continue module setup
                if not stat_store:
                    mod_comms = True

                else:
                    log = 'Could not initiate communications with module ' +\
                          'due to error in module storage process.'
                    logger.warning(log)

                print('lane {0} module {1} couch save new mod_config: {2}'.
                      format(addr_ln, addr_mod, round((time.time() - time_e), 3)))

            # If I2C communications with module is enabled, call function to set module
            # I2C address and upload module config values to module
            if mod_comms:
                time_f = time.time()
                stat_iface = comms_module(
                    data_cdb_out=data0_cdb_out,
                    obj_iface=obj_iface
                )

                if not stat_iface:
                    stat_mod = STAT_LVL['op']
                    log = 'Lane {0} module {1} setup completed.'.format(addr_ln, addr_mod)
                    logger.info(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'INFO',
                        log
                    ])

                else:
                    log = 'Lane {0} module {1} setup could not be completed due to I2C error.'.\
                          format(addr_ln, addr_mod)
                    logger.info(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'WARNING',
                        log
                    ])

                print('lane {0} module {1} i2c_write values to modules: {2}'.
                      format(addr_ln, addr_mod, round((time.time() - time_f), 3)))
            else:
                log = 'Lane {0} module {1} setup could not be '.format(addr_ln, addr_mod) +\
                      'completed due to missing data.'
                logger.info(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'WARNING',
                    log
                ])

        else:
            log = 'Lane {0} Module {0} could not be '.format(addr_ln, addr_mod) + \
                  'configured due to I2C error.'
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])

        MPQ_STAT.put_nowait([
            'module',
            [
                uid_mod_print,
                addr_ln,
                addr_mod,
                stat_mod
            ]
        ])

    else:
        log = 'Lane {0} Module {0} could not be '.format(addr_ln, addr_mod) + \
              'configured due to non-existent I2C content.'
        logger.warning(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'WARNING',
            log
        ])
        print(log)


def update_module(
    uid_mod_print: str,
    data_cdb_in: dict,
    addr_ln: int,
    addr_mod: int
):
    """
    Updates module configuration entry in CouchDB

    :param uid_mod_print: str
    :param data_cdb_in: dict
    :param addr_ln: int
    :param addr_mod: int
    """
    # Get module type/version document from CouchDB modules database
    cdb_doc = 'T{0}_V{1}'.format(data_cdb_in['mod_type'], data_cdb_in['mod_ver'])
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='modules',
        cdb_doc=cdb_doc,
        logfile=logfile,
        attempts=1
    )

    # If module type/version document exists, continue with update
    # of module configuration
    if not stat0_cdb and data0_cdb_out:

        num_sensors = data0_cdb_out['num_sensors']
        del data0_cdb_out['_rev']
        del data0_cdb_out['_id']

        for key in data0_cdb_out.keys():
            data_cdb_in[key] = data0_cdb_out[key]

        for addr_s in range(0, data0_cdb_out['num_sensors']):
            sensor = 'S{0}'.format(addr_s)
            data_cdb_in[sensor].update({
                'trig_low': 0,
                'trig_high': 30,
                'trig_step': 2,
                'trig_int': 900
            })

        # Update module document in CouchDB modconfig database
        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
            cdb_cmd='upd_doc',
            cdb_name='modconfig',
            cdb_doc='{0}'.format(uid_mod_print),
            data_cdb_in=data_cdb_in,
            logfile=logfile
        )

        if stat1_cdb:
            log = 'Could not update configuration data for lane ' + \
                  '{0} module {1} due '.format(addr_ln, addr_mod) + \
                  'to CouchDB document storage error.'
            logger.critical(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])

            log = 'Configuration data for lane {0} module {1} will remain blank.'. \
                format(addr_ln, addr_mod)
            logger.critical(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])

    else:
        log = 'Could not update configuration data for lane ' + \
              '{0} module {1} because '.format(addr_ln, addr_mod) + \
              'module type/version {0} does not exist.'.format(cdb_doc)
        logger.critical(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'WARNING',
            log
        ])

        log = 'Configuration data for lane {0} module {1} will remain blank.'. \
            format(addr_ln, addr_mod)
        logger.critical(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'WARNING',
            log
        ])

        num_sensors = 0

    return num_sensors


def new_module(
    data_in: dict
):
    """
    Stores module configuration entry in CouchDB

    :param data_in: dict

    :return stat_cdb: STAT_LVL['op'] or STAT_LVL['crit']
    """
    # Get module type/version document from CouchDB modules database
    data0_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='modules',
        cdb_doc='T{0}_V{1}'.format(data_in['mod_type'], data_in['mod_ver']),
        logfile=logfile,
        attempts=1
    )

    # If module type/version document exists, continue with store
    # of new module configuration
    if not stat_cdb and data0_cdb_out:
        data_cdb_in = {}

        del data0_cdb_out['_rev']
        del data0_cdb_out['_id']

        for key in data0_cdb_out.keys():
            data_cdb_in[key] = data0_cdb_out[key]

        for key in data_cdb_in.keys():
            if key in data_in.keys():
                data_cdb_in[key] = data_in[key]

        data_cdb_in.update({'_id': data_in['_id']})

        # Store module document in CouchDB modconfig database
        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
            cdb_cmd='sto_doc',
            cdb_name='modconfig',
            data_cdb_in=data_cdb_in,
            logfile=logfile
        )

        if stat1_cdb:
            log = 'Could not store new configuration data for lane ' + \
                  'module {1} due '.format(data_cdb_in['lane_addr'], data_cdb_in['mod_addr']) + \
                  'to CouchDB document storage error.'
            logger.critical(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])

            log = 'No configuration data for lane {0} module {1} will exist.'. \
                format(data_cdb_in['lane_addr'], data_cdb_in['mod_addr'])
            logger.critical(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])

    # If module type/version document does not exist, continue with store
    # of new module configuration using null data
    else:
        # TODO: get data from module self reporting, rather than load blank config
        data_cdb_in = {'num_sensors': 0}

        # Common entries for all sensors, all ports vacant
        for addr_s in range(0, 5):
            sensor = 'S{0}'.format(addr_s)
            data_cdb_in[sensor] = 'VACANT'

    return stat_cdb, data_cdb_in


def comms_module(
    data_cdb_out: dict,
    obj_iface: TYPE_INTERFACE = ''
):
    """
    Uploads module address and configuration to connected module

    :param data_cdb_out: dict
    :param obj_iface: Interface Object

    :return stat_iface: STAT_LVL['op'] or STAT_LVL['crit']
    """
    triggers_out = []
    stat_iface = STAT_LVL['op']

    # Cycle through module's installed sensors
    for addr_s in range(0, data_cdb_out['num_sensors']):
        sensor = 'S{0}'.format(addr_s)

        # Build I2C data packet for sensor low and high triggers
        trigger_low = struct.unpack(
            '4B',
            struct.pack(
                '>f',
                float(data_cdb_out[sensor]['trig_low'])
            )
        )[::-1]
        trigger_high = struct.unpack(
            '4B',
            struct.pack(
                '>f',
                float(data_cdb_out[sensor]['trig_high'])
            )
        )[::-1]

        for index in trigger_low:
            triggers_out.append(index)

        for index in trigger_high:
            triggers_out.append(index)

    # Upload low trigger values to module
    if len(triggers_out) > 0:
        stat_iface = obj_iface.i2c_write(
            addr_ln=data_cdb_out['lane_addr'],
            addr_mod=data_cdb_out['mod_addr'],
            addr_mem=MMAP[data_cdb_out['mem_map_ver']]['S0_LTRIG'][0],
            data_iface_in=triggers_out
        )

        if stat_iface:
            log = 'Triggers for lane {0} '.format(data_cdb_out['lane_addr']) + \
                  'module {0} could not be updated.'.format(data_cdb_out['mod_addr']) + \
                  'due to interface error.'
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])

        else:
            log = 'Triggers for lane {0} '.format(data_cdb_out['lane_addr']) + \
                  'module {0} were successfully updated.'.format(data_cdb_out['mod_addr'])
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'INFO',
                log
            ])

    return stat_iface
