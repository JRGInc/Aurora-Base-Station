import json
import logging
import multiprocessing
import mysql.connector
import time
import os
import requests
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from datetime import datetime
from random import randint
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'


def cdb_request(
    cdb_cmd: str,
    cdb_name: str = '',
    cdb_doc: str = '',
    data_cdb_in: dict = None,
    logfile: str = 'janusess',
    attempts: int = 5,
    backup_file: str = ''
):
    """
    Executes CouchDB transaction

    :param cdb_cmd: str
    :param cdb_doc: str
    :param cdb_name: str
    :param data_cdb_in: dict
    :param logfile: str
    :param attempts: int
    :param backup_file: str

    :return data_cdb_out: 0 (if STAT_LVL['op_err'])
    :return data_cdb_out: json (if STAT_LVL['op'])
    :return stat_cdb: STAT_LVL['op'] or STAT_LVL['crit']
    :return http_cdb: http response value
    """
    logger = logging.getLogger(logfile)

    http_resp = None
    cmd_req = ''
    cmd_str = ''
    data_cdb_out = 0
    data_en = True
    file_name = ''
    cont_exec = True
    stat_cdb = STAT_LVL['op']
    log_en = True
    stat_en = True
    http_cdb = 200
    attempt = 0

    if cdb_cmd == 'get_doc':
        cmd_req = 'get'
        cmd_str = 'http://127.0.0.1:5984/{0}/{1}'.format(cdb_name, cdb_doc)
        # TODO: When log cfg to *.ini file, delete following condition
        # TODO: When log cfg moves to *.ini file, remove log_en flags
        if (cdb_name == 'config') and (cdb_doc == 'log'):
            log_en = False

    elif cdb_cmd == 'get_view':
        cmd_req = 'get'
        cmd_str = 'http://127.0.0.1:5984/{0}/_design/{0}/_view/{1}'.format(cdb_name, cdb_doc)

    elif cdb_cmd == 'get_all':
        cmd_req = 'get'
        cmd_str = 'http://127.0.0.1:5984/{0}/_all_docs'.format(cdb_name)

    elif cdb_cmd == 'get_dbs':
        cmd_req = 'get'
        cmd_str = 'http://127.0.0.1:5984/_all_dbs'

    elif cdb_cmd == 'sto_doc':
        cmd_req = 'post'
        cmd_str = 'http://127.0.0.1:5984/{0}/'.format(cdb_name)

    elif cdb_cmd == 'upd_doc':
        cmd_req = 'get'
        cmd_str = 'http://127.0.0.1:5984/{0}/{1}'.format(cdb_name, cdb_doc)
        if (cdb_name == 'config') and (cdb_doc == 'base_status'):
            stat_en = False

    elif cdb_cmd == 'del_doc':
        cmd_req = 'get'
        cmd_str = 'http://127.0.0.1:5984/{0}/{1}'.format(cdb_name, cdb_doc)

    elif cdb_cmd == 'rst_dbs':
        cmd_req = 'delete'
        cmd_str = 'http://127.0.0.1:5984/{0}/'.format(cdb_name)
        if cdb_name == 'config':
            log_en = False

    elif cdb_cmd == 'cpt_dbs':
        cmd_req = 'post'
        cmd_str = 'http://127.0.0.1:5984/{0}/_compact'.format(cdb_name)
        data_en = False

    elif cdb_cmd == 'ark_dbs':
        cmd_req = 'get'
        cmd_str = 'http://127.0.0.1:5984/{0}/_all_docs?include_docs=true'.\
                  format(cdb_name)

        # Remove old archive file
        if backup_file == '':
            file_name = '/opt/Janus/ESS/backup/{0}Back.json'.format(cdb_name)

        else:
            file_name = backup_file

        file_exist = os.path.isfile(file_name)
        if file_exist:
            os.remove(file_name)

    elif cdb_cmd == 'res_dbs':
        cmd_req = 'post'
        cmd_str = 'http://127.0.0.1:5984/{0}/_bulk_docs'.format(cdb_name)

        # Get data from archive file
        if backup_file == '':
            file_name = '/opt/Janus/ESS/backup/{0}Back.json'.format(cdb_name)

        else:
            file_name = backup_file

        file_exist = os.path.isfile(file_name)
        if file_exist:
            mp_lock = multiprocessing.Lock()
            mp_lock.acquire()

            with open(
                file_name,
                mode='r',
                encoding='utf-8'
            ) as in_file:
                data_file_in = in_file.read()
                in_file.flush()
                in_file.close()

            mp_lock.release()

            # Issue CouchDB POST request and process result
            data_cdb_in = json.loads(data_file_in)

        else:
            cont_exec = False
            if cdb_name == 'config':
                log_en = False
            else:
                log = 'Can not locate file from which to restore {0} '.format(cdb_name) +\
                      'database.'
                logger.warning(log)

    # Always executes except in case of res_dbs, where file may not be found
    if cont_exec:
        timeout = 4.0  # large value for RPI v3
        cdb_err_conx = False
        cdb_err_timeout = False

        # Cycle through attempts
        for attempt in range(1, (attempts + 1)):
            if cmd_req == 'get':
                try:
                    http_resp = requests.get(
                        cmd_str,
                        timeout=timeout
                    )
                except requests.exceptions.ConnectionError:
                    cdb_err_conx = True
                except requests.exceptions.ReadTimeout:
                    cdb_err_timeout = True

            elif cmd_req == 'post':
                if data_en:
                    data_json_in = json.dumps(data_cdb_in)
                    try:
                        http_resp = requests.post(
                            cmd_str,
                            headers={'Content-type': 'application/json'},
                            data=data_json_in,
                            timeout=timeout
                        )
                    except requests.exceptions.ConnectionError:
                        cdb_err_conx = True
                    except requests.exceptions.ReadTimeout:
                        cdb_err_timeout = True

                else:
                    try:
                        http_resp = requests.post(
                            cmd_str,
                            headers={'Content-type': 'application/json'},
                            timeout=timeout
                        )
                    except requests.exceptions.ConnectionError:
                        cdb_err_conx = True
                    except requests.exceptions.ReadTimeout:
                        cdb_err_timeout = True

            elif cmd_req == 'delete':
                try:
                    http_resp = requests.delete(
                        cmd_str,
                        timeout=timeout
                    )
                except requests.exceptions.ConnectionError:
                    cdb_err_conx = True
                except requests.exceptions.ReadTimeout:
                    cdb_err_timeout = True

            if cdb_err_conx:
                stat_cdb = STAT_LVL['crit']
                log = 'Local CouchDB server did not respond to stage one {0}: {1}.'.format(cmd_req, cmd_str)
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
                        'couchdb',
                        stat_cdb
                    ]
                ])

            elif cdb_err_timeout:
                stat_cdb = STAT_LVL['op_err']
                log = 'Local CouchDB server timed out on stage one {0}: {1}.'.format(cmd_req, cmd_str)
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
                        'couchdb',
                        stat_cdb
                    ]
                ])

            else:
                data_cdb_out, stat_cdb, http_cdb = cdb_parse(
                    http_resp=http_resp,
                    cdb_doc=cdb_doc,
                    cdb_name=cdb_name,
                    attempt=attempt,
                    attempts=attempts,
                    log_en=log_en,
                    stat_en=stat_en,
                    logfile=logfile
                )

                # Execute two-stage GET view transaction
                if (cdb_cmd == 'get_view') and (http_cdb == 200) and not stat_cdb:
                    data_cdb_out = data_cdb_out['rows']

                # Execute two-stage GET all documents transaction
                elif (cdb_cmd == 'get_all') and (http_cdb == 200) and not stat_cdb:
                    data_cdb_all = []

                    for row in range(0, data_cdb_out['total_rows']):
                        # Issue CouchDB GET request and process result
                        cmd_str = 'http://127.0.0.1:5984/{0}/{1}'.format(cdb_name, data_cdb_out['rows'][row]['id'])
                        try:
                            http_resp = requests.get(
                                cmd_str,
                                timeout=timeout
                            )
                        except requests.exceptions.ConnectionError:
                            cdb_err_conx = True
                        except requests.exceptions.ReadTimeout:
                            cdb_err_timeout = True

                        if not cdb_err_conx:
                            data_cdb_row, stat_cdb, http_cdb = cdb_parse(
                                http_resp=http_resp,
                                cdb_doc=cdb_doc,
                                cdb_name=cdb_name,
                                attempt=attempt,
                                attempts=attempts,
                                log_en=log_en,
                                stat_en=stat_en,
                                logfile=logfile
                            )
                            data_cdb_all.append(data_cdb_row)

                    data_cdb_out = data_cdb_all

                    # Must delete '_rev' key as this prevents proper
                    # update of document to CouchDB
                    if not isinstance(data_cdb_out, int):
                        for data_dict in data_cdb_out:
                            if (isinstance(data_dict, dict)) and ('_rev' in data_dict.keys()):
                                del data_dict['_rev']

                # Execute two-level PUT document transaction
                elif (cdb_cmd == 'upd_doc') and (http_cdb == 200) and not stat_cdb:
                    for key0 in data_cdb_out.keys():
                        if key0 in data_cdb_in.keys():
                            if not (isinstance(data_cdb_out[key0], dict)):
                                data_cdb_out[key0] = data_cdb_in[key0]
                            else:
                                for key1 in data_cdb_out[key0].keys():
                                    if key1 in data_cdb_in[key0].keys():
                                        data_cdb_out[key0][key1] = data_cdb_in[key0][key1]

                    # Issue CouchDB PUT request and process result
                    data_json_in = json.dumps(data_cdb_out)
                    cmd_str = 'http://127.0.0.1:5984/{0}/{1}/'.format(cdb_name, cdb_doc)
                    try:
                        http_resp = requests.put(
                            cmd_str,
                            headers={'Content-type': 'application/json'},
                            data=data_json_in,
                            timeout=timeout
                        )

                    except requests.exceptions.ConnectionError:
                        cdb_err_conx = True
                    except requests.exceptions.ReadTimeout:
                        cdb_err_timeout = True

                    if not cdb_err_conx:
                        data_cdb_out, stat_cdb, http_cdb = cdb_parse(
                            http_resp=http_resp,
                            cdb_doc=cdb_doc,
                            cdb_name=cdb_name,
                            attempt=attempt,
                            attempts=attempts,
                            log_en=log_en,
                            stat_en=stat_en,
                            logfile=logfile
                        )

                # Execute two-stage DEL document transaction
                elif (cdb_cmd == 'del_doc') and (http_cdb == 200) and not stat_cdb:
                    data_json_in = json.dumps(data_cdb_out)

                    cmd_str = 'http://127.0.0.1:5984/{0}/{1}?rev={2}'.format(cdb_name, cdb_doc, data_json_in['_rev'])
                    try:
                        http_resp = requests.delete(
                            cmd_str,
                            timeout=timeout
                        )

                    except requests.exceptions.ConnectionError:
                        cdb_err_conx = True
                    except requests.exceptions.ReadTimeout:
                        cdb_err_timeout = True

                    if not cdb_err_conx:
                        data_cdb_out, stat_cdb, http_cdb = cdb_parse(
                            http_resp=http_resp,
                            cdb_doc=cdb_doc,
                            cdb_name=cdb_name,
                            attempt=attempt,
                            attempts=attempts,
                            log_en=log_en,
                            stat_en=stat_en,
                            logfile=logfile
                        )

                # Execute two-stage PUT database transaction
                # Either database is deleted or not found, either way
                # proceed with recreation
                elif (cdb_cmd == 'rst_dbs') and \
                        ((http_cdb == 200) or (http_cdb == 404)) and \
                        ((not stat_cdb) or (stat_cdb == STAT_LVL['op_err'])):

                    cmd_str = 'http://127.0.0.1:5984/{0}'.format(cdb_name)
                    try:
                        http_resp = requests.put(
                            cmd_str,
                            timeout=timeout
                        )

                    except requests.exceptions.ConnectionError:
                        cdb_err_conx = True
                    except requests.exceptions.ReadTimeout:
                        cdb_err_timeout = True

                    if not cdb_err_conx:
                        data_cdb_out, stat_cdb, http_cdb = cdb_parse(
                            http_resp=http_resp,
                            cdb_doc=cdb_doc,
                            cdb_name=cdb_name,
                            attempt=attempt,
                            attempts=attempts,
                            log_en=log_en,
                            stat_en=stat_en,
                            logfile=logfile
                        )

                # Execute two-stage GET view transaction
                elif (cdb_cmd == 'ark_dbs') and (http_cdb == 200) and not stat_cdb:
                    data_file_in = '{"docs":['
                    for data_cdb_row in data_cdb_out['rows']:
                        data_file_in = data_file_in + '{'
                        for key in data_cdb_row['doc']:
                            if key != '_rev':
                                data_file_in = data_file_in + '"' + str(key) + \
                                    '": ' + json.dumps(data_cdb_row["doc"][key]) + \
                                    ", "
                        data_file_in = data_file_in[:-2] + '}, '
                    data_file_in = data_file_in[:-2] + ']}'

                    mp_lock = multiprocessing.Lock()
                    mp_lock.acquire()

                    with open(
                        file_name,
                        mode='w',
                        encoding='utf-8'
                    ) as file_out:
                        file_out.write(data_file_in)
                        file_out.flush()
                        file_out.close()

                    mp_lock.release()

                if cdb_err_conx:
                    stat_cdb = STAT_LVL['crit']
                    log = 'Local CouchDB server did not respond to stage two {0}: {1}.'.format(cmd_req, cmd_str)
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
                            'couchdb',
                            stat_cdb
                        ]
                    ])

                elif cdb_err_timeout:
                    stat_cdb = STAT_LVL['op_err']
                    log = 'Local CouchDB server timed out on stage two {0}: {1}.'.format(cmd_req, cmd_str)
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
                            'couchdb',
                            stat_cdb
                        ]
                    ])

                # Break for loop on fully successful transactions
                if (http_cdb >= 200) and (http_cdb < 300) and not stat_cdb \
                        and not cdb_err_conx:
                    break

            if attempts > 1:
                time.sleep(0.005 * randint(0, 9) * attempt)

    if log_en:
        log_success = ''
        log_failure = ''

        if cdb_cmd == 'get_doc':
            log_success = 'Successfully retrieved document {0} from '.format(cdb_doc) + \
                          'CouchDB {0} database after {1} attempts.'.format(cdb_name, attempt)
            log_failure = 'General failure to get document {0} from/in '.format(cdb_doc) + \
                          'CouchDB {0} database after {1} attempts.'.format(cdb_name, attempt)

        elif cdb_cmd == 'get_view':
            log_success = 'Successfully retrieved view {0} from '.format(cdb_doc) + \
                          'CouchDB {0} database after {1} attempts.'.format(cdb_name, attempt)
            log_failure = 'General failure to get view {0} from '.format(cdb_doc) + \
                          'CouchDB {0} database after {1} attempts.'.format(cdb_name, attempt)

        elif cdb_cmd == 'get_all':
            log_success = 'Successfully retrieved all documents from CouchDB ' + \
                          '{0} database after {1} attempts.'.format(cdb_name, attempt)
            log_failure = 'General failure to get all documents from CouchDB ' + \
                          '{0} database after {1} attempts.'.format(cdb_name, attempt)

        elif cdb_cmd == 'get_dbs':
            log_success = 'Successfully retrieved all databases from CouchDB ' +\
                          'after {0} attempts.'.format(attempt)
            log_failure = 'General failure to get all databases from CouchDB ' +\
                          'after {0} attempts.'.format(attempt)

        elif cdb_cmd == 'sto_doc':
            log_success = 'Successfully stored document {0} in '.format(data_cdb_in['_id']) +\
                          'CouchDB {0} database after {1} attempts.'.format(cdb_name, attempt)
            log_failure = 'General failure to store document {0} '.format(data_cdb_in['_id']) + \
                          'in CouchDB {0} database after {1} attempts.'.format(cdb_name, attempt)

        elif cdb_cmd == 'upd_doc':
            log_success = 'Successfully updated document {0} in '.format(cdb_doc) + \
                          'CouchDB {0} database after {1} attempts.'.format(cdb_name, attempt)
            log_failure = 'General failure to update document {0} '.format(cdb_doc) + \
                          'in CouchDB {0} database after {1} attempts.'.format(cdb_name, attempt)

        elif cdb_cmd == 'del_doc':
            log_success = 'Successfully deleted document {0} from '.format(cdb_doc) + \
                          'CouchDB {0} database after {1} attempts.'.format(cdb_name, attempt)
            log_failure = 'General failure to delete document {0} from '.format(cdb_doc) + \
                          'CouchDB {0} database after {1} attempts.'.format(cdb_name, attempt)

        elif cdb_cmd == 'rst_dbs':
            log_success = 'Successfully reset CouchDB {0} database after '.format(cdb_name) +\
                          '{0} attempts.'.format(attempt)
            log_failure = 'General failure to reset CouchDB {0} database '.format(cdb_name) +\
                          'after {0} attempts.'.format(attempt)

        elif cdb_cmd == 'cpt_dbs':
            log_success = 'Successfully compacted CouchDB {0} '.format(cdb_name) +\
                          'database after {0} attempts.'.format(attempt)
            log_failure = 'General failure to compact CouchDB {0} '.format(cdb_name) +\
                          'database after {0} attempts.'.format(attempt)

        elif cdb_cmd == 'ark_dbs':
            log_success = 'Successfully archived CouchDB {0} '.format(cdb_name) +\
                          'database after {0} attempts.'.format(attempt)
            log_failure = 'General failure to archive CouchDB {0} '.format(cdb_name) +\
                          'database after {0} attempts.'.format(attempt)

        elif cdb_cmd == 'res_dbs':
            log_success = 'Successfully restored CouchDB {0} '.format(cdb_name) +\
                          'database after {0} attempts.'.format(attempt)
            log_failure = 'General failure to restore CouchDB {0} '.format(cdb_name) +\
                          'database after {0} attempts.'.format(attempt)

        if not stat_cdb:
            log = log_success
            activity_status = 'DEBUG'

        else:
            log = log_failure
            activity_status = 'CRITICAL'

        logger.log(logging.INFO if not stat_cdb else logging.CRITICAL, log)

        if stat_en:
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                activity_status,
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'couchdb',
                    stat_cdb
                ]
            ])

    return data_cdb_out, stat_cdb, http_cdb


