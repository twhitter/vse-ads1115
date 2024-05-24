import random
import pickle
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from guizero import *


def open_cal_window():
    calibration.show()


def close_cal_window():
    calibration.hide()


def close_app():
    app.destroy()


def reset_cal():

    P1.offset = P1.offset_default
    P1.slope = P1.slope_default

    P2.offset = P2.offset_default
    P2.slope = P2.slope_default

    Px.offset = Px.offset_default
    Px.slope = Px.slope_default

    Py.offset = Py.offset_default
    Py.slope = Py.slope_default

    Pc.offset = Pc.offset_default
    Pc.slope = Pc.slope_default

    pickle_values()

    chan1_offset.value = P1.offset
    chan1_slope.value = P1.slope

    chan2_offset.value = P2.offset
    chan2_slope.value = P2.slope

    chan3_offset.value = Px.offset
    chan3_slope.value = Px.slope

    chan4_offset.value = Py.offset
    chan4_slope.value = Py.slope

    chan5_offset.value = Pc.offset
    chan5_slope.value = Pc.slope


def pickle_values():
    with open("chan1_cal.pickle", "wb") as chan1_cal_storage:
        pickle.dump(P1, chan1_cal_storage)
    with open("chan2_cal.pickle", "wb") as chan2_cal_storage:
        pickle.dump(P2, chan2_cal_storage)
    with open("chan3_cal.pickle", "wb") as chan3_cal_storage:
        pickle.dump(Px, chan3_cal_storage)
    with open("chan4_cal.pickle", "wb") as chan4_cal_storage:
        pickle.dump(Py, chan4_cal_storage)
    with open("chan5_cal.pickle", "wb") as chan5_cal_storage:
        pickle.dump(Pc, chan5_cal_storage)


def save_chan1_cal():
    P1.offset = float(chan1_offset.value)
    P1.slope = float(chan1_slope.value)
    pickle_values()


def save_chan2_cal():
    P2.offset = float(chan2_offset.value)
    P2.slope = float(chan2_slope.value)
    pickle_values()


def save_chan3_cal():
    Px.offset = float(chan3_offset.value)
    Px.slope = float(chan3_slope.value)
    pickle_values()


def save_chan4_cal():
    Py.offset = float(chan4_offset.value)
    Py.slope = float(chan4_slope.value)
    pickle_values()


def save_chan5_cal():
    Pc.offset = float(chan5_offset.value)
    Pc.slope = float(chan5_slope.value)
    pickle_values()


def all_channel_update():
    # Get ADC outputs from channels
    P1.channel_voltage = adc1_chan2.voltage
    P2.channel_voltage = adc1_chan1.voltage
    Px.channel_voltage = adc1_chan0.voltage
    Py.channel_voltage = adc1_chan3.voltage
    Pc.channel_voltage = adc2_chan0.voltage

    # Get calibrated channel values from ADC
    P1.get_pressure()
    P2.get_pressure()
    Px.get_pressure()
    Py.get_pressure()
    Pc.get_pressure()

    # Update the GUI values
    chan1_value.value = round(P1.channel_pressure, 7)
    chan2_value.value = round(P2.channel_pressure, 7)
    chan3_value.value = round(Px.channel_pressure, 7)
    chan4_value.value = round(Py.channel_pressure, 7)
    chan5_value.value = round(Pc.channel_pressure, 7)


def delta_update():
    delta1.mag1 = P2.channel_pressure
    delta1.mag2 = P1.channel_pressure

    delta2.mag1 = Px.channel_pressure
    delta2.mag2 = Pc.channel_pressure

    delta3.mag1 = Px.channel_pressure
    delta3.mag2 = Py.channel_pressure

    delta4.mag1 = Px.channel_pressure
    delta4.mag2 = Py.channel_pressure

    delta1.getDelta()
    delta2.getDelta()
    delta3.getDelta()
    delta4.getDelta()

    delta1_magnitude.value = round(delta1.delta, 7)
    delta2_magnitude.value = round(delta2.delta, 7)
    delta3_magnitude.value = round(delta3.delta, 7)
    delta4_magnitude.value = round(delta4.delta * delta4.conversion_value, 7)


