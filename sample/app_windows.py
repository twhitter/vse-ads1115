# Built-in Libraries
import random
import pickle

# Libraries from PyPi
from guizero import *

# User Libraries
from adc import *


def open_cal_window():
    calibration.show()


def close_cal_window():
    calibration.hide()


def close_app():
    app.destroy()


def reset_cal():
    P1.offset = 0
    P1.slope = 1
    chan1_offset.value = P1.offset
    chan1_slope.value = P1.slope

    P2.offset = 0
    P2.slope = 1
    chan2_offset.value = P1.offset
    chan2_slope.value = P1.slope


def reset_chan1_cal():
    P1.offset = P1.offset_default
    P1.slope = P1.slope_default
    chan1_offset.value = P1.offset
    chan1_slope.value = P1.slope


def pickle_values():
    pickle.dump(P1, open("chan1_cal.pickle", "wb"))
    pickle.dump(P2, open("chan2_cal.pickle", "wb"))
    pickle.dump(Px, open("chan3_cal.pickle", "wb"))
    pickle.dump(Py, open("chan4_cal.pickle", "wb"))
    pickle.dump(Pc, open("chan5_cal.pickle", "wb"))


def save_chan1_cal():
    P1.offset = float(chan1_offset.value)
    P1.slope = float(chan1_slope.value)
    pickle_values()

def save_chan2_cal():
    P2.offset = float(chan2_offset.value)
    P2.slope = float(chan2_slope.value)
    pickle_values()


def save_cal():
    P1.offset = float(chan1_offset.value)
    P1.slope = float(chan1_slope.value)


def all_channel_update():
    P1.adc_out = round(float(random.randint(40, 1500)), 2)
    P2.adc_out = round(float(random.randint(40, 1500)), 2)
    Px.adc_out = round(float(random.randint(40, 1500)), 2)
    Py.adc_out = round(float(random.randint(40, 1500)), 2)
    Pc.adc_out = round(float(random.randint(40, 1500)), 2)

    # Update the channel values
    P1.get_chan_value()
    P2.get_chan_value()

    # Update the GUI values
    chan1_value.value = P1.channel_value
    chan2_value.value = P2.channel_value


def delta_update():
    delta1_magnitude.value = Deltas(P1.channel_value, P2.channel_value).getDelta()
    delta2_magnitude.value = Deltas(Px.channel_value, Pc.channel_value).getDelta()
    delta3_magnitude.value = Deltas(Px.channel_value, Py.channel_value).getDelta()
    delta4_magnitude.value = Deltas(Py.channel_value, Px.channel_value).getDelta() * Deltas(Py, Px).conversion_value


class ChanADC:

    def __init__(self, channel):
        self.channel = channel
        self.offset_default = 0.0
        self.slope_default = 1.0
        self.offset = 0.0
        self.slope = 1.0
        self.adc_out = 0
        self.channel_raw_value = 0.0
        self.channel_value = 0.0

    def channel_raw_value(self):
        self.channel_raw_value = (self.adc_out * self.slope_default) + self.offset_default

        return self.channel_raw_value

    def get_chan_value(self):
        self.channel_raw_value = (self.adc_out * self.slope_default) + self.offset_default

        self.channel_value = (self.adc_out * self.slope) + self.offset

        return self.channel_value


class Deltas:
    def __init__(self, mag1, mag2):
        self.mag1 = mag1
        self.mag2 = mag2
        self.delta = None
        self.conversion_value = 1 / 5

    def getDelta(self):
        self.delta = self.mag2 - self.mag1

        return self.delta

    # def setBoxName(self, name):


class ChanBox:
    def __init__(self, guizero_app, chan1, chan2):
        self.app = guizero_app
        self.chan1 = chan1
        self.chan2 = chan2
        self.box = None

    def defBox(self):
        self.box = Box(app, width="fill", align="top", border=True)
        return self.box


# Setup our main adc channels
try:
    pickle_file = open("chan1_cal.pickle", 'rb')
    P1 = pickle.load(pickle_file)
    pickle_file.close()
    P1.slope = float(P1.slope)
    P1.offset = float(P1.offset)
except:
    P1 = ChanADC(0)

P2 = ChanADC(1)
Px = ChanADC(2)
Py = ChanADC(3)
Pc = ChanADC(4)


# Create main app window, everything lives in here
app = App(title="Pressure Transducer Display Module")
app.full_screen = False
app.width = 1200
app.height = 900

# Create padding for deltas top box
top_pad_app = Box(app, align="top", height=75, width="fill", border=True)
left_pad_app = Box(app, align="left", height="fill", width=75, border=True)
right_pad_app = Box(app, align="right", height="fill", width=75, border=True)
bottom_pad_app = Box(app, align="bottom", height=75, width="fill", border=True)