def cdb_parse(
    http_resp: requests.models.Response,
    cdb_doc: str,
    cdb_name: str,
    attempt: int,
    attempts: int,
    log_en: bool,
    stat_en: bool = True,
    logfile: str = 'janusess',
):
    """
    Processes http response from CouchDB action

    :param http_resp: int
    :param cdb_doc: str
    :param cdb_name: str
    :param attempt: int
    :param attempts: int
    :param log_en: bool
    :param stat_en: bool
    :param logfile: str

    :return data_cdb_out: 0 (if STAT_LVL['op_err'])
    :return data_cdb_out: json (if STAT_LVL['op'])
    :return stat_cdb: STAT_LVL['op'] or STAT_LVL['crit']
    ;Return http_cdb: http response value
    """
    logger = logging.getLogger(logfile)
    data_cdb_out = 0
    stat_cdb = STAT_LVL['op']
    http_cdb = http_resp.status_code

    # Successful GET attempt
    if http_resp.status_code == 200:
        data_cdb_out = http_resp.json()

        log = 'Attempt {0} of {1} to get document '.format(attempt, attempts) +\
              '{0} from CouchDB {1} data succeeded.'.format(cdb_doc, cdb_name)
        if log_en:
            logger.debug(log)
            if stat_en:
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'DEBUG',
                    log
                ])

    elif http_resp.status_code == 201:
        log = 'Attempt {0} of {1} to store/update document '.format(attempt, attempts) + \
              '{0} to/in CouchDB {1} database succeeded.'.format(cdb_doc, cdb_name)
        if log_en:
            logger.debug(log)
            if stat_en:
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'DEBUG',
                    log
                ])

    elif http_resp.status_code == 202:
        log = 'Attempt {0} of {1} to compact CouchDB '.format(attempt, attempts) +\
              '{0} database succeeded.'.format(cdb_name)
        if log_en:
            logger.debug(log)
            if stat_en:
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'DEBUG',
                    log
                ])

    # Document not found error
    elif http_resp.status_code == 404:
        stat_cdb = STAT_LVL['op_evt']
        if attempt == attempts:
            log = 'Attempt to get document {0} from CouchDB '.format(cdb_doc) +\
                  '{0} database failed, document not found.'.format(cdb_name)
            if log_en:
                logger.warning(log)
                if stat_en:
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'WARNING',
                        log
                    ])

    # All other errors
    else:
        stat_cdb = STAT_LVL['crit']
        if attempt == attempts:
            log = 'Attempt {0} of {1} to execute document '.format(attempt, attempts) + \
                  '{0} transaction in CouchDB {1} data '.format(cdb_doc, cdb_name) + \
                  'returned http response {0}.'.format(http_resp.status_code)
            if log_en:
                logger.warning(log)
                if stat_en:
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'WARNING',
                        log
                    ])

    return data_cdb_out, stat_cdb, http_cdb


