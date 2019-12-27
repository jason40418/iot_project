#!/usr/bin/env python

from pms5003 import PMS5003

class PMS():

    def __init__(self):
        # Configure the PMS5003 for Enviro+
        self.__pms5003 = PMS5003(
            device='/dev/ttyAMA0',
            baudrate=9600,
            pin_enable=22,
            pin_reset=27
        )

    def get_data(self):
        try:
            data = self.__pms5003.read()
            return True, {
                'PM1.0'     : data.pm_ug_per_m3(1.0, False),
                'PM2.5'     : data.pm_ug_per_m3(2.5, False),
                'PM10.0'    : data.pm_ug_per_m3(10, False),
                '0.3um+'    : data.pm_per_1l_air(0.3),
                '0.5um+'    : data.pm_per_1l_air(0.5),
                '1.0um+'    : data.pm_per_1l_air(1.0),
                '2.5um+'    : data.pm_per_1l_air(2.5),
                '5.0um+'    : data.pm_per_1l_air(5.0),
                '10.0um+'   : data.pm_per_1l_air(10.0)
            }

        except:
            return False, {
                'PM1.0'     : None,
                'PM2.5'     : None,
                'PM10.0'    : None,
                '0.3um+'    : None,
                '0.5um+'    : None,
                '1.0um+'    : None,
                '2.5um+'    : None,
                '5.0um+'    : None,
                '10.0um+'   : None
            }
