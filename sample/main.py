# from guizero import App, Text, PushButton, TextBox, Window, Box
from guizero import *
import random


def open_cal_window():
    calibration.show()


def close_cal_window():
    calibration.hide()


def close_app():
    app.destroy()


def reset_cal():
    calibration = 0


def save_cal():
    calibration_data = 0


def adc_update():
    delta1_magnitude.value = float(delta1_magnitude.value) + random.random()
    delta2_magnitude.value = float(delta2_magnitude.value) + random.random()
    delta3_magnitude.value = float(delta3_magnitude.value) + random.random()
    delta4_magnitude.value = float(delta4_magnitude.value) + random.random()


class ChanADC:
    def __init__(self, channel):
        self.channel = channel
        self.offset = 0
        self.slope = 1
        self.channel_value = None

    def get_chan_value(self):
        adc_output = 0
        self.channel_value = (adc_output * self.slope) + self.offset


P1 = ChanADC(0)
P2 = ChanADC(1)
Px = ChanADC(2)
Py = ChanADC(3)
Pc = ChanADC(4)

P1.channel_value = random.random()
P2.channel_value = random.random()
Px.channel_value = random.random()
Py.channel_value = random.random()
Pc.channel_value = random.random()

# class DisplayDelta:
#     def __init__(self, delta1, delta2):
#         self.delta1 = delta1
#         self.delta2 = delta2
#
#     def setBoxName(self, name):


#
# Delta_P1P2 = DisplayDelta(P1, P2)
# Delta_PxPy = DisplayDelta(P1, P2)

app = App(title="Pressure Transducer Display Module")
app.full_screen = False
app.width = "1500"
app.height = "500"

calibration = Window(app, title="Transducer Calibration/Offset")
calibration.hide()

delta_P2_P1 = P2.channel_value - P1.channel_value
delta_Px_Pc = Pc.channel_value - Px.channel_value
delta_Py_Px_standard = Py.channel_value - Px.channel_value
delta_Py_Px_unique = (Px.channel_value - Py.channel_value) / 1500


class ChanBox:
    def __init__(self, guizero_app, chan1, chan2):
        self.app = guizero_app
        self.chan1 = chan1
        self.chan2 = chan2
        self.box = None

    def defBox(self):
        self.box = Box(app, width="fill", align="top", border=True)
        return self.box


Delta1 = ChanBox(app, P1, P2)
Delta2 = ChanBox(app, Px, Pc)
Delta3 = ChanBox(app, Py, Px)
Delta4 = ChanBox(app, Py, Px)

delta1_box = Delta1.defBox()
delta2_box = Delta2.defBox()
delta3_box = Delta3.defBox()
delta4_box = Delta4.defBox()

text_size = 35
unit_width = 15
standard_unit = "inch/Hg"
unique_unit = "inch/Kerosene"

# Setup first delta display
delta1_label = Text(delta1_box)
delta1_label.text_size = text_size
delta1_label.value = "Pressure Delta: P1-P2"
delta1_label.align = "left"

delta1_unit = Text(delta1_box)
delta1_unit.width = unit_width
delta1_unit.text_size = text_size
delta1_unit.value = standard_unit
delta1_unit.align = "right"

delta1_magnitude = Text(delta1_box)
delta1_magnitude.text_size = text_size
delta1_magnitude.value = delta_P2_P1
delta1_magnitude.align = "right"

# Setup second delta display
delta2_label = Text(delta2_box)
delta2_label.text_size = text_size
delta2_label.value = "Pressure Delta: Pc-Px"
delta2_label.align = "left"

delta2_unit = Text(delta2_box)
delta2_unit.width = unit_width
delta2_unit.text_size = text_size
delta2_unit.value = standard_unit
delta2_unit.align = "right"

delta2_magnitude = Text(delta2_box)
delta2_magnitude.text_size = text_size
delta2_magnitude.value = delta_Px_Pc
delta2_magnitude.align = "right"

# Setup third delta display
delta3_label = Text(delta3_box)
delta3_label.text_size = text_size
delta3_label.value = "Pressure Delta: Py-Px"
delta3_label.align = "left"

delta3_unit = Text(delta3_box)
delta3_unit.width = unit_width
delta3_unit.text_size = text_size
delta3_unit.value = standard_unit
delta3_unit.align = "right"

delta3_magnitude = Text(delta3_box)
delta3_magnitude.text_size = text_size
delta3_magnitude.value = delta_Py_Px_standard
delta3_magnitude.align = "right"

# Setup fourth delta display
delta4_label = Text(delta4_box)
delta4_label.text_size = text_size
delta4_label.value = "Pressure Delta: Py-Px"
delta4_label.align = "left"

delta4_unit = Text(delta4_box)
delta4_unit.width = unit_width
delta4_unit.text_size = text_size
delta4_unit.value = unique_unit
delta4_unit.align = "right"

delta4_magnitude = Text(delta4_box)
delta4_magnitude.text_size = text_size
delta4_magnitude.value = delta_Py_Px_unique
delta4_magnitude.align = "right"

# Buttons for Main App window
button_box = Box(app, border=True, align="bottom")
calibration_button = PushButton(button_box, command=open_cal_window, text="Add Offset to Channels", align="left")
exit_button = PushButton(button_box, command=close_app, text="Exit Program", align="left")

# Buttons for calibration window
cal_buttons = Box(calibration, border=True, align="bottom")
save_cal_button = PushButton(cal_buttons, command=save_cal, text="Save Calibration", align="left")
reset_calibration_button = PushButton(cal_buttons, command=reset_cal, text="Reset All Channel Offsets", align="left")
exit_cal_button = PushButton(cal_buttons, command=close_cal_window, text="Exit to Main Windows", align="left")

# Job to update transducer values every update_time (in milliseconds)
update_time = 250
app.repeat(update_time, adc_update)

# Main loop for program
app.display()
