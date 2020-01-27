#
# llichen80.py
#
#   Llichen-80 extensions for miniterm
#
#   Version 0.01 - 2020-01-22 - yorgle@gmail.com
#
#   Handles:
#       - toggling GPIO to reset the RC2014 (GPIO18)


import sys
import time
import imp
import subprocess
from interceptor import Interceptor

try:
    imp.find_module('RPI')
    import RPI.GPIO as GPIO
    onRaspi = True
except ImportError:
    onRaspi = False

# This is the GPIO pin (BCM) that is tied to the RC2014's reset line
gpioPin = 18



class Llichen( Interceptor ):
    """Disk IO and reset interface for RC2014"""

    def __init__( self ):
        super(Llichen,self).__init__()

        # 3ms delay per character sent from us
        self.set_msDelayChar( 3 )

        self.onRaspi = onRaspi
        self.gpioPin = gpioPin

        if( self.onRaspi ):
            # setup GPIO18 as an output
            GPIO.setmode( GPIO.BCM )
            GPIO.setwarnings( False )
            GPIO.setup( gpioPin, GPIO.OUT )
            sys.stderr.write( '\n--- Llichen API Starting up (RasPi+GPIO) ---\n' )
        else:
            sys.stderr.write( '\n--- Llichen API Starting up (sim) ---\n' )

        sys.stderr.write( self.describe() );


    def describe( self ):
        return """
Llichen-80 API Extensions  v0.01
(c)2020 Scott Lawrence
        yorgle@gmail.com
        """

    def receivedFromTarget(self, text):
        #sys.stderr.write(' [RX:{!r}] '.format(text))
        #sys.stderr.flush()
        if( text == 'Z' ):
            return False

        if( text == '5' ):
            self.tx( '\n\r10 a=99832\n\r' );
            # need a way to suppress echo.

        return text


    def do_command( self ):
        self.toggle_gpio_pin()



    def toggle_gpio_pin( self ):
        sys.stderr.write( '\n--- RESET: ' )
        if self.onRaspi:
            sys.stderr.write( 'Toggle GPIO18 ---\n' )
            # send LOW (reset) for 1 second, then restore HIGH (normal run)
            GPIO.output( self.gpioPin, GPIO.LOW )
            time.sleep( 1 )
            GPIO.output( self.gpioPin, GPIO.HIGH )
            # return to high-z state
            GPIO.setup( self.gpioPin, GPIO.IN )

        else:
            sys.stderr.write( 'Sending SIGUSR1 to emulator ---\n' )
            subprocess.run( [ 'killall', '-SIGUSR1', 'llichen80emu'  ] )

        sys.stderr.write( '--- Done ---\n' ) 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Create a single instance of this over in the miniterm file