def cdb_check():
    """
    Checks CouchDB if ready to accept transactions
    """
    logfile = 'janusess'
    logger = logging.getLogger(logfile)

    check_time = 0.5

    log = 'Checking CouchDB every {0} sec until operational.'.format(check_time)
    logger.debug(log)

    count = 1
    while True:

        # Issue CouchDB GET request and process result
        http_resp = requests.get('http://127.0.0.1:5984/')

        # Successful GET request
        if http_resp.status_code == 200:
            log = 'CouchDB is operational.'
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'INFO',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'couchdb',
                    STAT_LVL['op']
                ]
            ])
            break

        # All GET errors
        else:
            log = 'CouchDB is not operational, failed with http ' +\
                  'response {0}.  Making another attempt.'.format(http_resp.status_code)
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'couchdb',
                    STAT_LVL['cfg_err']
                ]
            ])

        count += count
        time.sleep(check_time)


def idb_check():
    """
    Checks InfluxDB if ready to accept transactions
    """
    logfile = 'janusess'
    logger = logging.getLogger(logfile)

    check_time = 3.0

    log = 'Checking InfluxDB every {0} sec until operational.'.format(check_time)
    logger.debug(log)

    count = 1
    # Simple check to determine if InfluxDB is operating and that the JanusESS database exists
    # Could not get a good response from requests library during system start,
    # so using influxdb library instead.
    data_cdb_in = 'SHOW DATABASES;'
    while True:
        try:
            influxdb_client = InfluxDBClient(
                host='localhost',
                port=8086,
                timeout=5
            )
            influxdb_result = influxdb_client.query(data_cdb_in)
            stat_idb = STAT_LVL['undeter']
            for key in influxdb_result:
                for index in key:
                    if index['name'] == 'JanusESS':
                        stat_idb = STAT_LVL['op']
                        break
                if stat_idb == STAT_LVL['op']:
                    break

            if not stat_idb:
                log = 'InfluxDB is operational.'
                logger.info(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'INFO',
                    log
                ])
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'influxdb',
                        stat_idb
                    ]
                ])

            else:
                stat_idb = STAT_LVL['cfg_err']
                log = 'Local InfluxDB server responded to check but JanusESS database was not found.'
                logger.critical(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'CRITICAL',
                    log
                ])
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'influxdb',
                        stat_idb
                    ]
                ])

                # Create missing database and loop again for anther check.
                influxdb_client.create_database('JanusESS')
                log = 'Created missing JanusESS database. Making another check.'
                logger.warning(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'WARNING',
                    log
                ])

        except InfluxDBClientError:
            stat_idb = STAT_LVL['not_cfg']
            log = 'Local InfluxDB server did not respond to check. Trying again.'
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
                    stat_idb
                ]
            ])

        if stat_idb < STAT_LVL['not_cfg']:
            break

        count += count
        time.sleep(check_time)