# Make box objects for holding pressure deltas
delta_top_box = Box(app, layout="grid", border=True)
delta1_box = Box(delta_top_box, grid=[0, 0], width=500, height=300, border=True)
delta_12_box_padding = Box(delta_top_box, grid=[1, 0], width=50, height=50, border=True)
delta2_box = Box(delta_top_box, grid=[2, 0], width=500, height=300, border=True)
delta_middle_box_padding = Box(delta_top_box, grid=[2, 1], width=50, height=50, border=True)
delta3_box = Box(delta_top_box, grid=[0, 2], width=500, height=300, border=True)
delta_34_box_padding = Box(delta_top_box, grid=[1, 2], width=50, height=50, border=True)
delta4_box = Box(delta_top_box, grid=[2, 2], width=500, height=300, border=True)

delta_label_text_size = 35
delta_magnitude_text_size = 35
delta_padding_height = 3

standard_unit = "   (inch/Hg) "
unique_unit = " (inch/Kerosene) "

# Setup first delta display
delta1_label = Text(delta1_box)
delta1_label.text_size = delta_label_text_size
delta1_label.value = "P1-P2" + standard_unit
delta1_label.align = "top"

delta1_padding = Text(delta1_box)
delta1_padding.height = delta_padding_height
delta1_padding.align = "top"

delta1_magnitude = Text(delta1_box)
delta1_magnitude.text_size = delta_magnitude_text_size
delta1_magnitude.value = 0

# Setup second delta display
delta2_label = Text(delta2_box)
delta2_label.text_size = delta_label_text_size
delta2_label.value = "Pc-Px" + standard_unit
delta2_label.align = "top"

delta2_padding = Text(delta2_box)
delta2_padding.height = delta_padding_height
delta2_padding.align = "top"

delta2_magnitude = Text(delta2_box)
delta2_magnitude.text_size = delta_magnitude_text_size
delta2_magnitude.value = 0

# Setup third delta display
delta3_label = Text(delta3_box)
delta3_label.text_size = delta_label_text_size
delta3_label.value = "Py-Px" + standard_unit
delta3_label.align = "top"

delta3_padding = Text(delta3_box)
delta3_padding.height = delta_padding_height
delta3_padding.align = "top"

delta3_magnitude = Text(delta3_box)
delta3_magnitude.text_size = delta_magnitude_text_size
delta3_magnitude.value = 0

# Setup fourth delta display
delta4_label = Text(delta4_box)
delta4_label.text_size = delta_label_text_size
delta4_label.value = "Py-Px" + unique_unit
delta4_label.align = "top"

delta4_padding = Text(delta4_box)
delta4_padding.height = delta_padding_height
delta4_padding.align = "top"

delta4_magnitude = Text(delta4_box)
delta4_magnitude.text_size = delta_magnitude_text_size
delta4_magnitude.value = 0

# Buttons for Main App window
button_box = Box(app, layout="grid", border=True, align="bottom")
calibration_button = PushButton(button_box, grid=[0, 0], command=open_cal_window, text="Add Offset to Channels")
button_box_padding = Text(button_box, grid=[1, 0], width=5)
exit_button = PushButton(button_box, grid=[2, 0], command=close_app, text="Exit Program")

# Setup calibration window
calibration = Window(app, title="Transducer Calibration/Offset")
calibration.width = 800
calibration.height = 500
# calibration.hide()

top_pad_cal = Box(calibration, align="top", height=25, width="fill", border=True)
bottom_pad_cal = Box(calibration, align="bottom", height=25, width="fill", border=True)
left_pad_cal = Box(calibration, align="left", height="fill", width=25, border=True)
right_pad_cal = Box(calibration, align="right", height="fill", width=25, border=True)

entry_box_height = 50
entry_box_width = 10
entry_box_pad_y = 10
entry_box_pad_x = 1

cal_label_text_size = 15

# Make box objects for holding cals
cal_top_box = Box(calibration, width="fill", height="fill", border=True)

chan_cal_label_box = Box(cal_top_box, layout="grid", width="fill", height=entry_box_height, border=True)
cal_label_box_pad = Box(cal_top_box, width="fill", height=entry_box_pad_y, border=True)

chan1_cal_box = Box(cal_top_box, layout="grid", width="fill", height=entry_box_height, border=True)
chan1_cal_box_pad = Box(cal_top_box, width="fill", height=entry_box_pad_y, border=True)

chan2_cal_box = Box(cal_top_box, layout="grid", width="fill", height=entry_box_height, border=True)
chan2_cal_box_pad = Box(cal_top_box, width="fill", height=entry_box_pad_y, border=True)

chan3_cal_box = Box(cal_top_box, layout="grid", width="fill", height=entry_box_height, border=True)
chan3_cal_box_pad = Box(cal_top_box, width="fill", height=entry_box_pad_y, border=True)

