import logging
import multiprocessing
import smtplib
import socket
import time
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
from shared import dbase
from shared.messaging import templates
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'


logfile = 'email'
logger = logging.getLogger(logfile)


def send_mail(
    msg_type: str,
    args: list,
):
    """
    Sends messaging message

    :param msg_type: str
    :param args: list
    """
    # Get base_status document from CouchDB config database
    data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='base_status',
        logfile=logfile
    )

    # Get email document from CouchDB config database
    data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='email',
        logfile=logfile,
    )

    # Get sms document from CouchDB config database
    data2_cdb_out, stat2_cdb, http2_cdb = dbase.cdb_request(
        cdb_cmd='get_doc',
        cdb_name='config',
        cdb_doc='sms',
        logfile=logfile,
    )

    # If messaging is enabled by user and network is operational,
    # then build template and send messaging
    if not stat0_cdb and not stat1_cdb and not stat2_cdb:

        if data1_cdb_out['smtp_enable'] and not data0_cdb_out['network']:
            dict_msg, stat_msg_temp = templates.message_templates(
                sms_enable=data2_cdb_out['sms_enable'],
                msg_type=msg_type,
                args=args
            )

            # Uncomment to test messaging text formatting
            # print("\n\n\n")
            # print(dict_msg['smtp_subject'])
            # print(dict_msg['smtp_body'])
            # print("\n\n\n")
            # print(dict_msg['sms_subject'])
            # print(dict_msg['sms_body'])
            # print("\n\n\n")

            # Comment this block to test message text formatting
            if not stat_msg_temp:
                try:
                    email_mp = multiprocessing.Process(
                        target=send,
                        args=(
                            data1_cdb_out,
                            data2_cdb_out,
                            dict_msg
                        )
                    )
                    email_mp.start()

                except multiprocessing.ProcessError:
                    log = 'Can not send email due to multiprocessing error.'
                    logger.exception(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'ERROR',
                        log
                    ])
                    MPQ_STAT.put_nowait([
                        'base',
                        [
                            'email',
                            STAT_LVL['crit']
                        ]
                    ])

            else:
                log = 'Email not attempted, email template build failed.'
                logger.warning(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'WARNING',
                    log
                ])
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'email',
                        stat_msg_temp
                    ]
                ])

        elif not data1_cdb_out['smtp_enable']:
            log = 'Email disabled by user.'
            logger.debug(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'DEBUG',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'email',
                    STAT_LVL['not_cfg']
                ]
            ])

        else:
            log = 'Email not attempted, latest network check shows network ' + \
                  'disconnected.'
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'INFO',
                log
            ])
            MPQ_STAT.put_nowait([
                'base',
                [
                    'email',
                    STAT_LVL['not_cfg']
                ]
            ])

    else:
        log = 'Email not attempted due to CouchDB error.'
        logger.warning(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'WARNING',
            log
        ])
        MPQ_STAT.put_nowait([
            'base',
            [
                'email',
                STAT_LVL['not_cfg']
            ]
        ])


