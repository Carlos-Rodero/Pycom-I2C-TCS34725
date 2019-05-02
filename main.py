import machine
import pycom
import time
import tcs34725
from machine import I2C, Pin

""" DEFINES """

# color leds
led_red = 0x7f0000
led_green = 0x007f00
led_yellow = 0x7f7f00

# PIN list
# SDA_pin_list = ['P11', 'P8', 'P10', 'P20', 'P9']
SDA_pin_list = ['P9']
SCL_pin = 'P21'

""" FUNCTIONS """


def blink_led(times, ms, color):
    """ Function to uses the RGB LED to make a blink light
    Parameters
        ----------
            times: int
                number of times to blink the light.
            ms: int
                time in ms that will be blink the light
            color: string
                type of color
    """
    for cycles in range(times):
        pycom.rgbled(color)
        time.sleep_ms(int(ms/2))
        pycom.heartbeat(False)
        time.sleep_ms(int(ms/2))


def read_sensors(SDA_pin_list, SCL_pin):
    """ Function to read TCS34725 light sensors using I2C protocol
    Parameters
        ----------
            SDA_pin_list: list
                list of SDA pins
            SCL_pin: int
                SCL pin number
    """
    for i in range(len(SDA_pin_list)):
        # I2C is a two-wire protocol for communicating between devices.
        # At the physical level it consists of 2 wires: SCL and SDA, the clock
        # and data lines respectively.
        # I2C objects are created attached to a specific bus.
        # I2C initialized on bus 0
        i2c = I2C(0, pins=(SDA_pin_list[i], SCL_pin))
        try:
            # Create a TCS34725 instance
            sensor = tcs34725.TCS34725(i2c)
            # switch off led
            sensor.interrupt(False)
            # set integration time as 154 ms
            sensor.integration_time(value=154)
            # and gain as 1x
            sensor.gain(1)
            time.sleep_ms(500)
            print("sensor: {}".format(i))
            for i in range(3):
                print(sensor.read(raw=True))
                time.sleep_ms(1000)
                blink_led(1, 500, led_green)

            sensor.active(False)
        except (OSError) as e:
            print(e)

        i2c.deinit()

""" CODE """

# Heartbeat LED flashes in blue colour once every 4s to signal that the system
# is alive. Turn off fimware blinking
pycom.heartbeat(False)

read_sensors(SDA_pin_list, SCL_pin)