class ChanADC:

    def __init__(self):
        self.offset_default = 0.0
        self.slope_default = 300.0
        self.offset = self.offset_default
        self.slope = self.slope_default # default transducer scaling for adc input
        self.channel_voltage = 0.0
        self.channel_pressure = 0.0

    def get_pressure(self):
        self.channel_pressure = (self.channel_voltage * self.slope) + self.offset


    def get_cal_data(self):
        return self.slope, self.offset


class Deltas:
    def __init__(self, mag1, mag2):
        self.mag1 = mag1
        self.mag2 = mag2
        self.delta = None
        self.conversion_value = 1 / 5

    def getDelta(self):
        self.delta = self.mag2 - self.mag1

        return self.delta


i2c = busio.I2C(board.SCL, board.SDA)
ads1 = ADS.ADS1115(i2c, address=0x48)
ads2 = ADS.ADS1115(i2c, address=0x49)

adc1_chan0 = AnalogIn(ads1, ADS.P0)
adc1_chan1 = AnalogIn(ads1, ADS.P1)
adc1_chan2 = AnalogIn(ads1, ADS.P2)
adc1_chan3 = AnalogIn(ads1, ADS.P3)
adc2_chan0 = AnalogIn(ads2, ADS.P0)

# Setup our main adc channels
try:
    with open("chan1_cal.pickle", 'rb') as pickle_file:
        P1 = pickle.load(pickle_file)
except:
    P1 = ChanADC()

try:
    with open("chan2_cal.pickle", 'rb') as pickle_file:
        P2_temp = pickle.load(pickle_file)

    P2 = P2_temp
except:
    P2 = ChanADC()

try:
    with open("chan3_cal.pickle", 'rb') as pickle_file:
        Px_temp = pickle.load(pickle_file)

    Px = Px_temp
except:
    Px = ChanADC()

try:
    with open("chan4_cal.pickle", 'rb') as pickle_file:
        Py_temp = pickle.load(pickle_file)

    Py = Py_temp
except:
    Py = ChanADC()

try:
    with open("chan5_cal.pickle", 'rb') as pickle_file:
        Pc_temp = pickle.load(pickle_file)

    Pc = Pc_temp
except:
    Pc = ChanADC()


delta1 = Deltas(P1.channel_pressure, P2.channel_pressure)
delta2 = Deltas(Px.channel_pressure, Pc.channel_pressure)
delta3 = Deltas(Px.channel_pressure, Py.channel_pressure)
delta4 = Deltas(Py.channel_pressure, Px.channel_pressure)

# Create main app window, everything lives in here
app = App(title="Pressure Transducer Display Module")
app.full_screen = False
app.width = 1200
app.height = 900

# Create padding for deltas top box
top_pad_app = Box(app, align="top", height=75, width="fill", border=False)
left_pad_app = Box(app, align="left", height="fill", width=75, border=False)
right_pad_app = Box(app, align="right", height="fill", width=75, border=False)
bottom_pad_app = Box(app, align="bottom", height=75, width="fill", border=False)

# Make box objects for holding pressure deltas
delta_top_box = Box(app, layout="grid", border=False)
delta1_box = Box(delta_top_box, grid=[0, 0], width=500, height=300, border=True)
delta_12_box_padding = Box(delta_top_box, grid=[1, 0], width=50, height=50, border=False)
delta2_box = Box(delta_top_box, grid=[2, 0], width=500, height=300, border=True)
delta_middle_box_padding = Box(delta_top_box, grid=[2, 1], width=50, height=50, border=False)
delta3_box = Box(delta_top_box, grid=[0, 2], width=500, height=300, border=True)
delta_34_box_padding = Box(delta_top_box, grid=[1, 2], width=50, height=50, border=False)
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
button_box = Box(app, layout="grid", border=False, align="bottom")
calibration_button = PushButton(button_box, grid=[0, 0], command=open_cal_window, text="Add Offset to Channels")
button_box_padding = Text(button_box, grid=[1, 0], width=5)
exit_button = PushButton(button_box, grid=[2, 0], command=close_app, text="Exit Program")

