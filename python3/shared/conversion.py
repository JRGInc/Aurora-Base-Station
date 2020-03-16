import logging
from pint import UnitRegistry

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'conversion'
logger = logging.getLogger(logfile)


class Conversion(
    object
):
    def __init__(
        self
    ):
        """
        Setup conversion properties
        """
        self.ureg = UnitRegistry()

        # Temperature conversions
        self.ureg.define('degC = degK; offset: 273.15 = celsius')
        self.ureg.define('degCS = degK = celsius_step')
        self.ureg.define('degF = 5 / 9 * degK; offset: 255.372222 = fahrenheit')
        self.ureg.define('degFS = 5 / 9 * degK; offset: 0 = fahrenheit_step')

        # Pressure conversions
        self.ureg.define('hPa = 100 * Pa = hectopascal')
        self.ureg.define('hPaS = 100 * Pa = hectopascal_step')
        self.ureg.define('torr = 133.322 * Pa = torr')
        self.ureg.define('torrS = 133.322 * Pa = torr_step')
        self.ureg.define('mbar = 100 * Pa = millibar')
        self.ureg.define('mbarS = 100 * Pa = millibar_step')
        self.ureg.define('atm = 101325 * Pa = atmosphere')
        self.ureg.define('atmS = 101325 * Pa = atmosphere_step')
        self.ureg.define('psi = 6895 * Pa = psi')
        self.ureg.define('psiS = 6895 * Pa = psi_step')

        self.unit_dict = {
            'celsius': 'C',
            'fahrenheit': 'F',
            'kelvin': 'K',
            'percent': '%',
            'pascal': 'Pa',
            'hectopascal': 'hPa',
            'torr': 'torr',
            'millibar': 'mBar',
            'atmosphere': 'atm',
            'psi': 'psi',
            'volt': 'V',
            'ampere': 'A',
            'watt': 'W',
            'watt-hour': 'W-hr',
            'hertz': 'Hz',
            'none': '*'
        }

    def convert(
        self,
        value_orig: float,
        unit_orig: str,
        unit_conv: str,
        step: bool = False
    ):
        """
        Performs unit conversions on all values.

        :param value_orig: original sensor value
        :param unit_orig: original unit
        :param unit_conv: target unit
        :param step: ignore unit conversion offset

        :return value_conv: converted value
        :return unit_abbr: abbreviated target unit
        """
        qty = self.ureg.Quantity

        unit_excluded = [
            'volt',
            'ampere',
            'watt',
            'watt-hour',
            'hertz',
            'none'
        ]
        excluded = False

        for unit in unit_excluded:
            if unit_orig == unit:
                excluded = True
                break

        if not excluded:
            if unit_conv != unit_orig:
                if not step:
                    value_dict_orig = qty(value_orig, unit_orig)
                    value_dict_conv = value_dict_orig.to(unit_conv)

                else:
                    value_dict_orig = qty(value_orig, (unit_orig + '_step'))
                    value_dict_conv = value_dict_orig.to(unit_conv + '_step')

                value_conv = round(value_dict_conv.magnitude, 1)
                unit_abbr = self.unit_dict[unit_conv]

            else:
                value_conv = value_orig
                unit_abbr = self.unit_dict[unit_orig]

        else:
            value_conv = value_orig
            unit_abbr = self.unit_dict[unit_orig]

        return value_conv, unit_abbr
