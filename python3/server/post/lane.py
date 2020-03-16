import logging
from shared import dbase
from shared.globals import MPQ_CMD0, MPQ_CMD3, MPQ_LN_SETUP, AUTO_LNRST

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'server'
logger = logging.getLogger(logfile)


def poll_start(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return post_data: dict
    """
    # Issue request to start polling
    MPQ_CMD0.put_nowait({
        'command': 0,
        'args': [
            int(post_data['button_lane'])
        ],
        'data': []
    })

    return post_data


def poll_clear(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # Convert posted data to usable form
    addr_ln = int(post_data['button_lane'])

    # Issue request to clear poll data
    MPQ_CMD0.put_nowait({
        'command': 2,
        'args': [addr_ln],
        'data': []
    })

    # Get lane_status document from CouchDB lanes database
    data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='lanes',
        cdb_doc='lane{0}_status'.format(addr_ln),
        logfile=logfile,
    )

    if stat_cdb:
        data_cdb_out = post_data
        log = 'Could not update web GUI from CouchDB ' + \
              'due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def poll_stop(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return data_cdb_out: post_data if not STAT_LVL['op']
    :return data_cdb_out: CouchDB data if STAT_LVL['op']
    """
    # Convert posted data to usable form
    addr_ln = int(post_data['button_lane'])

    # Issue request to stop polling
    command_dict = {
        'command': 1,
        'args': [addr_ln],
        'data': []
    }
    MPQ_CMD0.put_nowait(command_dict)

    # Get lane_status document from CouchDB lanes database
    data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='lanes',
        cdb_doc='lane{0}_status'.format(addr_ln),
        logfile=logfile,
    )

    if stat_cdb:
        data_cdb_out = post_data
        log = 'Could not update web GUI from CouchDB ' + \
              'due to CouchDB error.'
        logger.warning(log)

    return data_cdb_out


def reset(post_data: dict):
    """
    POST handler

    :param post_data: dict

    :return None
    """
    # Convert posted data to usable form
    addr_ln = int(post_data['lane_address'])
    data_cdb_out = {}

    # Issue request to reset lane and execute lane setup
    MPQ_CMD3.put([
        addr_ln
    ])

    while True:
        if not MPQ_LN_SETUP.empty():
            iface_ln, stat_ch = MPQ_LN_SETUP.get()

            if (iface_ln == addr_ln) and (stat_ch == 0):

                # Get lane_status document from CouchDB lanes database
                data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
                    cdb_cmd='get_doc',
                    cdb_name='lanes',
                    cdb_doc='lane{0}_status'.format(addr_ln),
                    logfile=logfile,
                )

                # If CouchDB get has not failed, continue with module upload
                if not stat_cdb:
                    data_cdb_out['fail'] = False
                else:
                    data_cdb_out['fail'] = True

            else:
                data_cdb_out['fail'] = True

            break

    print('Pre manual lane reset: {0}'.format(AUTO_LNRST[addr_ln]))
    AUTO_LNRST[addr_ln] = 0
    print('Post manual lane reset: {0}'.format(AUTO_LNRST[addr_ln]))
    return data_cdb_out
