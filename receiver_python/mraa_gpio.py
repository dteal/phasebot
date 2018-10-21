#!/usr/bin/env python

#gpio example in python using mraa
#Author: Manivannan Sadhasivam
#Toggles GPIO 23 and 24

import mraa
import time

gpio_1 = mraa.Gpio(23)
gpio_2 = mraa.Gpio(24)
gpio_1.dir(mraa.DIR_OUT)
gpio_2.dir(mraa.DIR_OUT)

while True:
    gpio_1.write(1)
    gpio_2.write(0)

    time.sleep(2)

    gpio_1.write(0)
    gpio_2.write(1)

    time.sleep(2)
    print("A cycle has passed.\n")
