#
# interceptor.py
#
#   extensions for miniterm to allow intercepting/inhibiting/injecting text
#   beyond the builtin filters
#
#   adds:
#       menu option for a function
#       operation for that option (canned as ctrl-g)
#       millisecond delay per character sent
#       helper calls to make communication easier
#
#   Version 0.01 - 2020-01-26 - yorgle@gmail.com
#

import sys
import time


class Interceptor(object):
    """fits inbetween the user and the target"""

    def __init__( self ):
        # be sure to call the constructor from your inherited class!!!
        self.miniterm = False
        self.msDelayChar = 0


    # helper functions
    def set_miniterm( self, mo ):
        """set our miniterm object (helper)"""
        self.miniterm = mo

    def set_msDelayChar( self, msd ):
        """set the delay per character"""
        self.msDelayChar = 0

    # this is a wrapper for a transmit call that adds in a ms delay
    def tx( self, text ):
        """send out through the connected port (helper)"""
        if self.msDelayChar < 1:
            self.miniterm.raw_tx( text )
            return

        # there's a delay per char, send it char by char
        for ch in text:
            self.miniterm.raw_tx( ch )
            time.sleep( self.msDelayChar / 1000 )


    # override these functions
    def receivedFromTarget( self, text ):
        """text received from serial port"""
        # return 'text' to pass through
        # return false if all text was consumed
        return text


    # for additional operation:

    def get_command_key( self ):
        """return the cotnrol character for menu operations """
        return '\x07'

    def get_help_text( self ):
        """text to be sent on menu help"""
        return "Do the interceptor operation"

    def do_command( self ):
        """do the operation"""
        sys.stderr.write( "Do command." );