# Setup calibration window
calibration = Window(app, title="Transducer Calibration/Offset")
calibration.width = 900
calibration.height = 500
calibration.hide()

top_pad_cal = Box(calibration, align="top", height=25, width="fill", border=False)
bottom_pad_cal = Box(calibration, align="bottom", height=25, width="fill", border=False)
left_pad_cal = Box(calibration, align="left", height="fill", width=25, border=False)
right_pad_cal = Box(calibration, align="right", height="fill", width=25, border=False)

entry_box_height = 50
entry_box_width = 10
entry_box_pad_y = 10
entry_box_pad_x = 1

cal_label_text_size = 15

# Make box objects for holding cals
cal_top_box = Box(calibration, width="fill", height="fill", border=True)

chan_cal_label_box = Box(cal_top_box, layout="grid", width="fill", height=entry_box_height, border=True)
cal_label_box_pad = Box(cal_top_box, width="fill", height=entry_box_pad_y, border=False)

chan1_cal_box = Box(cal_top_box, layout="grid", width="fill", height=entry_box_height, border=True)
chan1_cal_box_pad = Box(cal_top_box, width="fill", height=entry_box_pad_y, border=False)

chan2_cal_box = Box(cal_top_box, layout="grid", width="fill", height=entry_box_height, border=True)
chan2_cal_box_pad = Box(cal_top_box, width="fill", height=entry_box_pad_y, border=False)

chan3_cal_box = Box(cal_top_box, layout="grid", width="fill", height=entry_box_height, border=True)
chan3_cal_box_pad = Box(cal_top_box, width="fill", height=entry_box_pad_y, border=False)

chan4_cal_box = Box(cal_top_box, layout="grid", width="fill", height=entry_box_height, border=True)
chan4_cal_box_pad = Box(cal_top_box, width="fill", height=entry_box_pad_y, border=False)

chan5_cal_box = Box(cal_top_box, layout="grid", width="fill", height=entry_box_height, border=True)
chan5_cal_box_pad = Box(cal_top_box, width="fill", height=entry_box_pad_y, border=False)

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
chan1_value.value = str(P1.channel_pressure)

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
chan1_offset.value = str(P1.offset)

chan1_padding5 = Text(chan1_cal_box, grid=[11, 0])
chan1_padding5.width = entry_box_pad_x * 5

chan1_save = PushButton(chan1_cal_box, grid=[12, 0], command=save_chan1_cal, text="Save Chan. 1 Adjustment")

# Setup channel 2 cal entry
chan2_name = Text(chan2_cal_box, grid=[0, 0])
chan2_name.value = "P2:"

chan2_padding1 = Text(chan2_cal_box, grid=[1, 0])
chan2_padding1.width = entry_box_pad_x

chan2_value = Text(chan2_cal_box, grid=[2, 0], width=10)
chan2_value.value = str(P2.channel_pressure)

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
chan2_offset.value = str(P2.offset)

chan2_padding5 = Text(chan2_cal_box, grid=[11, 0])
chan2_padding5.width = entry_box_pad_x * 5

chan2_save = PushButton(chan2_cal_box, grid=[12, 0], command=save_chan2_cal, text="Save Chan. 2 Adjustment")

# Setup channel 3 cal entry
chan3_name = Text(chan3_cal_box, grid=[0, 0])
chan3_name.value = "Px:"

chan3_padding1 = Text(chan3_cal_box, grid=[1, 0])
chan3_padding1.width = entry_box_pad_x

chan3_value = Text(chan3_cal_box, grid=[2, 0], width=10)
chan3_value.value = str(Px.channel_pressure)

chan3_padding2 = Text(chan3_cal_box, grid=[3, 0])
chan3_padding2.width = entry_box_pad_x

chan3_unit = Text(chan3_cal_box, grid=[4, 0])
chan3_unit.value = standard_unit

chan3_padding3 = Text(chan3_cal_box, grid=[5, 0])
chan3_padding3.width = entry_box_pad_x * 5

