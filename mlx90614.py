"""
`mlx90614`
====================================================

MicroPython module for the MLX90614 IR object temperature sensor.

* Author(s): Alchemist Aloha based on code from these projects:
  Adafruit Industries - https://github.com/adafruit/Adafruit_CircuitPython_MLX90614
  Limor Fried - https://github.com/adafruit/Adafruit-MLX90614-Library
  Bill Simpson - https://github.com/BillSimpson/ada_mlx90614
  Mike Causer - https://github.com/mcauser/micropython-mlx90614

"""

from micropython import const

from machine import I2C, Pin


# Internal constants:
_MLX90614_I2CADDR = const(0x5A)

# RAM
_MLX90614_RAWIR1 = const(0x04)
_MLX90614_RAWIR2 = const(0x05)
_MLX90614_TA = const(0x06)
_MLX90614_TOBJ1 = const(0x07)
_MLX90614_TOBJ2 = const(0x08)

# EEPROM
_MLX90614_TOMAX = const(0x20)
_MLX90614_TOMIN = const(0x21)
_MLX90614_PWMCTRL = const(0x22)
_MLX90614_TARANGE = const(0x23)
_MLX90614_EMISS = const(0x24)
_MLX90614_CONFIG = const(0x25)
_MLX90614_ADDR = const(0x0E)
_MLX90614_ID1 = const(0x3C)
_MLX90614_ID2 = const(0x3D)
_MLX90614_ID3 = const(0x3E)
_MLX90614_ID4 = const(0x3F)


class MLX90614:
    """Create an instance of the MLX90614 temperature sensor.

    :param int i2c_id: The I2C bus ID.
    :param int scl_pin: The GPIO number of the SCL pin.
    :param int sda_pin: The GPIO number of the SDA pin.
    

    **Quickstart: Importing and using the MLX90614**

        Here is an example of using the :class:`MLX90614` class.
        First you will need to import the libraries to use the sensor

        .. code-block:: python

            from mlx90614 import *

        Once this is done you can define your sensor object

        .. code-block:: python

            sensor = MLX90614(i2c_id, scl_pin, sda_pin)

        Now you have access to the :attr:`ambient_temperature` and :attr:`object_temperature` attribute

        .. code-block:: python

            amb_temperature = sensor.ambient_temperature
            obj_temperature = sensor.object_temperature

    """

    def __init__(self, i2c_id, scl_pin, sda_pin) -> None:
        self.device = I2C(i2c_id, scl=Pin(scl_pin),
                          sda=Pin(sda_pin), freq=100000)
        self.buf = bytearray(2)
        self.buf_old = bytearray(2)
        self.buf[0] = _MLX90614_CONFIG

    @property
    def ambient_temperature(self) -> float:
        """Ambient Temperature in Celsius."""
        return self.read_temp(_MLX90614_TA)

    @property
    def object_temperature(self) -> float:
        """Object Temperature in Celsius."""
        return self.read_temp(_MLX90614_TOBJ1)

    def read_temp(self, register: int) -> float:
        """Read and return the temperature from the specified register."""
        temp = self.read_16(register)
        temp *= 0.02
        temp -= 273.15
        return temp

    def read_16(self, register: int) -> int:
        """Read and return a 16-bit value read from the
        specified 16-bit register address."""
        try:
            self.device.readfrom_mem_into(
                _MLX90614_I2CADDR, register, self.buf)
            self.buf_old = self.buf[:]
            return self.buf[1] << 8 | self.buf[0]  # output 16 bit as integer
        except Exception as e:
            print(e)
            # output previous 16 bit as integer
            return self.buf_old[1] << 8 | self.buf_old[0]
