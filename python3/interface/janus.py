import logging
import time
import usb
import usb1
from usb.core import find as finddev

__author__ = 'Brett McGuire, Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'interface'
logger = logging.getLogger(logfile)


class Janus:
    """
    Extensive rewrite to original library written by Brett McGuire,
    ported to Python 3.

    The object represents a notional four-lane interface that consists
    of a Microchip MCP-2221 USB to I2C adapter and a Texas Instruments
    TCA-9544A four-way I2C switch.

    Proper control message encoding (python sdata variable) and response
    message codes (python rdata variable) are found in the MCP-2221 datasheet.
    """

    # Setup global error message dictionary
    WRONG_HEADER_ERR = -1
    BUS_BUSY_ERR = -2
    DATA_READ_ERR = -3
    INVALID_DATA_ERR = -4
    DATA_LENGTH_ERR = -5
    USB_ERROR = -6
    USB_NOT_FOUND = -7

    ERR_MESSAGE = {
        WRONG_HEADER_ERR: 'Wrong USB header in reply.',
        BUS_BUSY_ERR: 'I2C bus is busy.',
        DATA_READ_ERR: 'Error reading data.',
        INVALID_DATA_ERR: 'MCP2221 received invalid data.',
        DATA_LENGTH_ERR: 'Supplied data exceeded 60 bytes: ',
        USB_ERROR: 'MCP2221 USB bus experienced an error.',
        USB_NOT_FOUND: 'MCP2221 Not Found'
    }

    def __init__(self):
        """
        Sets object attributes
        """
        # Clear existing USB handles to device
        self.handle = None

    def __get_device(self):
        """
        Determine if interface device is connected to USB hub
        """
        logger.debug('Attempting to find Janus Interface.')

        err_usb = self.USB_NOT_FOUND
        busses = usb.busses()

        # Cycle through USB busses
        for bus in busses:
            devices = bus.devices

            # Cycle through USB devices on bus
            for dev in devices:

                # Check for match to Microchip MCP-2221 Vendor and Product ID
                #
                # TODO v0.9.x: Vendor and Product ID should reflect Janus-specific interface
                # TODO v0.9.x: Vendor presently reflects Microchip MCP-2221.
                if (dev.idVendor == 0x04d8) and (dev.idProduct == 0x00dd):
                    err_usb = False

        if err_usb == self.USB_NOT_FOUND:
            log = self.ERR_MESSAGE[self.USB_NOT_FOUND]
            logger.critical(log)

        return err_usb

    def initialize(self):
        """
        Initializes the MCP2221 on the USB bus.
        """
        logger.debug('Attempting to initialize Janus Interface.')
        err_usb = self.USB_ERROR

        # Build Python USB handle to Microchip MCP-2221 Vendor and Product ID
        #
        # TODO: Vendor and Product ID should reflect Janus-specific interface
        # TODO: Vendor presently reflects Microchip MCP-2221.
        # TODO: Any USB device driven by Microchip MCP-2221 will connect
        # TODO: MCP-2221 on non-Janus interface board will produce errors
        try:
            context = usb1.USBContext()
            self.handle = context.openByVendorIDAndProductID(
                vendor_id=0x04d8,
                product_id=0x00dd
            )
            if self.handle.kernelDriverActive(interface=2):
                self.handle.detachKernelDriver(interface=2)
            self.handle.claimInterface(interface=2)
            logger.debug('Janus Interface Initialized.')
            err_usb = False

        except usb1.USBError:
            logger.critical('Janus Interface failed to initialize.')

        return err_usb

    def close(self):
        """
        Releases the MCP-2221 from the USB bus.
        """
        # Close Python USB handle
        try:
            self.handle.releaseInterface(interface=2)
            logger.debug('Janus interface closed.')

        except usb1.USBError:
            logger.exception('Could not close Janus Interface, perhaps it is already closed?')
    
    def __fill_buffer(
            self,
            ctl: str,
            data=None
    ):
        """
        Creates properly formatted and encoded USB buffer string.

        :param ctl: str
        :param data: list
        """
        # Retrieve byte-encoded string for control message
        str_buffer = self.__get_bytes(data=ctl)

        # If packet includes data, retrieve byte-encoded string for data, then add to buffer
        if data is not None:
            str_buffer += self.__get_bytes(data=data)

        return bytearray(str_buffer + bytes(64 - len(str_buffer)))
    
    def __get_bytes(
        self,
        data
    ):
        """
        Properly encodes data for USB buffer.

        :param data: bytes, str, int, list, or bytearray
        """
        # If incoming packet is already bytes type, return without changes.
        if isinstance(data, bytes):
            return data

        # If incoming packet is string type, convert to bytes and return.
        elif isinstance(data, str):
            return bytes(data, 'raw_unicode_escape')

        # If incoming packet is integer type, convert to bytes and return.
        elif isinstance(data, int):
            return bytes(chr(data), 'raw_unicode_escape')

        # if incoming packet is list type, convert elements to bytes and return.
        elif isinstance(data, list):
            return bytes(data)

        # If incoming packet is a byte array, convert elements to bytes and return.
        elif isinstance(data, bytearray):
            return bytes(data)

        # All other incoming data types are invalid.
        else:
            return self.INVALID_DATA_ERR

    def __send_ctrl_msg(
        self,
        sdata
    ):
        """
        Sends message across USB bus to MCP2221 device.

        :param sdata: str or bytearray
        """
        sdata = bytes(sdata)
        rdata = 0

        try:
            logger.debug('Attempting USB transaction.')
            usb_end_point = 131
            usb_time_out = 1000

            # Send data packet out to device
            self.handle.bulkWrite(
                endpoint=usb_end_point,
                data=sdata,
                timeout=usb_time_out
            )

            # Get response code from device
            rdata = self.handle.bulkRead(
                endpoint=usb_end_point,
                length=64,
                timeout=usb_time_out
            )
            err_ctl = False

        except usb1.USBError:
            err_ctl = self.__get_device()
            if err_ctl == self.USB_NOT_FOUND:
                log = self.ERR_MESSAGE[err_ctl]
            else:
                err_ctl = self.USB_ERROR
                log = self.ERR_MESSAGE[err_ctl]
            logger.critical(log)

        return rdata, err_ctl

    def __i2c_error(
        self,
        op: str,
        addr_i2c: int,
        addr_mem: int,
        sdata: bytearray,
        rdata: bytearray,
        err: int = None,
        data_len: int = None
    ):
        """
        Generates and logs i2c error messages.

        :param op: str
        :param addr_i2c: int
        :param addr_mem: int
        :param sdata: bytearray
        :param rdata: bytearray
        :param err: int
        :param data_len: int
        """
        log = 'I2C {0} error generated on device address {1}, '.format(op, addr_i2c) +\
              'memory {0}, operation: {1}.'.format(addr_mem, hex(sdata[0]))

        # If packet length is too long, log warning.
        if err == self.DATA_LENGTH_ERR:
            logger.warning(log)
            log = self.ERR_MESSAGE[err]
            log += 'Given {0} bytes.'.format(data_len)
            logger.warning(log)

        else:
            # If response command does not echo dispatched command, log warning.
            if rdata[0] != sdata[0]:
                logger.warning(log)
                err = self.WRONG_HEADER_ERR
                log = self.ERR_MESSAGE[err]
                logger.warning(log)
                logger.warning('Control message input:')
                logger.warning([
                    hex(i) for i in sdata[0:9]
                ])
                logger.warning('Control message output:')
                logger.warning([
                    hex(i) for i in rdata[0:9]
                ])

            # If response indicates device is busy, log warning.
            if (sdata[0] != 0x40) and (rdata[1] != 0x00):
                logger.warning(log)
                err = self.BUS_BUSY_ERR
                log = self.ERR_MESSAGE[err]
                logger.warning(log)
                logger.warning('Control message input:')
                logger.warning([
                    hex(i) for i in sdata[0:9]
                ])
                logger.warning('Control message output:')
                logger.warning([
                    hex(i) for i in rdata[0:9]
                ])

            # If response indicates a data read error, log warning.
            if (sdata[0] == 0x40) and (rdata[1] == 0x41):
                logger.warning(log)
                err = self.DATA_READ_ERR
                log = self.ERR_MESSAGE[err]
                logger.warning(log)
                logger.warning('Control message input:')
                logger.warning([
                    hex(i) for i in sdata[0:9]
                ])
                logger.warning('Control message output:')
                logger.warning([
                    hex(i) for i in rdata[0:9]
                ])

            # If response indicates an invalid data error, log warning.
            elif (sdata[0] == 0x40) and (rdata[3] == 0x7F):
                logger.warning(log)
                err = self.INVALID_DATA_ERR
                log = self.ERR_MESSAGE[err]
                logger.warning(log)
                logger.warning('Control message input:')
                logger.warning([
                    hex(i) for i in sdata[0:9]
                ])
                logger.warning('Control message output:')
                logger.warning([
                    hex(i) for i in rdata[0:9]
                ])

        return err

    def __cancel_i2c_transfer(
        self,
        addr_i2c: int
    ):
        """
        Cancels i2c messages.

        :param addr_i2c: int
        """
        logger.debug('Cancelling I2C request.')
        sdata = self.__fill_buffer(ctl='\x10\x00\x10')
        rdata, err_ctl = self.__send_ctrl_msg(sdata=sdata)
        switch_addr = 0x70

        err = True
        if not err_ctl:
            if rdata[2] == 0x00:
                log = 'I2C successfully canceled'
                logger.debug(log)
                err = False
            elif rdata[2] == 0x10:
                if (addr_i2c == switch_addr) or (addr_i2c == 0x7F):
                    log = 'Cancel on reserved address {0} failed, '.format(addr_i2c) +\
                          'perhaps disconnected?'
                    logger.warning(log)
                    err = False
                else:
                    log = 'I2C cancel needs more time, rechecking in 1 sec.'
                    logger.warning(log)
                    time.sleep(1)
            elif rdata[2] == 0x11:
                log = 'I2C cancel requested, bus is already idle.'
                logger.warning(log)
                err = False
            else:
                log = 'I2C cancel received bad response, rechecking in 1 sec.'
                logger.critical(log)
                time.sleep(1)

        return err

    def __usb_reset(self):
        """
        Sends the USB reset command.
        """
        logger.debug('Attempting to reset USB.')
        err = self.__get_device()

        if err != self.USB_NOT_FOUND:
            try:
                dev = finddev(
                    idVendor=0x04d8,
                    idProduct=0x00dd
                )
                dev.reset()

                # After USB device is reset, must reinitialize USB handle
                # and set interrupts enabled flag before servicing any
                # future interface requests.
                err = self.initialize()

                if not err:
                    err = self.__get_device()

                    if not err:
                        log = 'Device found, USB reset of Janus Interface succeeded.'
                        logger.info(log)

                        if not err:
                            err = self.interrupts_enable()

                    else:
                        log = 'Device not found, USB reset of Janus Interface failed.'
                        logger.critical(log)

            except usb.USBError:
                logger.critical('USB reset of Janus Interface failed.')

        else:
            logger.warning('Janus interface not found during attempted USB reset.')

        return err

    def __device_reset(self):
        """
        Sends the device reset command.
        """
        logger.debug('Attempting device reset of Janus interface.')

        err = self.__get_device()
        if not err:
            try:
                sdata = bytes(self.__fill_buffer('\x70\xab\xcd\xef'))
                usb_end_point = 131
                usb_time_out = 1000

                # This does not cut power to the MCP2221
                self.handle.bulkWrite(
                    endpoint=usb_end_point,
                    data=sdata,
                    timeout=usb_time_out
                )
                time.sleep(10)

                # After device is reset, must reinitialize USB handle
                # and set interrupts enabled flag before servicing any
                # future interface requests.
                err = self.initialize()
                if not err:
                    err = self.interrupts_enable()

                else:
                    log = 'Device reset of Janus Interface failed.'
                    logger.critical(log)

            except usb1.USBError:
                err = self.USB_ERROR
                logger.critical('Device reset of Janus Interface failed.')
                logger.critical('LIB USB would not accept reset command.')

        else:
            logger.warning('Janus interface not found during attempted device reset.')

        if not err:
            logger.debug('Device reset of Janus Interface succeeded.')

        return err

    def gpio_set_mode(
        self,
        pin: int,
        mode: str
    ):
        """
        Sets single GPIO pin direction.

        :param pin: int
        :param mode: str
        """
        logger.debug('Setting GPIO pin mode to: {0}.'.format(mode))
        err_ctl = True

        sdata = self.__fill_buffer(ctl='\x50')
        sdata[(pin * 4) + 4] = 0x01
        if mode == 'IN':
            sdata[(pin * 4) + 5] = 0x01
            rdata, err_ctl = self.__send_ctrl_msg(sdata=sdata)
        elif mode == 'OUT':
            sdata[(pin * 4) + 5] = 0x00
            rdata, err_ctl = self.__send_ctrl_msg(sdata=sdata)
        else:
            logger.critical('GPIO pin mode {0} not set to due '.format(mode) +
                            'to incorrect input mode.')

        if not err_ctl:
            logger.debug('GPIO pin mode set.')
        else:
            logger.critical('GPIO pin mode not set to due to USB error.')

        return err_ctl

    def gpio_set_mode_all(
        self,
        mode: str
    ):
        """
        Sets all GPIO pin directions.

        :param mode: str
        """
        logger.debug('Setting all GPIO pin modes to {0}.'.format(mode))
        err_ctl = True
        if mode == 'IN':
            sdata = self.__fill_buffer(
                ctl='\x60\x00\x00\x00\x00\x00\x00\xff\x08\x08\x08\x08'
            )
            rdata, err_ctl = self.__send_ctrl_msg(sdata)
        elif mode == 'OUT':
            sdata = self.__fill_buffer(
                ctl='\x60\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00'
            )
            rdata, err_ctl = self.__send_ctrl_msg(sdata=sdata)
        else:
            logger.critical('GPIO pin modes not set to due to incorrect input mode.')

        if not err_ctl:
            logger.debug('All GPIO pin modes set to {0}.'.format(mode))
        else:
            logger.critical('GPIO pin modes not set to due to USB error.')

        return err_ctl

    def gpio_read(
        self,
        pin: int
    ):
        """
        Reads from GPIO pin.

        :param pin: int
        """
        logger.debug('Reading from GPIO pin {0}.'.format(pin))
        sdata = self.__fill_buffer(ctl='\x51')
        rdata, err_ctl = self.__send_ctrl_msg(sdata=sdata)

        if not err_ctl:
            data = rdata[(2 * pin) + 2]
            logger.debug('Successfully read from GPIO pin {0}.'.format(pin))
        else:
            data = []
            logger.critical('GPIO pin {0} not read from due to USB error.'.format(pin))

        return data, err_ctl

    def gpio_write(
        self,
        pin: int,
        value: int
    ):
        """
        Writes to GPIO pin.

        :param pin: int
        :param value: int
        """
        logger.debug('Writing to GPIO pin {0} value {1}.'.format(pin, value))

        # Check for valid pin and mode values
        if (pin < 0) or (pin > 3) or (value < 0) or (value > 1):
            logger.critical(self.ERR_MESSAGE[self.INVALID_DATA_ERR])
            return self.INVALID_DATA_ERR

        sdata = self.__fill_buffer(ctl='\x50')
        sdata[pin * 4 + 2] = 0x01
        sdata[pin * 4 + 3] = value
        rdata, err_ctl = self.__send_ctrl_msg(sdata=sdata)

        if not err_ctl:
            logger.debug('Successfully wrote to GPIO pin {0} value {1}.'.format(pin, value))
        else:
            logger.critical('GPIO pin {0} not written to due to USB error.'.format(pin))

        return err_ctl

    def interrupts_enable(self):
        """
        Enables all GPIO pin interrupts.
        """
        logger.debug('Enabling interrupts.')
        # Enable GPIO operations on GPIO pins 0,2,3, and interrupts on GPIO pin 1.
        # MCP-2221 GPIO pin 1 is electrically tied to both TCA-945 INT and INT1 pins.
        sdata = self.__fill_buffer(
            ctl='\x60\x00\x00\x00\x00\x00\x00\xff\x00\x08\x00\x00'
        )
        rdata, err_ctl = self.__send_ctrl_msg(sdata=sdata)

        if not err_ctl:
            sdata = self.__fill_buffer(ctl='\x60\x00\x00\x00\x00\x00\x17')
            rdata, err_ctl = self.__send_ctrl_msg(sdata=sdata)

        if not err_ctl:
            logger.debug('Interrupts enabled.')
        else:
            logger.critical('Interrupts not enabled due to USB error.')

        return err_ctl

    def interrupt_check_flag(self):
        """
        Checks all GPIO pin interrupts.
        """
        logger.debug('Checking interrupt flags.')
        sdata = self.__fill_buffer(ctl='\x10')
        rdata, err_ctl = self.__send_ctrl_msg(sdata=sdata)

        if not err_ctl:
            # rdata[24] returns either a 0 or 1
            data = rdata[24]
            logger.debug('Interrupt flags checked.')
        else:
            data = []
            logger.critical('Interrupt flags not checked due to USB error.')

        return data, err_ctl

    def interrupt_clear_flag(self):
        """
        Clears all GPIO pin interrupts.
        """
        logger.debug('Clearing interrupt flags.')
        sdata = self.__fill_buffer(ctl='\x60\x00\x00\x00\x00\x00\x81')
        rdata, err_ctl = self.__send_ctrl_msg(sdata=sdata)

        if not err_ctl:
            logger.debug('Interrupt flags cleared.')
        else:
            logger.critical('Interrupts not cleared due to USB error.')

        return err_ctl

    def i2c_get_lane(self):
        """
        Gets I2C multiplexer lane.
        """
        logger.debug('Retrieving I2C lane.')
        switch_addr = 0x70
        addr_ln = 0
        data, err = self.i2c_read(
            addr_i2c=switch_addr,
            addr_mem=0,
            data_len=1,
            stage=1,
            reset=False
        )
        if not err:
            addr_ln = (int(data[0]) % 8) - 4
            logger.debug('I2C lane retrieval complete: lane {0}.'.format(addr_ln))

        return addr_ln, err

    def i2c_set_lane(
        self,
        addr_ln: int
    ):
        """
        Sets I2C multiplexer lane.

        :param addr_ln: int
        """
        logger.debug('Setting I2C lane.')
        switch_addr = 0x70
        if (addr_ln < 0) or (addr_ln > 3):
            return True, 0
        data_len, err = self.i2c_write(
            addr_i2c=switch_addr,
            addr_mem=(addr_ln + 4),
            data=[],
            reset=False
        )
        logger.debug('I2C lane set complete, error: {0}.'.format(err))
        return err

    def i2c_read(
        self,
        addr_i2c: int,
        addr_mem: int,
        data_len: int,
        stage: int = 0,
        reset: bool = True
    ):
        """
        Reads from I2C address.

        :param addr_i2c: int
        :param addr_mem: int
        :param data_len: int
        :param stage: int
        :param reset: bool

        This is a multi-attempt, multi-stage function with lots of error
        checking and recovery built in order to successfully retrieve data
        from and I2C device.
        """
        err = True
        rdata = 0

        if reset:
            attempts = 5
        else:
            attempts = 1

        for attempt in range(1, (attempts + 1)):
            log = 'Attempt {0} of {1} to read from I2C: addr {2}, mem {3}, length {4}.'.\
                  format(attempt, attempts, addr_i2c, addr_mem, data_len)
            logger.info(log)
            if stage == 0:
                logger.debug('Starting stage 0.')
                sdataw = self.__fill_buffer(ctl='\x90\x00\x00\x00')
                sdataw[1] = 1
                sdataw[3] = (addr_i2c << 1)
                sdataw[4] = addr_mem

                rdata, err_ctl = self.__send_ctrl_msg(sdata=sdataw)
                err_i2c = False

                if not err_ctl:
                    err_i2c = self.__i2c_error(
                        op='read',
                        addr_i2c=addr_i2c,
                        addr_mem=addr_mem,
                        sdata=sdataw,
                        rdata=rdata
                    )
                    logger.debug('I2C read stage 0 i2c err: {0}'.format(err_i2c))

                if err_ctl or err_i2c:
                    self.__cancel_i2c_transfer(addr_i2c=addr_i2c)

                    if reset:
                        if attempt == 2:
                            self.__usb_reset()

                        elif attempt == 3:
                            # MCP-2221 may not accept device reset, so follow
                            # with another USB reset
                            self.__device_reset()
                            time.sleep(4)
                            self.__usb_reset()

                        elif attempt > 3:
                            logger.critical('I2C read stage 0 failed after reset, nothing more to do.')
                            break

                    elif not reset and (attempt > 1):
                        logger.warning('I2C read stage 0 failed with no reset, nothing more to do.')
                        break

                    logger.warning('I2C read stage 0 unsuccessful, remaining at stage 0.')

                else:
                    stage = 1
                    logger.debug('I2C read stage 0 successful.')

            if stage == 1:
                err = True
                logger.debug('Starting stage 1.')
                time.sleep(0.005)
                sdatar = self.__fill_buffer(ctl='\x91')
                sdatar[1] = data_len
                sdatar[3] = ((addr_i2c << 1) | 0x01)

                rdata, err_ctl = self.__send_ctrl_msg(sdata=sdatar)
                err_i2c = False

                if not err_ctl:
                    err_i2c = self.__i2c_error(
                        op='read',
                        addr_i2c=addr_i2c,
                        addr_mem=addr_mem,
                        sdata=sdatar,
                        rdata=rdata
                    )
                    logger.debug('I2C read stage 1 i2c err: {0}'.format(err_i2c))

                if err_ctl or err_i2c:
                    self.__cancel_i2c_transfer(addr_i2c=addr_i2c)

                    if reset:
                        if attempt == 2:
                            self.__usb_reset()

                        elif attempt == 3:
                            # MCP-2221 may not accept device reset, so follow
                            # with another USB reset
                            self.__device_reset()
                            time.sleep(4)
                            self.__usb_reset()

                        elif attempt > 3:
                            logger.critical('I2C read stage 1 failed after reset, nothing more to do.')
                            break

                    elif not reset and (attempt > 1):
                        logger.warning('I2C read stage 1 failed with no reset, nothing more to do.')
                        break

                    stage = 0
                    logger.warning('I2C read stage 1 unsuccessful, returning to stage 0.')

                else:
                    stage = 2
                    logger.debug('I2C read stage 1 successful.')

            if stage == 2:
                logger.debug('Starting stage 2.')
                time.sleep(0.012)
                sdatar = self.__fill_buffer(ctl='\x40')
                rdata, err_ctl = self.__send_ctrl_msg(sdata=sdatar)
                err_i2c = False

                if not err_ctl:
                    err_i2c = self.__i2c_error(
                        op='read',
                        addr_i2c=addr_i2c,
                        addr_mem=addr_mem,
                        sdata=sdatar,
                        rdata=rdata
                    )
                    logger.debug('I2C read stage 2 i2c err: {0}'.format(err_i2c))

                if err_ctl or err_i2c:
                    self.__cancel_i2c_transfer(addr_i2c=addr_i2c)

                    if reset:
                        if attempt == 2:
                            self.__usb_reset()

                        elif attempt == 3:
                            self.__device_reset()
                            time.sleep(4)
                            self.__usb_reset()

                        elif attempt > 3:
                            logger.critical('I2C read stage 2 failed after reset, nothing more to do.')
                            break

                    elif not reset and (attempt > 1):
                        logger.warning('I2C read stage 2 failed with no reset, nothing more to do.')
                        break

                    stage = 0
                    logger.warning('I2C read stage 2 unsuccessful, returning to stage 0.')
                else:
                    err = False
                    logger.debug('I2C read stage 2 successful.')
                    log = 'I2C read complete after {0} attempts: '.format(attempt) +\
                          'addr {0}, mem {1}, length {2}.'.format(addr_i2c, addr_mem, data_len)
                    logger.debug(log)
                    break

            time.sleep(0.005)

        if not err:
            data_out = [int(i) for i in rdata[4:(4 + data_len)]]
            return data_out, err
        else:
            return rdata, err

    def i2c_write(
        self,
        addr_i2c: int,
        addr_mem: int,
        data: list,
        reset: bool = True
    ):
        """
        Writes to I2C address.

        :param addr_i2c: int
        :param addr_mem: int
        :param data: list
        :param reset: bool
        """
        wsdata = self.__get_bytes(data=addr_mem) + self.__get_bytes(data=data)
        data_len = len(wsdata)

        if reset:
            attempts = 5
        else:
            attempts = 1

        err = True
        if data_len < 60:
            for attempt in range(1, (attempts + 1)):
                log = 'Attempt {0} of {1} to write to I2C: addr {2}, mem {3}, length {4}'.\
                      format(attempt, attempts, addr_i2c, addr_mem, (data_len - 1))
                logger.debug(log)
                sdata = self.__fill_buffer(
                    ctl='\x92\x00\x00\x00',
                    data=wsdata
                )
                sdata[1] = data_len
                sdata[3] = (addr_i2c << 1)

                rdata, err_ctl = self.__send_ctrl_msg(sdata=sdata)

                err_i2c = False

                if not err_ctl:
                    err_i2c = self.__i2c_error(
                        op='write',
                        addr_i2c=addr_i2c,
                        addr_mem=addr_mem,
                        sdata=sdata,
                        rdata=rdata
                    )
                    logger.debug('I2C write i2c err: {0}'.format(err_i2c))

                if err_ctl or err_i2c:
                    self.__cancel_i2c_transfer(addr_i2c=addr_i2c)

                    if reset:
                        if attempt == 2:
                            self.__usb_reset()

                        elif attempt == 3:
                            # MCP-2221 may not accept device reset, so follow
                            # with another USB reset
                            self.__device_reset()
                            time.sleep(4)
                            self.__usb_reset()

                        else:
                            logger.critical('I2C write operation failed, nothing more to do')
                            break

                    elif not reset and (attempt > 1):
                        logger.warning('I2C write failed with no reset, nothing more to do.')
                        break

                    logger.warning('I2C write operation unsuccessful')

                else:
                    err = False
                    log = 'I2C write complete after {0} attempts: '.format(attempt) +\
                          'addr {0}, mem {1}, length {2}.'.\
                          format(addr_i2c, addr_mem, (data_len - 1))
                    logger.debug(log)
                    break

        else:
            sdata = self.__fill_buffer(ctl='\x00')
            rdata = self.__fill_buffer(ctl='\x00')
            err = self.__i2c_error(
                op='write',
                addr_i2c=addr_i2c,
                addr_mem=addr_mem,
                sdata=sdata,
                rdata=rdata,
                err=self.DATA_LENGTH_ERR,
                data_len=data_len
            )

        return (data_len - 1), err
