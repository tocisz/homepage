===
date: 2018-05-10
===
# LCD Screens

Nothing really interesting here. I just want to document how to connect two
LCD screens to a blue pill. Actually it's not a blue pill. It's black.
Some pins are connected differently. E.g. onboard LED is not on `PC13`,
but on `PC15`.

## ST7735 1.8'' TFT LCD

This one has `128`x`160` resolution.

![1.8'' LCD](007-1.jpg)

Connect as follows.

```
STM32  3.3 --- VCC  LCD
       GND --- GND
       AO  --- CS
       A1  --- RESET
       C13 --- AO
       A7  --- SDA
       A5  --- SCK
       3.3 --- LED
```

I used code from ... TODO.

## 2.4'' TFT LCD

This one has `320`x`240` resolution and is touch sensitive.

Connect as in [this article](https://www.instructables.com/id/Fast-Portable-and-Affordable-Oscilloscope-and-Indu/).

Some documentation can be found [here](http://misc.ws/category/arduino/).
