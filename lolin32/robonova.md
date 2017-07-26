# Robonova robot control


[Back to the main page](readme.md)

## Acknowledgements 

Robonova is a robot from the year 2008. The orignal control platform (MR-C3024) is an Atmega platform controlled with basic as higher language.
It is a nice control platform, but has its limits.

Robonova consists of 16 special designed servos. Each servo can be controlled with standard pulse, extended pulse or hmi.
See: https://robosavvy.com/Builders/i-Bot/HSR8498HB%20Servo.pdf

More info about the hmi here: http://robosavvy.com/Builders/i-Bot/HSR8498_serial.pdf

and here:
http://www.iri.upc.edu/files/scidoc/1186-Slave-architecture-for-the-Robonova-MR-C3024-using-the-HMI-protocol-IRI-Technical-Report.pdf


## Goal

* Short term: I try to control the robonova via HMI, using a lolin32 with micropython as platform. Status: fully working! 
Longer term: control Robonova via ROS. Create a ROS driver for the the Robonova

## Firmware modification

To control the servos directory, without extra electronics, the uart RX and TX must be inverted. The underlying esp-idf platform does support inverting the signals.

Add next lines to function machine_uart_init_helper in machine_uart.c:

   if (args[ARG_inv].u_int > 0){
        uint32_t mask = (1 << 22 ) | (1<< 19);
        uart_set_line_inverse(self->uart_num, mask);
    }

And modify:
   static const mp_arg_t allowed_args[] = {
        { MP_QSTR_baudrate, MP_ARG_INT, {.u_int = 0} },
        { MP_QSTR_inv, MP_ARG_INT, {.u_int = 0} },
        { MP_QSTR_bits, MP_ARG_INT, {.u_int = 0} },

Note that line with MP_QSTR_inv is added.

Rebuild and flash the new firmware.

## Servo connection:

* Connect the data line of the servo to RX of uart2 (pin 16 on lolin32)
* Connect the data line of the servo with an 1K resistor to TX of uart2 (pin 17 on lolin32) 

The effect is that the esp32 can send frames via TX and the 1k resitor.
While receiving data the esp32 will transmit 2 zeros, effectivly creating a pullup resistor (note that TX is inverted!)


# Testing
* Connect up to  3 servo's to uart2.
* Run test /test/lib/test_hitecservo.py

# Servo control app:
* A web app is available to control all 16 servo's of the robonova
* see /app/robonova
* status: work in progress, working, but not finished yet

