from abc import abstractmethod
import logging
# import RPi.GPIO as GPIO
from time import sleep

from homeassistant.helpers.restore_state import RestoreEntity

from .const import *

_LOGGER = logging.getLogger(__name__)

class GPIOCon(RestoreEntity):
    """GPIO connector"""
    _pin = -1
    _repeat = 3
    _pause = 8064
    _init = {}
    _bit = {}
    _open = "00010001"
    _close = "00110011"
    _stop = "01010101"

    def __init__(self, conf) -> None:
        _LOGGER.info("rf_cover log ")
        self._pin = conf.get(PIN)
        self._repeat = conf.get(REPEAT)
        self._pause = float(conf.get(PAUSE)) / 1000000
        self._init = conf.get(INIT)
        self._bit = conf.get(BIT)
        self._setup_gpio()


    def send_close(self):
        """Sends command to GPIO"""
        code = self._get_code() + " " + self._close
        _LOGGER.info("send_close %s", code)
        self._emit_code(code)
        # GPIO.output(self._pin, 1)

    def send_open(self):
        """Sends command to GPIO"""
        code = self._get_code() + " " + self._open
        _LOGGER.info("send_open %s", code)
        self._emit_code(code)
        # GPIO.output(self._pin, 0)

    def send_stop(self):
        """Sends command to GPIO"""
        code = self._get_code() + " " + self._stop
        _LOGGER.info("send_stop %s", code)
        self._emit_code(code)

    def _setup_gpio(self):
        """Initialize GPIO"""
        _LOGGER.info("rf_cover log ")
        # GPIO.setwarnings(False)
        # # GPIO.setmode(GPIO.BOARD)
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self._pin, GPIO.OUT)

    @abstractmethod
    def _get_code(self)->str:
        pass

    def _init_code(self):
        """Initialize signal"""
        high = float(self._init.get(TIME).get(HIGH)) / 1000000
        low = float(self._init.get(TIME).get(LOW)) / 1000000
        _LOGGER.info("Emit initialize signale %s, %s", high, low)
        # GPIO.output(self._pin, 1)
        sleep(high)
        # GPIO.output(self._pin, 0)
        sleep(low)

    def _emit_code(self, command):
        """emit code"""
        _LOGGER.info("Emit code %s", command)
        long = float(self._bit.get(TIME).get(LONG)) / 1000000
        short = float(self._bit.get(TIME).get(SHORT)) / 1000000
        for t in range(self._repeat):
            self._init_code()
            self._emit_single_command(command, long, short)
            sleep(self._pause)

    def _emit_single_command(self, bits, long, short):
        command = bits.replace(" ", "")
        _LOGGER.info("Emit single code %s", command)
        for i in range(1, len(command)+1):
            if (command[i-1] == '1'):
                # GPIO.output(self._pin, 1)
                sleep(long)
                # GPIO.output(self._pin, 0)
                sleep(short)
            elif (command[i-1] == '0'):
                # GPIO.output(self._pin, 1)
                sleep(short)
                # GPIO.output(self._pin, 0)
                sleep(long)
