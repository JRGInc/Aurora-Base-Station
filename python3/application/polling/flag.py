import logging
from datetime import datetime
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_FLAG_LOG, TYPE_INTERFACE

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'polling'
logger = logging.getLogger(logfile)


def interrupt(
    obj_iface: TYPE_INTERFACE,
    addr_ln: int,
    addr_mod: int,
    evt_byte: list
):
    """
    Polls modules for interrupts

    :param obj_iface: Interface Object
    :param addr_ln: int
    :param addr_mod: int
    :param evt_byte: list

    :return stat_cdb: STAT_LVL['op'] or STAT_LVL['op_err']
    """
    while not MPQ_FLAG_LOG.empty():
        mpq_record = MPQ_FLAG_LOG.get()
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

    stat_mod = STAT_LVL['op']

    # Get trigger flag from module
    data_iface_in, err_iface = obj_iface.i2c_read(
        addr_ln=addr_ln,
        addr_mod=addr_mod,
        addr_mem=evt_byte[0],
        data_len=evt_byte[1]
    )
    print('check interrupt flag on lane {0} module {1}: {2}'.
          format(addr_ln, addr_mod, data_iface_in))

    # Check if trigger flag has been set, then perform actions
    if (not err_iface) and (data_iface_in[0] > 0):
        log = 'Interrupt discovered for lane {0} module {1}.'.\
              format(addr_ln, addr_mod, data_iface_in)
        logger.info(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'INFO',
            log]
        )

        # TODO: Assess proper value to send to STAT_MPQ and process for interrupt type
        stat_mod = STAT_LVL['op_evt']

        # Clear flag on module
        err_iface = obj_iface.i2c_write(
            addr_ln=addr_ln,
            addr_mod=addr_mod,
            addr_mem=evt_byte[0],
            data_out=[0]
        )

    elif (not err_iface) and (data_iface_in[0] == 0):
        log = 'No interrupt discovered for lane {0} module {1}.'. \
            format(addr_ln, addr_mod, data_iface_in)
        logger.info(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'DEBUG',
            log
        ])

    if err_iface:
        log = 'Could not check and clear event flag on lane {0} '.format(addr_ln) +\
              'module {0} due to interface errors.'.format(addr_mod)
        logger.warning(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'WARNING',
            log
        ])
        stat_mod = STAT_LVL['op_err']

    return stat_mod
