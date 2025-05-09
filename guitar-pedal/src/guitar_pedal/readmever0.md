# 🎛️ Feedback-Controlled Delay Pedal (Python + Pyo)

This is a prototype of a **software-based audio effect pedal** for electric guitar (or any live audio input), implemented in Python using the [`pyo`](https://ajaxsoundstudio.com/software/pyo/) real-time audio DSP library. The pedal features a **feedback-controlled delay** where the feedback gain dynamically adapts to the input signal's amplitude using a **PID controller**.

---

## 🚀 Features

- **Real-time audio processing** using Pyo.
- **Dynamic delay effect** where feedback gain is automatically adjusted:
  - Louder playing → shorter delay tail (lower gain).
  - Softer playing → longer ambient decay (higher gain).
- **PID control loop** adjusts gain based on amplitude error with tunable parameters.

---

## 🎧 How It Works

### Signal Chain:
1. Audio input (`Input(chnl=0)`) captures live sound.
2. `Follower` tracks the signal's envelope (amplitude).
3. A custom **PID controller** compares the current amplitude to a reference value.
4. The PID output adjusts the feedback gain of a `Delay` object.
5. Dry and delayed signals are mixed and output.

---

## 🔧 Requirements

- Python 3.10 (not 3.11+ due to `pyo` compatibility)
- [`pyo`](https://pyo.readthedocs.io)
- `numpy`

You can install dependencies with:

```bash
poetry install
