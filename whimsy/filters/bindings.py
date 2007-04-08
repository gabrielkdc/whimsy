# Whimsy is written by Nick Welch <mack@incise.org>, 2005-2007.
#
# This software is in the public domain
# and is provided AS IS, with NO WARRANTY.

from Xlib import X, XK

from whimsy import event

from whimsy.log import *

# instead of registering the replayer to the main event signal, we should
# register it to the event's done_processing signal (...?)

class binding_base:
    def __init__(self, **options):
        self.options = options

    def __call__(self, signal):
        ev = signal.ev
        if self._should_at_least_be_swallowed(ev):
            if not self.options.get('passthru', False):
                ev.swallow = True
            return self._should_be_executed(ev)

    def _should_at_least_be_swallowed(self, ev):
        return (
            ev.type in self.swallow_event_types and
            self.detail == ev.detail and
            self.mods.matches(ev.state)
        )
                                                                                                           
    def _should_be_executed(self, ev):
        return ev.type in self.execute_event_types

class if_key_press(binding_base):
    execute_event_types = [X.KeyPress]
    swallow_event_types = [X.KeyPress, X.KeyRelease]

    def __init__(self, keyname, mods, **options):
        binding_base.__init__(self, **options)
        self.keyname = keyname
        self.detail = 'notakeycode'
        self.mods = mods

    def __call__(self, signal):
        if self.detail == 'notakeycode':
            self.detail = signal.wm.dpy.keysym_to_keycode(
                XK.string_to_keysym(self.keyname)
            )
        return binding_base.__call__(self, signal)

class if_button_press(binding_base):
    execute_event_types = [X.ButtonPress]
    swallow_event_types = [X.ButtonPress, X.ButtonRelease]

    def __init__(self, button, mods, **options):
        binding_base.__init__(self, **options)
        self.detail = button
        self.mods = mods
        self.memory = event.click_memory()

    def _should_at_least_be_swallowed(self, ev):
        if ev.__class__.__name__ == "ButtonPress":
            debug('remember')
            self.memory.remember(ev)
        return (
            binding_base._should_at_least_be_swallowed(self, ev) and
            self.options.get('count', 0) in (0, self.memory.count)
        )

class if_button_release(if_button_press):
    execute_event_types = [X.ButtonRelease]
    swallow_event_types = [X.ButtonRelease]

class if_key_release(if_key_press):
    execute_event_types = [X.KeyRelease]
    swallow_event_types = [X.KeyRelease]

