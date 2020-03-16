import logging
import struct
from interface.memorymap import MMAP
from interface.led import Control
from shared import conversion, dbase
from shared.globals import MPQ_CMD2, MPQ_CMD4, STAT_LVL


__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'server'
logger = logging.getLogger(logfile)


def poll(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return post_data: dict
    """
    mod_uid = str(post_data['mod_uid'])
    addr_ln = post_data['lane_address']
    addr_mod = post_data['module_address']

    # Issue request to start polling
    MPQ_CMD2.put_nowait([
        mod_uid,
        addr_ln,
        addr_mod
    ])

    return post_data


def modconfig(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # Convert posted data to usable form
    addr_ln = post_data['lane_address']
    addr_mod = post_data['module_address']
    addr_s = post_data['sensor_address']
    sensor = 'S{0}'.format(addr_s)
    mod_uid = str(post_data['mod_uid'])

    # Get module document from CouchDB modconfig database, document will exist
    # if module was previously attached to base unit
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='modconfig',
        cdb_doc=mod_uid,
        logfile=logfile
    )

    data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='dataunits',
        logfile=logfile
    )

    if not stat0_cdb:
        unit_convert = conversion.Conversion()

        # Convert low-threshold value to user-selected unit
        lth_value, lth_unit = unit_convert.convert(
            float(post_data['trig_low']),
            data1_cdb_out[data0_cdb_out[sensor]['type']],
            data0_cdb_out[sensor]['unit']
        )

        # Convert high-threshold value to user-selected unit
        uth_value, uth_unit = unit_convert.convert(
            float(post_data['trig_high']),
            data1_cdb_out[data0_cdb_out[sensor]['type']],
            data0_cdb_out[sensor]['unit']
        )

        # Convert step to user-selected unit
        step_value, step_unit = unit_convert.convert(
            float(post_data['trig_step']),
            data1_cdb_out[data0_cdb_out[sensor]['type']],
            data0_cdb_out[sensor]['unit'],
            step=True
        )

        data_cdb_in = {sensor: {}}
        if post_data['trig_low'] != '':
            data_cdb_in[sensor]['trig_low'] = lth_value

        else:
            data_cdb_in[sensor]['trig_low'] = 0.0

        if post_data['trig_high'] != '':
            data_cdb_in[sensor]['trig_high'] = uth_value

        else:
            data_cdb_in[sensor]['trig_high'] = 0.0

        if post_data['trig_step'] != '':
            data_cdb_in[sensor]['trig_step'] = step_value

        else:
            data_cdb_in[sensor]['trig_step'] = 0.0

        if post_data['trig_int'] != '':
            data_cdb_in[sensor]['trig_int'] = float(post_data['trig_int'])

        else:
            data_cdb_in[sensor]['trig_int'] = 0.0

        # Update module document in CouchDB modconfig database
        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
            cdb_cmd='upd_doc',
            cdb_name='modconfig',
            cdb_doc=mod_uid,
            data_cdb_in=data_cdb_in,
            logfile=logfile
        )

        if stat1_cdb:
            log = 'Could not update module config due to CouchDB error.'
            logger.warning(log)

        # Get lane_status document from CouchDB lanes database
        data2_cdb_out, stat2_cdb, http2_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='lanes',
            cdb_doc='lane{0}_status'.format(addr_ln),
            logfile=logfile,
        )

        # If lane has not failed, continue with module upload
        if not stat2_cdb and not stat0_cdb:
            if (data2_cdb_out['status'] < STAT_LVL['crit']) and (data0_cdb_out['status'] < STAT_LVL['crit']):

                # Issue request to update sensor lower trigger value,
                # does not depend on outcome of CouchDB get request
                vals = struct.unpack(
                    '4B',
                    struct.pack(
                        '>f',
                        float(post_data['trig_low'])
                    )
                )[::-1]
                data_out = []
                for value in vals:
                    data_out.append(value)

                # Get memory address for sensor trigger values
                addr_mem = MMAP[data0_cdb_out['mem_map_ver']]['S{0}_{1}'.format(
                    addr_s,
                    'LTRIG'
                )][0]

                MPQ_CMD4.put([
                    mod_uid,
                    addr_ln,
                    addr_mod,
                    addr_mem,
                    data_out
                ])

                # Issue request to update sensor upper trigger value,
                # does not depend on outcome of CouchDB get request
                vals = struct.unpack(
                    '4B',
                    struct.pack(
                        '>f',
                        float(post_data['trig_high'])
                    )
                )[::-1]
                data_out = []
                for value in vals:
                    data_out.append(value)

                # Get memory address for sensor trigger values
                addr_mem = MMAP[data0_cdb_out['mem_map_ver']]['S{0}_{1}'.format(
                    addr_s,
                    'HTRIG'
                )][0]

                MPQ_CMD4.put([
                    mod_uid,
                    addr_ln,
                    addr_mod,
                    addr_mem,
                    data_out
                ])

            else:
                log = 'Could not update module config due to CouchDB error.'
                logger.warning(log)

        else:
            log = 'Could not update module config due to CouchDB error.'
            logger.warning(log)

    else:
        log = 'Could not update module config due to CouchDB error.'
        logger.warning(log)
    
    return post_data


def location(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # Convert posted data to usable form
    mod_uid = post_data['mod_uid']

    # This variable gets overwritten on success
    data_cdb_out = post_data

    if post_data['loc'] is '':
        data_cdb_in = {
            'loc': 'NO LOCATION SET'
        }

    else:
        data_cdb_in = {
            'loc': post_data['loc']
        }

    # Update module document in CouchDB modconfig database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='upd_doc',
        cdb_name='modconfig',
        cdb_doc=mod_uid,
        data_cdb_in=data_cdb_in,
        logfile=logfile
    )

    # Get module document from CouchDB modconfig database
    if not stat0_cdb:
        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='modconfig',
            cdb_doc=mod_uid,
            logfile=logfile,
        )

        if not stat1_cdb:
            data_cdb_out = data1_cdb_out

    else:
        log = 'Could not update web GUI from CouchDB due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def led_effect(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return post_data: dict
    """
    mod_uid = str(post_data['mod_uid'])
    addr_ln = post_data['lane_address']
    addr_mod = post_data['module_address']
    effect = post_data['effect']

    led_ctl = Control()
    led_ctl.effect(
        effect,
        mod_uid,
        addr_ln,
        addr_mod
    )

    return post_data
