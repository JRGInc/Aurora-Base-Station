import logging
from datetime import datetime
from interface.janus import Janus
from shared import dbase
from shared.globals import STAT_LVL, MPQ_ACT, MPQ_STAT

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'interface'
logger = logging.getLogger(logfile)


class Interface(
    object
):
    """
    System GPIO processes
    """

    def __init__(
        self
    ):
        """
        Sets object attributes
        """
        # Set default to single-lane interface
        self.err_iface = 0

        # Current lane address of interface board, set only if different
        self.addr_ln = None

        # Instantiation clears any previous USB device handles pertaining to interface
        self.obj_janus = Janus()
        self.setup()

    def setup(
        self
    ):
        """
        Setups USB connection to interface board
        """
        # Establish a new persistent USB handle with the interface device.
        #
        # Returns False if no error, negative integer for error type.
        err_iface = self.obj_janus.initialize()

        if not err_iface:

            # Get lane call produces error if four-lane interface is not connected.
            # This is the only way to programmatically differentiate between single- and
            # four-lane interface boards.
            #
            # First return value is 0 through 3 if lane is set, negative integer otherwise.
            # Second return value is False if no error, negative integer for error type.
            addr_ln, err_iface = self.obj_janus.i2c_get_lane()

            # If no error returned, set to four-lane interface
            if not err_iface:
                self.addr_ln = addr_ln
                log = 'Four-lane Janus Interface detected.'
                logger.info(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'INFO',
                    log
                ])
                print(log)
            else:
                self.err_iface = 4
                log = 'Could not detect Four-lane Janus Interface.'
                logger.warning(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'INFO',
                    log
                ])
                print(log)

        # Update core document in CouchDB config database
        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='upd_doc',
            cdb_name='config',
            cdb_doc='core',
            data_cdb_in={'interface': self.err_iface},
            logfile=logfile
        )

        if stat_cdb:
            log = 'Could not update Janus Interface type in CouchDB.'
            logger.warning(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'WARNING',
                log
            ])

    def close(
        self
    ):
        """
        Closes USB connection to device
        """
        self.obj_janus.close()

    def error_iface(
        self
    ):
        """
        Retrieves number of link networks

        :return number_links: int
        """
        return self.err_iface

    def gpio_read(
        self,
        addr_ln: int,
        mode: bool = True,
        stat_en: bool = True,
        attempts: int = 2
    ):
        """
        Reads GPIO pin value

        :param addr_ln: int
        :param mode: bool
        :param stat_en: bool
        :param attempts: int

        :return data_iface_out: int (0/1 if STAT_LVL['op'])
        :return stat_iface: STAT_LVL['op'] or STAT_LVL['crit']
        """
        attempt = 0
        err_iface = True
        data_iface_out = None

        stat_iface = STAT_LVL['op']

        # Cycle through attempts
        for attempt in range(1, (attempts + 1)):

            # If mode flag is set, set GPIO mode to 'IN' prior to GPIO read
            if mode:
                err_iface = self.obj_janus.gpio_set_mode(
                    pin=addr_ln,
                    mode='IN'
                )

                if not err_iface:
                    data_iface_out, err_iface = self.obj_janus.gpio_read(pin=addr_ln)

            else:
                data_iface_out, err_iface = self.obj_janus.gpio_read(pin=addr_ln)

            if err_iface:
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'interface',
                        STAT_LVL['op_err']
                    ]
                ])

                # Only log warning on last attempt, keeps log clean
                if attempt == attempts:
                    log = 'Attempt {0} of {1} to '.format(attempt, attempts) + \
                          'read GPIO pin {0} failed.'.format(addr_ln)
                    logger.warning(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'WARNING',
                        log
                    ])

            else:
                break

        if err_iface:
            log = 'General IO failure to read GPIO pin {0}.'.format(addr_ln)
            logger.critical(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
            stat_iface = STAT_LVL['crit']
            print(log)

        else:
            log = 'Successfully read GPIO pin {0} after {1} attempts.'.\
                  format(addr_ln, attempt)
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'DEBUG',
                log
            ])

        if stat_en:
            MPQ_STAT.put_nowait([
                'base',
                [
                    'interface',
                    stat_iface
                ]
            ])

        return data_iface_out, stat_iface

    def gpio_write(
        self,
        addr_ln: int,
        data_iface_in: int,
        mode: bool = True,
        stat_en: bool = True,
        attempts: int = 2
    ):
        """
        Sets GPIO pin to output LOW signal

        :param addr_ln: int
        :param data_iface_in: int (0 or 1)
        :param mode: bool
        :param stat_en: bool
        :param attempts: int

        :return stat_iface: STAT_LVL['op'] or STAT_LVL['crit']
        """
        attempt = 0
        err_iface = True
        stat_iface = STAT_LVL['op']

        # Cycle through attempts
        for attempt in range(1, (attempts + 1)):

            # If mode flag is set, set GPIO mode to 'OUT' prior to GPIO write
            if mode:
                err_iface = self.obj_janus.gpio_set_mode(
                    pin=addr_ln,
                    mode='OUT'
                )
                if not err_iface:
                    err_iface = self.obj_janus.gpio_write(
                        pin=addr_ln,
                        value=data_iface_in
                    )
            else:
                err_iface = self.obj_janus.gpio_write(
                    pin=addr_ln,
                    value=data_iface_in
                )

            if err_iface:
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'interface',
                        STAT_LVL['op_err']
                    ]
                ])

                # Only log warning on last attempt, keeps log clean
                if attempt == attempts:
                    log = 'Attempt {0} of {1} to '.format(attempt, attempts) + \
                          'set GPIO pin {0} to value {1} failed.'.format(addr_ln, data_iface_in)
                    logger.warning(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'WARNING',
                        log
                    ])

            else:
                break

        if err_iface:
            log = 'General IO failure to set GPIO pin {0} to value {1}.'.\
                  format(addr_ln, data_iface_in)
            logger.critical(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
            stat_iface = STAT_LVL['crit']
            print(log)

        else:
            log = 'Successfully set GPIO pin {0} to value {1} after {2} attempts.'.\
                  format(addr_ln, data_iface_in, attempt)
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'DEBUG',
                log
            ])

        if stat_en:
            MPQ_STAT.put_nowait([
                'base',
                [
                    'interface', stat_iface
                ]
            ])

        return stat_iface

    def interrupts_enable(
        self,
        attempts: int = 2,
        stat_en: bool = True
    ):
        """
        Enables GPIO interrupt

        :param attempts: int
        :param stat_en: bool

        :return stat_iface: STAT_LVL['op'] or STAT_LVL['crit']
        """
        attempt = 0
        err_iface = True
        stat_iface = STAT_LVL['op']

        # Cycle through attempts
        for attempt in range(1, (attempts + 1)):
            err_iface = self.obj_janus.interrupts_enable()

            if err_iface:
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'interface',
                        STAT_LVL['op_err']
                    ]
                ])

                # Only log warning on last attempt, keeps log clean
                if attempt == attempts:
                    log = 'Attempt {0} of {1} to '.format(attempt, attempts) + \
                          'enable GPIO interrupts failed.'
                    logger.warning(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'WARNING',
                        log
                    ])

            else:
                break

        if err_iface:
            log = 'General IO failure to enable GPIO interrupts.'
            logger.critical(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
            stat_iface = STAT_LVL['crit']
            print(log)

        else:
            log = 'Successfully enabled GPIO interrupts after {0} attempts.'.\
                  format(attempt)
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'DEBUG',
                log
            ])

        if stat_en:
            MPQ_STAT.put_nowait([
                'base',
                [
                    'interface',
                    stat_iface
                ]
            ])

        return stat_iface

    def interrupt_check_flag(
        self,
        attempts: int = 2,
        stat_en: bool = True
    ):
        """
        Checks GPIO interrupt

        :param attempts: int
        :param stat_en: bool

        :return data_iface_out: int (0/1 if STAT_LVL['op'])
        :return stat_iface: STAT_LVL['op'] or STAT_LVL['crit']
        """
        attempt = 0
        err_iface = True
        stat_iface = STAT_LVL['op']
        data_iface_out = None

        # Cycle through attempts
        for attempt in range(1, (attempts + 1)):

            # There is only one interrupt flag for all four lanes.  Therefore
            # no method exists to isolate which of the four GPIOs were triggered.
            data_iface_out, err_iface = self.obj_janus.interrupt_check_flag()

            if err_iface:
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'interface',
                        STAT_LVL['op_err']
                    ]
                ])

                # Only log warning on last attempt, keeps log clean
                if attempt == attempts:
                    log = 'Attempt {0} of {1} to '.format(attempt, attempts) + \
                          'check GPIO interrupt flag failed.'
                    logger.warning(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'WARNING',
                        log
                    ])
            else:
                break

        if err_iface:
            log = 'General IO failure to check GPIO interrupt flag.'
            logger.critical(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
            stat_iface = STAT_LVL['crit']
            print(log)

        else:
            log = 'Successfully checked GPIO interrupt flag after {0} attempts.'.\
                  format(attempt)
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'DEBUG',
                log
            ])

        if stat_en:
            MPQ_STAT.put_nowait([
                'base',
                [
                    'interface', stat_iface
                ]
            ])

        return data_iface_out, stat_iface

    def interrupt_clear_flag(
        self,
        attempts: int = 3,
        stat_en: bool = True
    ):
        """
        Clears GPIO interrupt

        :param attempts: int
        :param stat_en: bool

        :return stat_iface: STAT_LVL['op'] or STAT_LVL['crit']
        """
        attempt = 0
        err_iface = True
        stat_iface = STAT_LVL['op']

        # Cycle through attempts
        for attempt in range(1, (attempts + 1)):
            err_iface = self.obj_janus.interrupt_clear_flag()

            if err_iface:
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'interface',
                        STAT_LVL['op_err']
                    ]
                ])

                # Only log warning on last attempt, keeps log clean
                if attempt == attempts:
                    log = 'Attempt {0} of {1} to '.format(attempt, attempts) + \
                          'clear GPIO interrupt flag failed.'
                    logger.warning(log)
                    MPQ_ACT.put_nowait([
                        datetime.now().isoformat(' '),
                        'WARNING',
                        log
                    ])

            else:
                break

        if err_iface:
            log = 'General IO failure to clear GPIO interrupt flag.'
            logger.critical(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'CRITICAL',
                log
            ])
            stat_iface = STAT_LVL['crit']
            print(log)

        else:
            log = 'Successfully cleared GPIO interrupt flag after {0} attempts.'. \
                  format(attempt)
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'DEBUG',
                log
            ])

        if stat_en:
            MPQ_STAT.put_nowait([
                'base',
                [
                    'interface',
                    stat_iface
                ]
            ])

        return stat_iface

    def i2c_lane_set(
        self,
        addr_ln: int,
        stat_en: bool = True,
        attempts: int = 3
    ):
        """
        Sets lane for I2C network

        :param addr_ln: int
        :param stat_en: bool
        :param attempts: int

        :return stat_iface: STAT_LVL['op'] or STAT_LVL['crit']
        """
        attempt = 0
        err_iface = False
        stat_iface = STAT_LVL['op']

        # Cycle through attempts
        if addr_ln != self.addr_ln:

            for attempt in range(1, (attempts + 1)):
                err_iface = self.obj_janus.i2c_set_lane(addr_ln=addr_ln)

                if err_iface:
                    err_iface = True
                    if stat_en:
                        MPQ_STAT.put_nowait([
                            'base',
                            [
                                'interface',
                                STAT_LVL['op_err']
                            ]
                        ])

                    # Only log warning on last attempt, keeps log clean
                    if attempt == attempts:
                        log = 'Attempt {0} of {1} to '.format(attempt, attempts) + \
                              'set interface to lane {0} failed.'.format(addr_ln)
                        logger.warning(log)
                        MPQ_ACT.put_nowait([
                            datetime.now().isoformat(' '),
                            'WARNING',
                            log
                        ])

                else:
                    err_iface = False
                    self.addr_ln = addr_ln
                    break

        if err_iface:
            stat_iface = STAT_LVL['op_err']
            if stat_en:
                MPQ_STAT.put_nowait([
                    'base',
                    [
                        'interface',
                        stat_iface
                    ]
                ])
            log = 'Set lane {0} on four port interface failed.'.format(addr_ln)
            logger.critical(log)

        else:
            log = 'Set lane {0} on four port interface succeeded after {1} attempts.'. \
                format(addr_ln, attempt)
            logger.info(log)

        return stat_iface

    def i2c_read(
        self,
        addr_ln: int,
        addr_mod: int,
        addr_mem: int,
        data_len: int,
        stat_en: bool = True,
        attempts: int = 1
    ):
        """
        Reads block of bytes from I2C network

        :param addr_ln: int
        :param addr_mod: int
        :param addr_mem: int
        :param data_len: int
        :param stat_en: bool
        :param attempts: int

        :return data_iface_out: list (if STAT_LVL['op'])
        :return data_iface_out: 0 (if STAT_LVL['crit'])
        :return stat_iface: STAT_LVL['op'] or STAT_LVL['crit']
        """
        # Janus interfaces allow for 64 byte transfers, including 5 or 6 bytes of
        # addressing header information.  Modules use an memory map that is
        # 256 or 512 bytes in length, therefore breaking data into 32 byte blocks
        # is more convenient to track and error-check than 58- or 59-byte blocks.
        packet_length = 48
        number_packets = data_len // packet_length
        number_bytes = data_len % packet_length

        attempt = 0
        data_iface_out = []
        err_iface = False
        stat_iface = STAT_LVL['op']

        # Cycle through all whole blocks
        for packet in range(0, (number_packets + 1)):
            data_addr = ((packet * packet_length) + addr_mem)
            if packet < number_packets:
                data_length = packet_length
            else:
                data_length = number_bytes
            # Cycle through attempts
            for attempt in range(1, (attempts + 1)):

                # Module 0x7F read begins at later failure stage and uses
                # less corrective actions on failure to reduce setup time.
                if addr_mod == 127:
                    data_out, err_iface = self.obj_janus.i2c_read(
                        addr_i2c=addr_mod,
                        addr_mem=data_addr,
                        data_len=data_length,
                        reset=False
                    )

                else:
                    data_out, err_iface = self.obj_janus.i2c_read(
                        addr_i2c=addr_mod,
                        addr_mem=data_addr,
                        data_len=data_length
                    )

                if err_iface:

                    # Only process errors on attempts for non-0x7F I2C addresses
                    if addr_mod != 127:
                        MPQ_STAT.put_nowait([
                            'base',
                            [
                                'interface',
                                STAT_LVL['op_err']
                            ]
                        ])

                        # Only log warning on last attempt, keeps log clean
                        if attempt == attempts:
                            log = 'Attempt {0} of {1} to '.format(attempt, attempts) + \
                                  'read packet {0} from I2C '.format(packet) +\
                                  'link {0} module {1} failed.'.format(addr_ln, addr_mod)
                            logger.warning(log)
                            MPQ_ACT.put_nowait([
                                datetime.now().isoformat(' '),
                                'WARNING',
                                log
                            ])
                    else:
                        break

                else:
                    # Add retrieved data to the end of the Python list variable
                    data_iface_out.extend(data_out)
                    break

            if err_iface:
                break

        if err_iface:
            data_iface_out = []

            # Only process errors on attempts for non-0x7F I2C addresses
            if addr_mod != 127:
                log = 'General IO failure to read data from lane {0} module {1}.'.\
                      format(addr_ln, addr_mod)
                logger.critical(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'CRITICAL',
                    log
                ])
                print(log)
                stat_iface = STAT_LVL['crit']
            else:
                stat_iface = STAT_LVL['op_err']

        else:
            log = 'Successfully read data from lane {0} '.format(addr_ln) + \
                  'module {0} memory {1} length {2} '.format(addr_mod, addr_mem, data_len) +\
                  'after {0} attempts.'.format(attempt)
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'DEBUG',
                log
            ])

        if stat_en:
            MPQ_STAT.put_nowait([
                'base',
                [
                    'interface',
                    stat_iface
                ]
            ])

        return data_iface_out, stat_iface

    def i2c_write(
        self,
        addr_ln: int,
        addr_mod: int,
        addr_mem: int,
        data_iface_in: list,
        stat_en: bool = True,
        attempts: int = 1
    ):
        """
        Writes block of bytes to I2C network

        :param addr_ln: int
        :param addr_mod: int
        :param addr_mem: int
        :param data_iface_in: list
        :param stat_en: bool
        :param attempts: int

        :return stat_iface: STAT_LVL['op'] or STAT_LVL['crit']
        """
        data_len = len(data_iface_in)
        packet_length = 24
        number_packets = data_len // packet_length

        attempt = 0
        err_iface = False
        stat_iface = STAT_LVL['op']

        # Cycle through all whole blocks
        for packet in range(0, (number_packets + 1)):

            if packet < number_packets:
                data_in = data_iface_in[(packet * packet_length):packet_length]
            else:
                data_in = data_iface_in[(packet * packet_length):]

            # Cycle through attempts
            for attempt in range(1, (attempts + 1)):

                # Module 0x7F write begins at later failure stage and uses
                # less corrective actions on failure to reduce setup time.

                if addr_mod == 127:
                    data_out, err_iface = self.obj_janus.i2c_write(
                        addr_i2c=addr_mod,
                        addr_mem=((packet * packet_length) + addr_mem),
                        data=data_in,
                        reset=False
                    )
                else:
                    data_out, err_iface = self.obj_janus.i2c_write(
                        addr_i2c=addr_mod,
                        addr_mem=((packet * packet_length) + addr_mem),
                        data=data_in
                    )

                if err_iface:

                    # Only process errors on attempts for non-0x7F I2C addresses
                    if addr_mod != 127:
                        MPQ_STAT.put_nowait([
                            'base',
                            [
                                'interface',
                                STAT_LVL['op_err']
                            ]
                        ])

                        # Only log warning on last attempt, keeps log clean
                        if attempt == attempts:
                            log = 'Attempt {0} of {1} to '.format(attempt, attempts) + \
                                  'write packet {0} to I2C '.format(packet) + \
                                  'link {0} module {1} failed.'.format(addr_ln, addr_mod)
                            logger.warning(log)
                            MPQ_ACT.put_nowait([
                                datetime.now().isoformat(' '),
                                'WARNING',
                                log
                            ])
                    else:
                        break

                else:
                    break

            if err_iface:
                break

        if err_iface:

            # Only process errors on attempts for non-0x7F I2C addresses
            if addr_mod != 127:
                log = 'General IO failure to write data to lane {0} module {1}.'. \
                    format(addr_ln, addr_mod)
                logger.critical(log)
                MPQ_ACT.put_nowait([
                    datetime.now().isoformat(' '),
                    'CRITICAL',
                    log
                ])
                print(log)
                stat_iface = STAT_LVL['crit']
            else:
                stat_iface = STAT_LVL['op_err']

        else:
            log = 'Successfully write data to lane {0} '.format(addr_ln) + \
                  'module {0} memory {1} length {2} '.format(addr_mod, addr_mem, data_len) + \
                  'after {0} attempts.'.format(attempt)
            logger.info(log)
            MPQ_ACT.put_nowait([
                datetime.now().isoformat(' '),
                'DEBUG',
                log
            ])

        if stat_en:
            MPQ_STAT.put_nowait([
                'base',
                [
                    'interface',
                    stat_iface
                ]
            ])

        return stat_iface
