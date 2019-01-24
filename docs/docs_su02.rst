.. module:: SU02

***************
 SU02 Module
***************

This is a Module for the `SU02 <https://wiki.xinabox.cc/SU02_-_Universal_Digital_Input>`_ digital input.
The xChip is based on the ADC081C021 analogue to digital converter manufactured by Texas Instruments.
The board uses I2C for communication.

Data Sheets:

-  `ADC081C021 <http://www.ti.com/lit/ds/symlink/adc081c021.pdf>`_

    
===============
SU02 class
===============

.. class:: SU02(self, drvname, addr=0x55, clk=100000)

        Create an instance of the SU02 class.

        :param drvname: I2C Bus used '( I2C0, ... )'
        :param addr: Slave address, default 0x55
        :param clk: Clock speed, default 100kHz

    
.. method:: init()

        Configures the registers of ADC081C021.
        Call after instantiation of the class.
        Exception raised if unsuccessful

        
.. method:: getState()

        Reads the state of the input.
        
        Returns False for Open and True for closed.

        
.. method:: getVolatge()

        Reads the voltage on the input.
        
        Returns the voltage.

        
