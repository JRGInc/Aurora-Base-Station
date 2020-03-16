from datetime import *
import logging
import time
from application.tasks import appdbase, queue, status, systime, network
from apscheduler.schedulers.background import BackgroundScheduler
from shared import dbase
from shared.globals import MPQ_NETINT
from tzlocal import get_localzone


__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'tasks'
logger = logging.getLogger(logfile)


def task_scheduler(
    db_list: list
):
    """
    JanusESS tasks scheduler

    :param db_list: list
    """
    # One minute tasks
    systime.store()
    appdbase.archive(db_list)

    # Get tasks document from CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='compact',
        logfile=logfile
    )
    if stat0_cdb:
        data0_cdb_out = {
            'dbcompact_firsttime': '0:13',
            'dbcompact_interval': 1
        }

    data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='network',
        logfile=logfile
    )
    if stat1_cdb:
        data1_cdb_out = {
            'url_server': 'www.google.com',
            'interval_good': 30,
            'interval_bad': 5,
            'url_timeout': 10
        }

    data2_cdb_out, stat2_cdb, http2_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='update',
        logfile=logfile
    )
    if stat2_cdb:
        data2_cdb_out = {
            'updateemail_firsttime': '0:33',
            'updateemail_interval': 1
        }

    net_int = data1_cdb_out['interval_good']
    prev_net_int = net_int

    # Need to build earliest start time from input and properly format for dbcompact
    dbcompact_int = int(data0_cdb_out['dbcompact_interval'])
    dbcompact_hour = int(data0_cdb_out['dbcompact_firsttime'].split(":")[0])
    while True:
        dbcompact_hour = dbcompact_hour - dbcompact_int
        if dbcompact_hour < 0:
            dbcompact_hour = str(dbcompact_hour + dbcompact_int)
            break
    if len(dbcompact_hour) == 1:
        dbcompact_hour = '0' + dbcompact_hour

    dbcompact_firsttime = str(dbcompact_hour) + ':' + data0_cdb_out['dbcompact_firsttime'].split(":")[1]
    dbcompact_start = datetime.today().strftime('%Y-%m-%d') + ' ' + dbcompact_firsttime + ':24'
    prev_dbcompact_start = dbcompact_start
    prev_dbcompact_int = dbcompact_int

    # Need to build earliest start time from input and properly format for update
    update_int = int(data2_cdb_out['updateemail_interval'])
    update_hour = int(data2_cdb_out['updateemail_firsttime'].split(":")[0])
    while True:
        update_hour = update_hour - update_int
        if update_hour < 0:
            update_hour = str(update_hour + update_int)
            break
    if len(update_hour) == 1:
        update_hour = '0' + update_hour

    update_firsttime = str(update_hour) + ':' + data2_cdb_out['updateemail_firsttime'].split(":")[1]
    update_start = datetime.today().strftime('%Y-%m-%d') + ' ' + update_firsttime + ':36'
    prev_update_start = update_start
    prev_update_int = update_int

    # Get the hour
    # Get the interval
    # Subtract interval from hour until negative number
    # Concatenate hour with minute to produce new first time

    timezone = get_localzone()
    scheduler = BackgroundScheduler(timezone=timezone)
    scheduler.remove_all_jobs()
    # scheduler.print_jobs()
    scheduler.add_job(
        systime.store,
        'cron',
        second='0'
    )
    scheduler.add_job(
        appdbase.archive,
        'cron',
        second='12',
        args=[db_list]
    )
    job_queue = scheduler.add_job(
        queue.clear,
        'interval',
        minutes=60
    )
    job_network = scheduler.add_job(
        network.check,
        'interval',
        minutes=net_int
    )
    job_compact = scheduler.add_job(
        appdbase.compact,
        'interval',
        start_date=dbcompact_start,
        hours=dbcompact_int
    )
    job_update = scheduler.add_job(
        status.update,
        'interval',
        start_date=update_start,
        hours=update_int,
        args=[update_int]
    )

    try:
        scheduler.start()
        scheduler.print_jobs()

    except (KeyboardInterrupt, SystemExit):
        scheduler.remove_all_jobs()
        scheduler.shutdown()

    while True:
        if not MPQ_NETINT.empty():
            net_int = MPQ_NETINT.get_nowait()
            if prev_net_int != net_int:
                prev_net_int = net_int
                job_network.remove()
                job_network = scheduler.add_job(
                    network.check,
                    'interval',
                    minutes=net_int
                )

        data3_cdb_out, stat3_cdb, http3_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='compact',
            logfile=logfile
        )

        if not stat3_cdb:
            # Need to build earliest start time from input and properly format for dbcompact
            dbcompact_int = int(data3_cdb_out['dbcompact_interval'])
            dbcompact_hour = int(data3_cdb_out['dbcompact_firsttime'].split(":")[0])
            while True:
                dbcompact_hour = dbcompact_hour - dbcompact_int
                if dbcompact_hour < 0:
                    dbcompact_hour = str(dbcompact_hour + dbcompact_int)
                    break
            if len(dbcompact_hour) == 1:
                dbcompact_hour = '0' + dbcompact_hour

            dbcompact_firsttime = str(dbcompact_hour) + ':' + data3_cdb_out['dbcompact_firsttime'].split(":")[1]
            dbcompact_start = datetime.today().strftime('%Y-%m-%d') + ' ' + dbcompact_firsttime + ':24'

            if (dbcompact_start != prev_dbcompact_start) or (dbcompact_int != prev_dbcompact_int):
                job_compact.remove()
                job_compact = scheduler.add_job(
                    appdbase.compact,
                    'interval',
                    start_date=dbcompact_start,
                    hours=dbcompact_int
                )
                prev_dbcompact_int = dbcompact_int
                prev_dbcompact_start = dbcompact_start

        data4_cdb_out, stat4_cdb, http4_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='config',
            cdb_doc='update',
            logfile=logfile
        )

        if not stat4_cdb:
            # Need to build earliest start time from input and properly format for update
            update_int = int(data4_cdb_out['updateemail_interval'])
            update_hour = int(data4_cdb_out['updateemail_firsttime'].split(":")[0])
            while True:
                update_hour = update_hour - update_int
                if update_hour < 0:
                    update_hour = str(update_hour + update_int)
                    break
            if len(update_hour) == 1:
                update_hour = '0' + update_hour

            update_firsttime = str(update_hour) + ':' + data4_cdb_out['updateemail_firsttime'].split(":")[1]
            update_start = datetime.today().strftime('%Y-%m-%d') + ' ' + update_firsttime + ':36'

            if (update_start != prev_update_start) or (update_int != prev_update_int):
                job_update.remove()
                job_update = scheduler.add_job(
                    status.update,
                    'interval',
                    start_date=update_start,
                    hours=update_int,
                    args=[update_int]
                )
                prev_update_int = update_int
                prev_update_start = update_start

        # scheduler.print_jobs()
        time.sleep(30)
