from pyo import *
import numpy as np

# ----------------------------------------
# ⚠️ IMPORTANT SETUP NOTES ⚠️
#
# This script uses the Pyo audio server with explicit input/output devices
# and a fixed sample rate (sr = 48000) to ensure compatibility.
#
# Devices selected via `pa_list_devices()`:
# - input_device = 4 (TONOR TC30 USB mic)
# - output_device = 8 (default output)
# - forced sample rate = 48000 Hz
# ----------------------------------------

# Boot server
s = Server(sr=48000, nchnls=1, audio='portaudio')
s.setOutputDevice(8)
s.setInputDevice(4)
s.boot()
s.start()

# Get input audio
guitar = Input(chnl=0)

# Amplitude follower for intensity tracking
amp = Follower(guitar, freq=10)

# Create a Sig object for dynamic feedback gain (will be updated in PID loop)
feedback_gain = Sig(0.5)

# Delay effect
delay = Delay(guitar, delay=0.5, feedback=feedback_gain)
mix = Mix([guitar, delay], voices=2)
mix.out()

# ----------------------------------------
# PID CONTROLLER SETUP
# ----------------------------------------
Kp, Ki, Kd = 10, 0.5, 0.2
A_ref = 0.02  # Target RMS amplitude
e_sum = 0
e_prev = 0
dt = 0.05  # Update interval in seconds

# PID update function
def pid_update():
    global e_sum, e_prev

    A = amp.get()  # Current measured amplitude
    e = A_ref - A
    e_sum += e * dt
    de = (e - e_prev) / dt

    G = Kp * e + Ki * e_sum + Kd * de
    G = np.clip(G, 0.3, 0.9)  # Limit gain between 0.3 and 0.9

    feedback_gain.set(G)
    e_prev = e

# Periodic update using Pyo Pattern
pid_controller = Pattern(pid_update, time=dt).play()

# GUI loop
s.gui(locals())