chan4_cal_box = Box(cal_top_box, layout="grid", width="fill", height=entry_box_height, border=True)
chan4_cal_box_pad = Box(cal_top_box, width="fill", height=entry_box_pad_y, border=True)

chan5_cal_box = Box(cal_top_box, layout="grid", width="fill", height=entry_box_height, border=True)
chan5_cal_box_pad = Box(cal_top_box, width="fill", height=entry_box_pad_y, border=True)

# Setup channel cal top line (labels)
chan_label1 = Text(chan_cal_label_box, grid=[0, 0])
chan_label1.text_size = cal_label_text_size
chan_label1.value = "  Current Channel Value"

chan_label1_padding = Text(chan_cal_label_box, grid=[1, 0])
chan_label1_padding.width = 5

chan_label2 = Text(chan_cal_label_box, grid=[2, 0])
chan_label2.text_size = cal_label_text_size
chan_label2.value = "User Slope"

chan_label2_padding = Text(chan_cal_label_box, grid=[3, 0])
chan_label2_padding.width = 6

chan_label3 = Text(chan_cal_label_box, grid=[4, 0])
chan_label3.text_size = cal_label_text_size
chan_label3.value = "User Offset"

chan_label3_padding = Text(chan_cal_label_box, grid=[5, 0])
chan_label3_padding.width = 5

# Setup channel 1 cal entry
chan1_name = Text(chan1_cal_box, grid=[0, 0])
chan1_name.value = "P1:"

chan1_padding1 = Text(chan1_cal_box, grid=[1, 0])
chan1_padding1.width = entry_box_pad_x

chan1_value = Text(chan1_cal_box, grid=[2, 0], width=10)
chan1_value.value = str(P1.channel_value)

chan1_padding2 = Text(chan1_cal_box, grid=[3, 0])
chan1_padding2.width = entry_box_pad_x

chan1_unit = Text(chan1_cal_box, grid=[4, 0])
chan1_unit.value = standard_unit

chan1_padding3 = Text(chan1_cal_box, grid=[5, 0])
chan1_padding3.width = entry_box_pad_x * 5

chan1_slope = TextBox(chan1_cal_box, grid=[6, 0], width=entry_box_width)
chan1_slope.value = str(P1.slope)

chan1_padding4 = Text(chan1_cal_box, grid=[9, 0])
chan1_padding4.width = entry_box_pad_x * 10

chan1_offset = TextBox(chan1_cal_box, grid=[10, 0], width=entry_box_width)
chan1_offset.value = str(P1.offset) * 5

chan1_padding5 = Text(chan1_cal_box, grid=[11, 0])
chan1_padding5.width = entry_box_pad_x * 5

chan1_save = PushButton(chan1_cal_box, grid=[12, 0], command=save_chan1_cal, text="Save Chan. 1 Adjustment")

# Setup channel 2 cal entry
chan2_name = Text(chan2_cal_box, grid=[0, 0])
chan2_name.value = "P2:"

chan2_padding1 = Text(chan2_cal_box, grid=[1, 0])
chan2_padding1.width = entry_box_pad_x

chan2_value = Text(chan2_cal_box, grid=[2, 0], width=10)
chan2_value.value = str(P2.channel_value)

chan2_padding2 = Text(chan2_cal_box, grid=[3, 0])
chan2_padding2.width = entry_box_pad_x

chan2_unit = Text(chan2_cal_box, grid=[4, 0])
chan2_unit.value = standard_unit

chan2_padding3 = Text(chan2_cal_box, grid=[5, 0])
chan2_padding3.width = entry_box_pad_x * 5

chan2_slope = TextBox(chan2_cal_box, grid=[6, 0], width=entry_box_width)
chan2_slope.value = str(P2.slope)

chan2_padding4 = Text(chan2_cal_box, grid=[9, 0])
chan2_padding4.width = entry_box_pad_x * 10

chan2_offset = TextBox(chan2_cal_box, grid=[10, 0], width=entry_box_width)
chan2_offset.value = str(P2.offset) * 5

chan2_padding5 = Text(chan2_cal_box, grid=[11, 0])
chan2_padding5.width = entry_box_pad_x * 5

chan2_save = PushButton(chan2_cal_box, grid=[12, 0], command=save_chan2_cal, text="Save Chan. 2 Adjustment")

# Buttons for calibration window
cal_buttons = Box(calibration, layout="grid")
cal_buttons.border = True
cal_buttons.align = "bottom"

cal_box_padding_1 = Text(cal_buttons, grid=[1, 0], width=1)

reset_calibration_button = PushButton(cal_buttons, grid=[2, 0], command=reset_cal, text="Reset All Offsets")
reset_calibration_button.align = "left"

cal_box_padding_2 = Text(cal_buttons, grid=[3, 0], width=1)

exit_cal_button = PushButton(cal_buttons, grid=[4, 0], command=close_cal_window, text="Exit to Main Windows")
exit_cal_button.align = "left"
