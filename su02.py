"""
.. module:: SU02

***************
 SU02 Module
***************

This is a Module for the `SU02 <https://wiki.xinabox.cc/SU02_-_Universal_Digital_Input>`_ digital input.
The xChip is based on the ADC081C021 analogue to digital converter manufactured by Texas Instruments.
The board uses I2C for communication.

Data Sheets:

-  `ADC081C021 <http://www.ti.com/lit/ds/symlink/adc081c021.pdf>`_

    """
import i2c

ADC_REG_RESULT          = 0x00
ADC_REG_ALERT           = 0x01
ADC_REG_CONF            = 0x02
ADC_REG_LOW_LIM         = 0x03
ADC_REG_HIGH_LIM        = 0x04
ADC_REG_HYSTERESIS      = 0x05
ADC_REG_LOW_CONVR       = 0x06
ADC_REG_HIGH_COVR       = 0x07

ADC_ALERT_OVER_V        = 0x01
ADC_ALERT_UNDER_V       = 0x00

ADC_CONF_CYC_TIME_OFF   = 0x00
ADC_CONF_CYC_TIME_32    = 0x20  
ADC_CONF_CYC_TIME_64    = 0x40
ADC_CONF_CYC_TIME_128   = 0x50
ADC_CONF_CYC_TIME_256   = 0x80
ADC_CONF_CYC_TIME_512   = 0xA0
ADC_CONF_CYC_TIME_1024  = 0xC0
ADC_CONF_CYC_TIME_2048  = 0xE0
ADC_CONF_ALERT_MAN      = 0x01
ADC_CONF_FLAG_EN        = 0x08

HIGH_STATE              = 3.0
LOW_STATE               = 1.0


class SU02(i2c.I2C):
    '''

===============
SU02 class
===============

.. class:: SU02(self, drvname, addr=0x55, clk=100000)

        Create an instance of the SU02 class.

        :param drvname: I2C Bus used '( I2C0, ... )'
        :param addr: Slave address, default 0x55
        :param clk: Clock speed, default 100kHz

    '''
    voltage=0
    state=0
    def __init__(self, drvname=I2C0, addr=0x55, clk=100000):
        i2c.I2C.__init__(self,drvname,addr,clk)
        self._addr=addr
        try:
            self.start()
        except PeripheralError as e:
            print(e)
            
    def init(self):
        '''
.. method:: init()

        Configures the registers of ADC081C021.
        Call after instantiation of the class.
        Exception raised if unsuccessful

        '''
        self.write_bytes(ADC_REG_CONF, ADC_CONF_CYC_TIME_256)
        conf = self.write_read(ADC_REG_CONF, 1)[0]
        if conf != ADC_CONF_CYC_TIME_256:
            raise Exception
    
    def getState(self):
        '''
.. method:: getState()

        Reads the state of the input.
        
        Returns False for Open and True for closed.

        '''
        self.readVoltage()
        return self.state
    
    def getVoltage(self):
        '''
.. method:: getVolatge()

        Reads the voltage on the input.
        
        Returns the voltage.

        '''
        self.readVoltage()
        return self.voltage
    
    def readVoltage(self):
        
        data = self.write_read(ADC_REG_RESULT, 2)
        data_int = (data[0]*256 + data[1])
        a = (data_int & 0xFF00) >> 8
        b = (data_int & 0x00FF) >> 0
        
        self.voltage = (((((a & 0x0F)*256) + (b & 0xF0))/0x10)*(3.3/256))
        
        if self.voltage > HIGH_STATE:
            self.state = True
        elif self.voltage < LOW_STATE:
            self.state = False