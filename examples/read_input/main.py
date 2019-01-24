###############################################
#   This is an example for the SU02 digital
#   input.
#
#   The state is read and displayed over the
#   serial console.
###############################################

import streams
from xinabox.su02 import su02

streams.serial()

# SU02 instance
SU02 = su02.SU02(I2C0)

# configure SU02
SU02.init()

while True:
    state = SU02.getState()		# read the state at the input
    print(state)
    sleep(1000)