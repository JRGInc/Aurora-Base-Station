import logging
import time
from datetime import datetime
from os import close, remove
from random import randint
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT
from shutil import move
from tempfile import mkstemp

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'


# TODO: Hold library for module programming via I2C, update to handle *.hex files


def request(
    file_cmd: str,
    file_name: str,
    data_loc: int,
    num_bytes: int,
    data_file_in: str,
    search_field: str = '',
    replace_line: str = '',
    logfile: str = 'janusess',
    attempts: int = 3
):
    """
    Executes file transaction

    :param file_cmd: str
    :param file_name: str
    :param data_loc: int
    :param num_bytes: int
    :param search_field: str,
    :param replace_line: str,
    :param data_file_in: str
    :param logfile: str
    :param attempts: int

    :return read_err: bool
    :return data: 0 (read_err = True)
    :return data: str (read_err = False)
    """
    logger = logging.getLogger(logfile)

    stat_file = STAT_LVL['op']
    data_file_out = 0
    attempt = 1
    file_mode = ''
    field_dict = {}
    temp_path = None
    file_hdlr = None
    file_temp = None
    log_oserror = ''
    log_no_oserror = ''

    if file_cmd == 'data_read':
        file_mode = 'r'
        log_no_oserror = 'to retrieve data from file {0} succeeded.'.format(file_name)
        log_oserror = 'to retrieve data from file {0} failed.'.format(file_name)

    elif file_cmd == 'line_app':
        file_mode = 'a+'
        log_no_oserror = 'to append line to file {0} succeeded.'.format(file_name)
        log_oserror = 'to append line to file {0} failed.'.format(file_name)

    elif file_cmd == 'fld_read':
        file_mode = 'r'
        log_no_oserror = 'to read field from file {0} succeeded.'.format(file_name)
        log_oserror = 'to read field from file {0} failed.'.format(file_name)

    elif file_cmd == 'fld_read_all':
        file_mode = 'r'
        log_no_oserror = 'to read all fields from file {0} succeeded.'.format(file_name)
        log_oserror = 'to read all fields from file {0} failed.'.format(file_name)

    elif file_cmd == 'fld_edit':
        file_mode = 'r'
        log_no_oserror = 'to edit field in file {0} succeeded.'.format(file_name)
        log_oserror = 'to edit field in file {0} failed.'.format(file_name)

    elif file_cmd == 'data_wrt':
        file_mode = 'r+'
        log_no_oserror = 'to write data to file {0} succeeded.'.format(file_name)
        log_oserror = 'to write data to file {0} failed.'.format(file_name)

    elif file_cmd == 'file_replace':
        file_mode = 'w'
        log_no_oserror = 'to replace contents in file {0} succeeded.'.format(file_name)
        log_oserror = 'to replace contents in file {0} failed.'.format(file_name)

    # Cycle through attempts
    for attempt in range(1, (attempts + 1)):
        try:
            # Open file in specified mode, utf-8
            file_open = open(
                file_name,
                mode=file_mode,
                encoding='utf-8'
            )

            if file_cmd == 'data_read':
                file_open.seek(data_loc)
                data_file_out = file_open.read(num_bytes)

            elif file_cmd == 'line_app':
                file_open.write(data_file_in + '\n')
                file_open.flush()

            elif file_cmd == 'fld_read':
                for line in file_open:
                    line = line.split('\n')[0]
                    key = line.split('=')[0]
                    if key == search_field:
                        data_file_out = line.split('=')[1]

            elif file_cmd == 'fld_read_all':
                for line in file_open:
                    line = line.split('\n')[0]
                    key, val = line.split('=')
                    field_dict[key] = str(val)

            elif file_cmd == 'fld_edit':
                file_hdlr, temp_path = mkstemp()
                file_temp = open(temp_path,
                                 mode='w',
                                 encoding='utf-8'
                                 )

                found_field = False
                for line in file_temp:
                    if search_field in line:
                        file_temp.write(replace_line + '\n')
                        found_field = True

                    else:
                        file_temp.write(line)

                if not found_field:
                    file_temp.write(replace_line)

                file_temp.flush()

            elif file_cmd == 'data_wrt':
                file_open.seek(data_loc)
                file_open.write(data_file_in)
                file_open.flush()

            elif file_cmd == 'file_replace':
                file_open.seek(0)
                file_open.write(data_file_in)
                file_open.flush()

            # Close file
            file_open.close()

            if file_cmd == 'fld_edit':
                remove(file_name)
                move(temp_path, file_name)
                file_temp.close()
                close(file_hdlr)

            log = 'Attempt {0} of {1} '.format(attempt, (attempts - 1)) + log_no_oserror
            logger.debug(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'DEBUG',
                log
            ])
            stat_file = STAT_LVL['op']
            break

        except OSError:
            stat_file = STAT_LVL['op_err']
            MPQ_STAT.put_nowait([
                'base',
                [
                    'file',
                    stat_file
                ]
            ])
            if attempt == (attempts - 1):
                log = 'Attempt {0} of {1} '.format(attempt, (attempts - 1)) + log_oserror
                logger.exception(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'ERROR',
                    log
                ])

        time.sleep(0.1 * randint(0, 9) * attempt)

    log_success = ''
    log_failure = ''

    if file_cmd == 'data_read':
        log_success = 'Successfully read data from file {0} after {1} attempts.'.\
                      format(file_name, attempt)
        log_failure = 'General failure to read data from file {0}.'.format(file_name)

    elif file_cmd == 'line_app':
        log_success = 'Successfully appended line to file {0} after {1} attempts.'.\
                      format(file_name, attempt)
        log_failure = 'General failure to append line to file {0}.'.format(file_name)

    elif file_cmd == 'fld_read':
        log_success = 'Successfully read from file {0} after {1} attempts.'.\
                      format(file_name, attempt)
        log_failure = 'General failure to read field from file {0}.'.format(file_name)

    elif file_cmd == 'fld_read_all':
        log_success = 'Successfully read all fields from file {0} after {1} attempts.'.\
                      format(file_name, attempt)
        log_failure = 'General failure to read all fields from file {0}.'.format(file_name)

    elif file_cmd == 'fld_edit':
        log_success = 'Successfully edited field in file {0} after {1} attempts.'.\
                      format(file_name, attempt)
        log_failure = 'General failure to edit field in file {0}.'.format(file_name)

    elif file_cmd == 'data_wrt':
        log_success = 'Successfully wrote data to file {0} after {1} attempts.'.\
                      format(file_name, attempt)
        log_failure = 'General failure to write data to file {0}.'.format(file_name)

    elif file_cmd == 'file_replace':
        log_success = 'Successfully replaced contents in file {0} after {1} attempts.'.\
                      format(file_name, attempt)
        log_failure = 'General failure to replace contents in file {0}.'.format(file_name)

    if not stat_file:
        log = log_success
        activity_status = 'DEBUG'

    else:
        log = log_failure
        activity_status = 'CRITICAL'
        stat_file = STAT_LVL['crit']

    logger.log(logging.INFO if not stat_file else logging.CRITICAL, log)

    MPQ_ACT.put_nowait([
        datetime.now().isoformat(' '),
        activity_status,
        log
    ])
    MPQ_STAT.put_nowait([
        'base',
        [
            'file',
            stat_file
        ]
    ])

    return data_file_out, stat_file
