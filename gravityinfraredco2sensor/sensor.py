# -*- coding: utf-8 -*-

from time import sleep
from threading import Thread

import serial


class GravityInfraredCO2Sensor(Thread):
    def __init__(self, dev, timeout=10.0, hook=None):
        super(GravityInfraredCO2Sensor, self).__init__()
        self.serial = serial.Serial(
            dev,
            timeout=timeout
        )
        self.__command = 0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79
        self.__renew()
        self.__hook = hook if hook is not None else lambda v: None

    def __renew(self):
        self.serial.write(self.__command)
        sleep(0.5)
        res = self.serial.read(9)
        val = res[2] * 256 + res[3]
        self.__latest_value = val

    def run(self):
        while True:
            self.__renew()
            self.__hook(dict(zip(self.attributes(), self.values())))
            sleep(0.5)

    def attributes(self):
        return ('co2', )

    def values(self):
        return (self.co2, )

    @property
    def co2(self):
        return self.__latest_value

    def __getitem__(self, attr):
        if attr in self.attributes():
            return getattr(self, attr)
        raise KeyError(attr)