def recover(db_list: list):
    """
    Recover from corrupt JanusESS databases found during startup

    :param db_list: list

    :return stat_cdb: STAT_LVL['op'] or STAT_LVL['cfg_err']
    """
    logfile = 'janusess'
    logger = logging.getLogger(logfile)

    stat_cdb = STAT_LVL['op']

    # Cycle through all databases in the list
    for cdb_name in db_list:

        # Get all documents from listed CouchDB database
        data_cdb_out, stat_cdb, http_cdb = cdb_request(
            cdb_cmd='get_all',
            cdb_name=cdb_name,
            logfile=logfile
        )

        # Check for database corruption
        db_attempt = 0
        while (data_cdb_out == 0) and (db_attempt <= 1):
            log = 'JanusESS start stalled due to config database corruption.'
            logger.warning(log)

            log = 'Attempting to restore {0} database from backup.'.format(cdb_name)
            logger.warning(log)
            MPQ_STAT.put_nowait([
                'base',
                [
                    'couchdb',
                    STAT_LVL['cfg_err']
                ]
            ])

            # Delete and create database
            data_cdb_out, stat_cdb, http_cdb = cdb_request(
                cdb_cmd='rst_dbs',
                cdb_name=cdb_name,
                logfile=logfile
            )

            if not stat_cdb:

                # Restore database documents from most recent
                # archived JSON file
                data_cdb_out, stat_cdb, http_cdb = cdb_request(
                    cdb_cmd='res_dbs',
                    cdb_name=cdb_name,
                    logfile=logfile
                )

                if not stat_cdb:

                    # Get all documents from listed CouchDB database
                    data_cdb_out, stat_cdb, http_cdb = cdb_request(
                        cdb_cmd='get_all',
                        cdb_name=cdb_name,
                        logfile=logfile
                    )

            db_attempt += 1

        if data_cdb_out == 0:
            log = 'JanusESS could not start due to {0} database corruption.'.\
                  format(cdb_name)
            logger.critical(log)

            log = 'Attempted restoration of {0} database failed.'.\
                  format(cdb_name)
            logger.critical(log)
            stat_cdb = ['cfg_err']
            MPQ_STAT.put_nowait([
                'base',
                [
                    'couchdb',
                    stat_cdb
                ]
            ])

    return stat_cdb


