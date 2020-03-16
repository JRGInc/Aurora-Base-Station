import logging
from datetime import datetime
from interface.memorymap import MMAP
from shared import dbase
from shared.globals import MPQ_ACT, STAT_LVL, MPQ_CMD4

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'interface'
logger = logging.getLogger(logfile)


class Control(
    object
):
    """
    Module LED Controls
    """

    def __init__(
        self
    ):
        """
        Sets object attributes

        LED Control Arrays
        0: LED Effect
        1: LED Primary Red Intensity
        2: LED Primary Green Intensity
        3: LED Primary Blue Intensity
        4: LED Secondary Red Intensity
        5: LED Secondary Green Intensity
        6: LED Secondary Blue Intensity
        7: LED Effect Duration (secs to 240 secs)
        8: LED Effect Period (40 msec increments to 10 seconds)
        9: LED Effect Duty Cycle (percentage)

        v0.10.2 Effects
        0 = Disable
        1 = Static
        2 = Blink
        3 = Heartbeat
        """
        self.dict_led_settings = {
            'disable': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'locate': [1, 255, 255, 255, 0, 0, 0, 240, 250, 100],
            'sensor_low': [2, 0, 0, 255, 0, 0, 0, 15, 125, 50],     # 3x red 2.5 sec pulse with 2.5 off
            'sensor_high': [2, 255, 0, 0, 0, 0, 0, 15, 125, 50],    # 3x blue 2.5 sec pulse with 2.5 off
            'heartbeat': [3, 0, 255, 0, 0, 0, 0, 240, 0, 0]
        }

    def effect(
        self,
        led_effect: str,
        mod_uid: str,
        addr_ln: int,
        addr_mod: int,
    ):
        """
        Disables LEDs on module

        :param led_effect: string
        :param mod_uid: string
        :param addr_ln: int
        :param addr_mod: int
        """
        data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
            cdb_cmd='get_doc',
            cdb_name='modconfig',
            cdb_doc=mod_uid,
            logfile=logfile,
            attempts=1
        )

        if not stat0_cdb:
            if data0_cdb_out['status'] < STAT_LVL['crit']:
                addr_mem = MMAP[data0_cdb_out['mem_map_ver']]['LED_ALL'][0]

                MPQ_CMD4.put([
                    mod_uid,
                    addr_ln,
                    addr_mod,
                    addr_mem,
                    self.dict_led_settings[led_effect]
                ])

        else:
            log = 'Could not complete module LED {0} process due to CouchDB error.'.format(led_effect)
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
