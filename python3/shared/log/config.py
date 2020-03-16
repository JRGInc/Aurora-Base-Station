import logging
import os
from shared.messaging.smtp import send_mail


# Log paths and files
LOGPATH = os.path.normpath(os.getenv('JANUSESS_CORE_LOG_PATH',
                                     '/var/log/JanusESS/'))  # Log path
activity = os.path.join(LOGPATH, 'activity')  # Log file
janusess = os.path.join(LOGPATH, 'janusess')  # Log file
setup = os.path.join(LOGPATH, 'setup')  # Log file
polling = os.path.join(LOGPATH, 'polling')  # Log file
tasks = os.path.join(LOGPATH, 'tasks')  # Log file
server = os.path.join(LOGPATH, 'server')  # Log file
interface = os.path.join(LOGPATH, 'interface')  # Log file
heartbeat = os.path.join(LOGPATH, 'heartbeat')  # Log file
command = os.path.join(LOGPATH, 'command')  # Log file
conversion = os.path.join(LOGPATH, 'conversion')  # Log file


class Logging(object):
    def __init__(self):
        self.config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'format': '%(levelname)s %(message)s',
                },
                'verbose': {
                    'format': " * %(asctime)s * %(levelname)s: " +
                              "<function '%(funcName)s' from '%(filename)s'>: %(message)s",
                },
            },
            'loggers': {
                'activity': {
                    'handlers': ['activity'],
                    'propagate': False,
                    'level': 'INFO',
                },
                'janusess': {
                    'handlers': ['janusess', 'email'],
                    'propagate': False,
                    'level': 'INFO',
                },
                'command': {
                    'handlers': ['command', 'email'],
                    'propagate': False,
                    'level': 'INFO',
                },
                'conversion': {
                    'handlers': ['conversion', 'email'],
                    'propagate': True,
                    'level': 'INFO',
                },
                'email': {
                    'handlers': ['janusess'],
                    'propagate': True,
                    'level': 'INFO',
                },
                'heartbeat': {
                    'handlers': ['heartbeat', 'email'],
                    'propagate': True,
                    'level': 'INFO',
                },
                'interface': {
                    'handlers': ['interface', 'email'],
                    'propagate': True,
                    'level': 'INFO',
                },
                'polling': {
                    'handlers': ['polling', 'email'],
                    'propagate': True,
                    'level': 'INFO',
                },
                'server': {
                    'handlers': ['server', 'email'],
                    'propagate': True,
                    'level': 'INFO',
                },
                'setup': {
                    'handlers': ['setup', 'email'],
                    'propagate': True,
                    'level': 'INFO',
                },
                'tasks': {
                    'handlers': ['tasks', 'email'],
                    'propagate': True,
                    'level': 'INFO',
                },
            },
            'handlers': {
                'activity': {
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': activity,
                    'maxBytes': 8192000,
                    'backupCount': 40,
                },
                'janusess': {
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': janusess,
                    'maxBytes': 8192000,
                    'backupCount': 40,
                },
                'command': {
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': command,
                    'maxBytes': 8192000,
                    'backupCount': 40,
                },
                'conversion': {
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': conversion,
                    'maxBytes': 8192000,
                    'backupCount': 40,
                },
                'heartbeat': {
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': heartbeat,
                    'maxBytes': 8192000,
                    'backupCount': 40,
                },
                'interface': {
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': interface,
                    'maxBytes': 8192000,
                    'backupCount': 40,
                },
                'polling': {
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': polling,
                    'maxBytes': 8192000,
                    'backupCount': 40,
                },
                'server': {
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': server,
                    'maxBytes': 8192000,
                    'backupCount': 40,
                },
                'setup': {
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': setup,
                    'maxBytes': 8192000,
                    'backupCount': 40,
                },
                'tasks': {
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': tasks,
                    'maxBytes': 8192000,
                    'backupCount': 40,
                },
                'console': {
                    'level': 'DEBUG',
                    'formatter': 'simple',
                    'class': 'logging.StreamHandler',
                },
                'email': {
                    'level': 'ERROR',
                    'formatter': 'verbose',
                    'class': 'shared.log.config.EmailHandler',
                },
            }
        }


class EmailHandler(logging.Handler):
    def emit(self, record):
        return send_mail(
            msg_type='error_dispatch',
            args=[record]
        )