def mdb_request(
    mdb_sql: str,
    logfile: str = 'janusess',
    attempts: int = 5,
    backup_file: str = ''
):
    """
    Executes MariaDB transaction

    :param mdb_sql: str
    :param logfile: str
    :param attempts: int
    :param backup_file: str

    :return data_mdb_out: 0 (if STAT_LVL['op_err'])
    :return data_mdb_out: json (if STAT_LVL['op'])
    :return stat_mdb: STAT_LVL['op'] or STAT_LVL['crit']
    :return mdb_err: mariadb response value in event of error
    """
    logger = logging.getLogger(logfile)

    mdb_err = 'NONE'
    data_mdb_out = 0
    stat_mdb = STAT_LVL['op']
    attempt = 0

    # Cycle through attempts
    for attempt in range(1, (attempts + 1)):
        try:
            mdb_conn = mysql.connector.connect(
                user='aurora',
                password='PyrrHuloxia',
                host='127.0.0.1',
                database='aurora',
                unix_socket='/run/mysqld/mysqld.sock'
            )

            mdb_cursor = mdb_conn.cursor(dictionary=True)
            mdb_cursor.execute(mdb_sql)

            mdb_sql = mdb_sql.lstrip()
            if mdb_sql[:6] == 'SELECT':
                data_mdb_out = mdb_cursor.fetchall()

            elif mdb_sql[:11] == 'INSERT INTO':
                mdb_conn.commit()

            mdb_conn.close()
            stat_mdb = STAT_LVL['op']

            log = 'MariaDB is operational.'
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'INFO',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'mariadb',
                    stat_mdb
                ]
            ])

        except mysql.connector.Error as mdb_error:
            stat_mdb = STAT_LVL['op_err']
            log = 'Local MariaDB server failed to execute SQl statement, returned error: {0}.'.\
                format(mdb_error)
            mdb_err = mdb_error
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'mariadb',
                    stat_mdb
                ]
            ])

        if attempts > 1:
            time.sleep(0.005 * randint(0, 9) * attempt)

    if not stat_mdb:
        log = 'Successfully executed SQL statement in Aurora ' +\
              'database after {0} attempts.'.format(attempt)
        activity_status = 'DEBUG'

    else:
        log = 'General failure to execute SQl statement in Aurora ' +\
              'database after {0} attempts.'.format(attempt)
        activity_status = 'CRITICAL'

    logger.log(logging.INFO if not stat_mdb else logging.CRITICAL, log)

    MPQ_ACT.put_nowait([
        datetime.now().isoformat(' '),
        activity_status,
        log
    ])
    MPQ_STAT.put_nowait([
        'base',
        [
            'mariadb',
            stat_mdb
        ]
    ])

    return data_mdb_out, stat_mdb, mdb_err


def mdb_check():
    logfile = 'janusess'
    logger = logging.getLogger(logfile)

    check_time = 3.0

    log = 'Checking MariaDB every {0} sec until operational.'.format(check_time)
    logger.debug(log)

    count = 1

    while True:
        try:
            mdb_conn = mysql.connector.connect(
                user='aurora',
                password='PyrrHuloxia',
                host='127.0.0.1',
                database='aurora',
                unix_socket='/run/mysqld/mysqld.sock'
            )
            mdb_conn.close()
            stat_mdb = STAT_LVL['op']

            log = 'MariaDB is operational.'
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'INFO',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'mariadb',
                    stat_mdb
                ]
            ])

        except mysql.connector.Error:
            stat_mdb = STAT_LVL['not_cfg']
            log = 'Local MariaDB server did not respond to check. Trying again.'
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'mariadb',
                    stat_mdb
                ]
            ])

        if stat_mdb < STAT_LVL['not_cfg']:
            break

        count += count
        time.sleep(check_time)

