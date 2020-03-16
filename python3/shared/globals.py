import multiprocessing
from typing import TypeVar


__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'


# Global websocket queues
MPQ_WS = multiprocessing.Queue(-1)  # Heartbeat messages

# Global status queue
MPQ_LN_SETUP = multiprocessing.Queue(-1)
MPQ_STAT = multiprocessing.Queue(-1)  # Heartbeat statements
MPQ_ACT = multiprocessing.Queue(-1)  # Heartbeat statements
MPQ_ACT_CMD = multiprocessing.Queue(-1)  # Heartbeat statements

# Global status level dictionary
# Operational level is 0 to allow for simplified Python conditional statements
STAT_LVL = {'op': 0,        # Operational
            's_evt': 1,     # Sensor event
            'op_evt': 2,    # Operational event
            'op_err': 3,    # Operational error
            'crit': 4,      # Critical error
            'not_cfg': 5,   # Not configured/setup
            'cfg_err': 6,   # Configuration/setup error
            'undeter': 7,   # Undetermined status
            'not_trk': 8    # Not tracked
            }

# Logging level dictionary
LOG_LVL = {'DEBUG': 10,
           'INFO': 20,
           'WARNING': 30,
           'ERROR': 40,
           'CRITICAL': 50,
           }

# Global lane and interface queues used during JanusESS startup sequence
MPQ_IFACE_SETUP = multiprocessing.Queue(-1)

# Global command queues
MPQ_CMD0 = multiprocessing.Queue(-1)  # Commands to execute
MPQ_CMD1 = multiprocessing.Queue(-1)  # Neighbor bus trigger events
MPQ_CMD2 = multiprocessing.Queue(-1)  # Link setup
MPQ_CMD3 = multiprocessing.Queue(-1)  # On demand polling of module
MPQ_CMD4 = multiprocessing.Queue(-1)  # Write values to module
MPQ_CMD5 = multiprocessing.Queue(-1)  # Routine cyclic polling
FLAG_LNRST = [
    False,
    False,
    False,
    False
]
AUTO_LNRST = [
    0,
    0,
    0,
    0
]

TYPE_INTERFACE = TypeVar('TYPE_INTERFACE')

MPQ_FLAG_LOG = multiprocessing.Queue(-1)

# Global polling queues
MPQ_POLL_START = multiprocessing.Queue(-1)
MPQ_POLL_STOP = multiprocessing.Queue(-1)
MPQ_POLL_COMPLETE = multiprocessing.Queue(-1)
MPQ_POLL_LOG_DISP = multiprocessing.Queue(-1)
MPQ_POLL_LOG_DATA = multiprocessing.Queue(-1)

MPQ_SETUP_LOG_RESET = multiprocessing.Queue(-1)
MPQ_SETUP_LOG_INIT = multiprocessing.Queue(-1)

MPQ_NETINT = multiprocessing.Queue(-1)  # Network intervals

# Global log level queue
MPQ_LOG_LVL = multiprocessing.Queue(-1)

# Global SNMP globals
MPQ_SNMPA2 = multiprocessing.Queue(-1)
MPQ_SNMPA3 = multiprocessing.Queue(-1)
MPQ_SNMPA4 = multiprocessing.Queue(-1)
MPQ_SNMPA5 = multiprocessing.Queue(-1)
MPQ_SNMPA_STOP = multiprocessing.Queue(-1)
MPQ_SNMPN2 = multiprocessing.Queue(-1)
MPQ_SNMPN3 = multiprocessing.Queue(-1)
MPQ_SNMPN4 = multiprocessing.Queue(-1)
MPQ_SNMPN5 = multiprocessing.Queue(-1)
MPQ_SNMPN_STOP = multiprocessing.Queue(-1)