chan3_slope = TextBox(chan3_cal_box, grid=[6, 0], width=entry_box_width)
chan3_slope.value = str(Px.slope)

chan3_padding4 = Text(chan3_cal_box, grid=[9, 0])
chan3_padding4.width = entry_box_pad_x * 10

chan3_offset = TextBox(chan3_cal_box, grid=[10, 0], width=entry_box_width)
chan3_offset.value = str(Px.offset)

chan3_padding5 = Text(chan3_cal_box, grid=[11, 0])
chan3_padding5.width = entry_box_pad_x * 5

chan3_save = PushButton(chan3_cal_box, grid=[12, 0], command=save_chan3_cal, text="Save Chan. 3 Adjustment")

# Setup channel 4 cal entry
chan4_name = Text(chan4_cal_box, grid=[0, 0])
chan4_name.value = "Py:"

chan4_padding1 = Text(chan4_cal_box, grid=[1, 0])
chan4_padding1.width = entry_box_pad_x

chan4_value = Text(chan4_cal_box, grid=[2, 0], width=10)
chan4_value.value = str(Py.channel_pressure)

chan4_padding2 = Text(chan4_cal_box, grid=[3, 0])
chan4_padding2.width = entry_box_pad_x

chan4_unit = Text(chan4_cal_box, grid=[4, 0])
chan4_unit.value = standard_unit

chan4_padding3 = Text(chan4_cal_box, grid=[5, 0])
chan4_padding3.width = entry_box_pad_x * 5

chan4_slope = TextBox(chan4_cal_box, grid=[6, 0], width=entry_box_width)
chan4_slope.value = str(Py.slope)

chan4_padding4 = Text(chan4_cal_box, grid=[9, 0])
chan4_padding4.width = entry_box_pad_x * 10

chan4_offset = TextBox(chan4_cal_box, grid=[10, 0], width=entry_box_width)
chan4_offset.value = str(Py.offset)

chan4_padding5 = Text(chan4_cal_box, grid=[11, 0])
chan4_padding5.width = entry_box_pad_x * 5

chan4_save = PushButton(chan4_cal_box, grid=[12, 0], command=save_chan4_cal, text="Save Chan. 4 Adjustment")

# Setup channel 5 cal entry
chan5_name = Text(chan5_cal_box, grid=[0, 0])
chan5_name.value = "Pc:"

chan5_padding1 = Text(chan5_cal_box, grid=[1, 0])
chan5_padding1.width = entry_box_pad_x

chan5_value = Text(chan5_cal_box, grid=[2, 0], width=10)
chan5_value.value = str(Pc.channel_pressure)

chan5_padding2 = Text(chan5_cal_box, grid=[3, 0])
chan5_padding2.width = entry_box_pad_x

chan5_unit = Text(chan5_cal_box, grid=[4, 0])
chan5_unit.value = standard_unit

chan5_padding3 = Text(chan5_cal_box, grid=[5, 0])
chan5_padding3.width = entry_box_pad_x * 5

chan5_slope = TextBox(chan5_cal_box, grid=[6, 0], width=entry_box_width)
chan5_slope.value = str(Pc.slope)

chan5_padding4 = Text(chan5_cal_box, grid=[9, 0])
chan5_padding4.width = entry_box_pad_x * 10

chan5_offset = TextBox(chan5_cal_box, grid=[10, 0], width=entry_box_width)
chan5_offset.value = str(Pc.offset)

chan5_padding5 = Text(chan5_cal_box, grid=[11, 0])
chan5_padding5.width = entry_box_pad_x * 5

chan5_save = PushButton(chan5_cal_box, grid=[12, 0], command=save_chan5_cal, text="Save Chan. 5 Adjustment")

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

# The real program starts here

# Get ADC outputs from channels and set boxes
all_channel_update()

# Set delta values in their respective boxes
delta_update()

# Job to update transducer values for both windows every update_time (in milliseconds)
update_time = 500

calibration.repeat(update_time, all_channel_update)
app.repeat(update_time, delta_update)

# Main loop for program
app.display()
