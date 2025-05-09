# 🎛️ Feedback-Controlled Delay Pedal (Volume-Sensitive Delay and Feedback)

This Python-based software pedal simulates a **dynamic delay effect** for live audio input (e.g., guitar or microphone). It adapts **both the feedback gain** and the **delay time** in real-time based on how loudly you play or speak — creating an expressive, volume-responsive effect.

Built with [`pyo`](https://ajaxsoundstudio.com/software/pyo/), this prototype demonstrates how control theory (specifically PID control) can be applied to sound processing.

---

## 🚀 What It Does

- 🎚️ **Adaptive Feedback Gain**  
  Louder input → lower feedback → quicker echo fade  
  Softer input → higher feedback → longer, sustained echo

- 🕒 **Adaptive Delay Time**  
  Louder input → shorter delay (tighter echo)  
  Softer input → longer delay (ambient feel)

- ⚙️ **PID Control Loop**  
  Dynamically tunes feedback gain using a control-theoretic approach based on signal amplitude.

---

## 🧠 Signal Flow

1. **Audio Input**: Captured live from a mic or guitar input.
2. **Envelope Detection**: Uses `Follower` to track input amplitude.
3. **PID Controller**:
   - Compares amplitude to a setpoint (`A_ref`)
   - Computes a feedback gain `G(t)`
   - Maps amplitude `A(t)` to delay time `τ(t)`
4. **Delay DSP**:
   - Applies a variable delay and gain to create echo
5. **Mix Output**: Combines dry + delayed signal and plays it.

---

## 🎧 Requirements

- Python 3.10 (required for pyo compatibility)
- `pyo`, `numpy`

Install via Poetry:

```bash
poetry install
```

---

## 🔧 Audio Device Setup (Linux)

Use:

```python
from pyo import *
print(pa_list_devices())
```

Then update the script with:

- `input_device = 4` (e.g., TONOR USB mic)
- `output_device = 8` (default audio out)
- Sample rate: `48000 Hz` (common for USB mics)

---

## 🖥️ Running the App

```bash
poetry run python src/guitar_pedal/main.py
```

You'll hear your input processed through a dynamic delay effect.

---

## ⚙️ Tuning Parameters

- `A_ref = 0.3`: Reference amplitude target
- `Kp, Ki, Kd`: PID gains (default: 2.0, 0.5, 0.2)
- Delay time mapped from amplitude:  
  `τ(t) = 0.8 - A(t) * 0.6` (clipped between 0.2 and 0.8)

---

## 🧩 Future Additions

- Tempo tracking → beat-synced delay
- Pitch-based control → shimmer & harmonizing
- Streamlit GUI or JUCE plugin version
- Real-time plot of gain and delay

---

## 📜 License

MIT License. For experimental and educational use.

---

## 🙌 Author

Created by [Adrian Guel](https://github.com/AdrianGuel), exploring the intersection of audio effects and control engineering.