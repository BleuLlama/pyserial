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

try:
    imp.find_module('RPI')
    import RPI.GPIO as GPIO
    onRaspi = True
except ImportError:
    onRaspi = False

# This is the GPIO pin (BCM) that is tied to the RC2014's reset line
gpio_reset_rc2014 = 18


class Llichen( object ):

    def __init__( self, onRaspi, gpioPin ):
        self.onRaspi = onRaspi
        self.gpioPin = gpioPin

        if( self.onRaspi ):
            # setup GPIO18 as an output
            GPIO.setmode( GPIO.BCM )
            GPIO.setwarnings( False )
            GPIO.setup( gpioPin, GPIO.OUT )
            sys.stderr.write( '\n--- Llichen API Starting up (RasPi) ---\n' )
        else:
            sys.stderr.write( '\n--- Llichen API Starting up (sim) ---\n' )

        sys.stderr.write( self.describe() );


    def describe( self ):
        return """
Llichen-80 API Extensions  v0.01
(c)2020 Scott Lawrence
        yorgle@gmail.com
        """
    

    def toggle_gpio_pin( self ):
        sys.stderr.write( '\n--- Toggle GPIO ---\n' )
        if self.onRaspi:
            # send LOW (reset) for 1 second, then restore HIGH (normal run)
            GPIO.output( self.gpioPin, GPIO.LOW )
            time.sleep( 1 )
            GPIO.output( self.gpioPin, GPIO.HIGH )
            # return to high-z state
            GPIO.setup( self.gpioPin, GPIO.IN )
            sys.stderr.write( '--- Done ---\n' ) 
        #else:
        #    sys.stderr.write( '--- (No Pi) ---\n' ) 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Create a single instance of this...

llichen = Llichen( onRaspi, gpio_reset_rc2014 )