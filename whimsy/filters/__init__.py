# Whimsy is written by Nick Welch <mack@incise.org>, 2005-2007.
#
# This software is in the public domain
# and is provided AS IS, with NO WARRANTY.

from Xlib import X

from whimsy import util

class if_event_type:
    def __init__(self, evtype):
        self.evtype = evtype
    def __call__(self, signal):
        return signal.ev.type == self.evtype

def if_client(signal):
    return util.window_type(signal.wm, signal.ev.window) == 'client'

def if_root(signal):
    return util.window_type(signal.wm, signal.ev.window) == 'root'

def if_no_button_mask(signal):
    mask = X.Button1Mask|X.Button2Mask|X.Button3Mask|X.Button4Mask|X.Button5Mask
    return hasattr(signal.ev, 'state') and not signal.ev.state & mask

class if_:
    def __init__(self, evtype, wintype=None):
        self.evtype = evtype
        self.wintype = wintype
    def __call__(self, signal):
        if signal.ev.type != self.evtype:
            return False
        if self.wintype is None:
            return True
        return util.window_type(signal.wm, signal.ev.window) == self.wintype