def send(
    data_cdb_smtp: dict,
    data_cdb_sms: dict,
    dict_msg: dict,
):
    """
    Sends email message

    :param data_cdb_smtp: dict
    :param data_cdb_sms: dict
    :param dict_msg: dict
    """
    stat_smtp = STAT_LVL['op']

    for attempt in range(1, 4):

        # Prepare message body, default is plain text
        smtp_email_msg = MIMEText(dict_msg['smtp_body'])
        sms_email_msg = None

        # Prepare recipients lists
        #
        # p = operational polling
        # s = system status updates
        # e = system errors
        smtp_recipients = None
        sms_recipients = None
        if dict_msg['smtp_distribution'] == 'p':
            smtp_email_msg['To'] = ', '.join(data_cdb_smtp['smtp_list_alert'])
            smtp_recipients = data_cdb_smtp['smtp_list_alert']

        elif dict_msg['smtp_distribution'] == 's':
            smtp_email_msg['To'] = ', '.join(data_cdb_smtp['smtp_list_status'])
            smtp_recipients = data_cdb_smtp['smtp_list_status']

        elif dict_msg['smtp_distribution'] == 'e':
            smtp_email_msg['To'] = ', '.join(data_cdb_smtp['smtp_list_error'])
            smtp_recipients = data_cdb_smtp['smtp_list_error']

        # Prepare message sender
        smtp_email_msg['From'] = data_cdb_smtp['smtp_from']

        # Prepare message subject line
        smtp_email_msg['Subject'] = Header(dict_msg['smtp_subject'])

        # If SMS is enabled prepare second message
        if data_cdb_sms['sms_enable']:
            sms_email_msg = MIMEText(dict_msg['sms_body'])

            sms_recipients = None
            if dict_msg['sms_distribution'] == 'p':
                sms_email_msg['To'] = ', '.join(data_cdb_sms['sms_list_alert'])
                sms_recipients = data_cdb_sms['sms_list_alert']

            elif dict_msg['sms_distribution'] == 's':
                sms_email_msg['To'] = ', '.join(data_cdb_sms['sms_list_status'])
                sms_recipients = data_cdb_sms['sms_list_status']

            elif dict_msg['sms_distribution'] == 'e':
                sms_email_msg['To'] = ', '.join(data_cdb_sms['sms_list_error'])
                sms_recipients = data_cdb_sms['sms_list_error']

            sms_email_msg['From'] = data_cdb_smtp['smtp_from']
            sms_email_msg['Subject'] = Header(dict_msg['sms_subject'])

        pymail = None

        # Build SMTP server connection
        try:
            pymail = smtplib.SMTP(
                host=data_cdb_smtp['smtp_server'],
                port=data_cdb_smtp['smtp_port'],
                timeout=data_cdb_smtp['smtp_timeout']
            )

        except socket.gaierror:
            stat_smtp = STAT_LVL['crit']
            log = 'Attempt to send email failed due to unknown server.'
            logger.exception(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'ERROR',
                log
            ])

        except socket.timeout:
            stat_smtp = STAT_LVL['crit']
            log = 'Attempt to send email failed due to connection timeout.'
            logger.exception(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'ERROR',
                log
            ])

        except smtplib.SMTPConnectError:
            stat_smtp = STAT_LVL['crit']
            log = 'Attempt to connect to email server reached timeout ' +\
                  'of {0} sec.'.format(data_cdb_smtp['timeout'])
            logger.exception(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'ERROR',
                log
            ])

        except smtplib.SMTPServerDisconnected:
            stat_smtp = STAT_LVL['crit']
            log = 'Attempt to send email failed because client and ' +\
                  'server inadvertently disconnected.'
            logger.exception(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'ERROR',
                log
            ])

        except smtplib.SMTPException:
            stat_smtp = STAT_LVL['crit']
            log = 'Attempt to send email failed due to unspecified error.'
            logger.exception(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'ERROR',
                log
            ])

        if (not stat_smtp) and (data_cdb_smtp['smtp_password'] is not None):
            # Authenticate with smtp server
            try:
                pymail.login(
                    user=data_cdb_smtp['smtp_from'],
                    password=data_cdb_smtp['smtp_password']
                )

            except smtplib.SMTPAuthenticationError:
                stat_smtp = STAT_LVL['crit']
                log = 'Attempt to login to email server failed due to ' +\
                      'invalid credentials.'
                logger.exception(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'ERROR',
                    log
                ])

            except smtplib.SMTPException:
                stat_smtp = STAT_LVL['crit']
                log = 'Attempt to send email failed due to unspecified error.'
                logger.exception(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'ERROR',
                    log
                ])

        if not stat_smtp:
            try:
                # Send message packets through SMTP server
                pymail.sendmail(
                    from_addr=data_cdb_smtp['smtp_from'],
                    to_addrs=smtp_recipients,
                    msg=smtp_email_msg.as_string()
                )
                if data_cdb_sms['sms_enable']:
                    if len(sms_recipients) >= 1:
                        pymail.sendmail(
                            from_addr=data_cdb_smtp['smtp_from'],
                            to_addrs=sms_recipients,
                            msg=sms_email_msg.as_string()
                        )
                pymail.quit()

                log = 'Emails successfully sent.'
                logger.debug(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'DEBUG',
                    log
                ])
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'email',
                        stat_smtp
                    ]
                ])
                break

            except smtplib.SMTPException:
                stat_smtp = STAT_LVL['crit']
                log = 'Attempt to send emails failed due to unspecified error.'
                logger.debug(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'ERROR',
                    log
                ])

        time.sleep(5 * attempt)

    if stat_smtp:
        log = 'General failure to send emails.'
        logger.warning(log)
        MPQ_ACT.put_nowait([
            datetime.now().isoformat(' '),
            'WARNING',
            log
        ])
        MPQ_STAT.put_nowait([
            'base',
            [
                'email',
                stat_smtp
            ]
        ])
