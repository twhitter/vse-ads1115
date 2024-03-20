from app_windows import *

# Get ADC outputs from channels
P1.adc_out = round(float(random.randint(40, 1500)), 2)
P2.adc_out = round(float(random.randint(40, 1500)), 2)
Px.adc_out = round(float(random.randint(40, 1500)), 2)
Py.adc_out = round(float(random.randint(40, 1500)), 2)
Pc.adc_out = round(float(random.randint(40, 1500)), 2)

# Get calibrated channel values from ADC
P1.get_chan_value()
P2.get_chan_value()
Px.get_chan_value()
Py.get_chan_value()
Pc.get_chan_value()

# Set delta values in their respective boxes
delta1_magnitude.value = Deltas(P1.channel_value, P2.channel_value).getDelta()
delta2_magnitude.value = Deltas(Px.channel_value, Pc.channel_value).getDelta()
delta3_magnitude.value = Deltas(Px.channel_value, Py.channel_value).getDelta()
delta4_magnitude.value = Deltas(Py.channel_value, Px.channel_value).getDelta() * Deltas(Py, Px).conversion_value

# Job to update transducer values for both windows every update_time (in milliseconds)
update_time = 1000

calibration.repeat(update_time, all_channel_update)
app.repeat(update_time, delta_update)


# Main loop for program
app.display()
