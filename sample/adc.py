# -*- coding: utf-8 -*-
import app_windows

def get_hmm():
    """Get a thought."""
    return 'hmmm...'


def hmm():
    """Contemplation..."""
    if helpers.get_answer():
        print(get_hmm())

class InterfaceADC:
    def __init__(self, channel):
        self.channel = channel
        self.channel_value = None

    def get_chan_value(self):
        adc_output = 0
        self.channel_value = ADC.channel_value()
        return self.channel_value