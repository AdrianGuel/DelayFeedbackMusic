from pyo import *
import numpy as np

# ----------------------------------------
# ⚠️ SETUP NOTES ⚠️
#
# Devices chosen via pa_list_devices():
# - Input Device (mic/guitar): 4 (TONOR USB)
# - Output Device (speakers): 8 (default)
# - Sample Rate: 48000 Hz (needed for device compatibility)
# ----------------------------------------

# Boot Pyo server with correct I/O and sample rate
s = Server(sr=48000, nchnls=1, audio='portaudio')
s.setInputDevice(4)
s.setOutputDevice(8)
s.boot()
s.start()

# --- SIGNAL CHAIN SETUP ---

# Input signal from mic/guitar
guitar = Input(chnl=0)

# Real-time envelope follower to measure input amplitude
amp = Follower(guitar, freq=10)

# Sig objects for dynamic control
feedback_gain = Sig(0.5)
delay_time = Sig(0.5)

# Delay with both feedback and delay time controlled
delay = Delay(guitar, delay=delay_time, feedback=feedback_gain)
mix = Mix([guitar, delay], voices=2)
mix.out()

# --- PID CONTROLLER CONFIG ---

Kp, Ki, Kd = 20.0, 0, 2
A_ref = 0.1  # Desired RMS amplitude reference
e_sum = 0
e_prev = 0
dt = 0.05  # Update rate (in seconds)

# --- CONTROL LOOP: feedback_gain AND delay_time ---
def pid_update():
    global e_sum, e_prev

    A = amp.get()  # Current amplitude estimate
    e = A_ref - A
    e_sum += e * dt
    de = (e - e_prev) / dt

    # PID output for feedback gain
    G = Kp * e + Ki * e_sum + Kd * de
    G = np.clip(G, 0.3, 0.9)
    feedback_gain.set(G)

    # Map amplitude to delay time: softer = longer delay
    # Example: A = 0.0 -> τ = 0.8, A = 1.0 -> τ = 0.2
    tau = np.clip(0.8 - A * 0.6, 0.2, 0.8)
    delay_time.set(tau)

    # Debug print
    print(f"A = {A:.2f}, G = {G:.2f}, τ = {tau:.2f}")

    e_prev = e

# Run the control loop periodically
Pattern(pid_update, time=dt).play()

# Launch GUI to keep app running
s.gui(locals())
