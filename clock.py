#!/home/pi/.virtualenvs/Adafruit_Python_LED_Backpack-6CZK7jrH/bin/python -u

# Copyright (c) 2014 Adafruit Industries
# Author: Carter Nelson
# Modified from matrix8x8_test.py by Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time

import datetime

from random import *

from PIL import Image
from PIL import ImageDraw

from Adafruit_LED_Backpack import Matrix8x16

# Create display instance on default I2C address (0x70) and bus number.
display = Matrix8x16.Matrix8x16()

DIGIT_VALUES = {
    '0': 0b0000110000111111,
    '1': 0b0000000000000110,
    '2': 0b0000000011011011,
    '3': 0b0000000001001111,
    '4': 0b0000000011100110,
    '5': 0b0000000001101101,
    '6': 0b0000000011111101,
    '7': 0b0000000000000111,
    '8': 0b0000000011111111,
    '9': 0b0000000011101111,
    ':': 0b0001001000000000
}
# Alternatively, create a display with a specific I2C address and/or bus.
# display = Matrix8x16.Matrix8x16(address=0x74, busnum=1)

# On BeagleBone, try busnum=2 if IOError occurs with busnum=1
# display = Matrix8x16.Matrix8x16(address=0x74, busnum=2)

# Initialize the display. Must be called once before using the display.
display.begin()
display.clear()

display.set_brightness(5)
#display.set_blink(0x02)

def display_time(time_arr, second):
    for i in range(16):
        display.set_pixel(7, i, time_arr[0][i])
        display.set_pixel(6, i, time_arr[1][i])
        display.set_pixel(4, i, time_arr[2][i])
        display.set_pixel(3, i, time_arr[3][i])
        display.write_display()

    # blink colon
    display.set_pixel(5, 1, second % 2)

def segment_time_array(current_time):
    time_arr = [[0 for i in range(16)] for j in range(4)]
    for i in range(16):
        time_arr[0][i] = DIGIT_VALUES[current_time[0]] >> i & 1
        time_arr[1][i] = DIGIT_VALUES[current_time[1]] >> i & 1
        time_arr[2][i] = DIGIT_VALUES[current_time[2]] >> i & 1
        time_arr[3][i] = DIGIT_VALUES[current_time[3]] >> i & 1
    return time_arr

def randomize_arr(arr, percent):
    rand_arr = [[0 for j in range(len(arr[i]))] for i in range(len(arr))]
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if random() < percent:
                rand_arr[i][j] = randint(0,1)
            else:
                rand_arr[i][j] = arr[i][j]
    return rand_arr

def screwy_display(time_arr, seconds, decay):
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=seconds)
    while datetime.datetime.now() < end_time:
        now = datetime.datetime.now()
        percent_complete = (end_time - now)/datetime.timedelta(seconds=seconds)
        display_time(randomize_arr(time_arr, percent_complete), now.second)

        time.sleep(0.0001)

if __name__ == "__main__":
    last_minute = datetime.datetime.now().minute
    while True:
        now = datetime.datetime.now()
        current_time = str(now.hour).zfill(2) + str(now.minute).zfill(2)

        seg_time_arr = segment_time_array(current_time)

        if now.minute > last_minute and now.minute % 39 == 0:
            screwy_display(seg_time_arr, 7, 0.1)
        else:
            display_time(seg_time_arr, now.second)

        last_minute = now.minute
        time.sleep(0.0001)
