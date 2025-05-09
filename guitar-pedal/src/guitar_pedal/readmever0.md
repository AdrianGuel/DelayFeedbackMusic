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
````

Ensure `pyo` can access your audio hardware. If needed, check your devices with:

```python
from pyo import *
print(pa_list_devices())
```

---

## 🛠️ Device Setup (Linux)

We hardcoded the audio setup based on `pa_list_devices()`:

* **Input Device**: TONOR TC30 USB Microphone → `input_device = 4`
* **Output Device**: Default output (headphones or speakers) → `output_device = 8`
* **Sample Rate**: Forced to `48000 Hz` to ensure compatibility between devices

---

## 🧠 PID Controller

The controller updates every 50 ms:

* Reference amplitude: `A_ref = 0.3`
* PID Gains:

  * Proportional: `Kp = 0.8`
  * Integral: `Ki = 0.3`
  * Derivative: `Kd = 0.1`
* Gain output `G(t)` is clipped to stay between `0.3` and `0.9`.

---

## 🖥️ Running the App

Launch the delay effect pedal with:

```bash
poetry run python src/guitar_pedal/main.py
```

This will:

* Open the Pyo GUI
* Start processing audio in real time

---

## 🧩 Future Additions

* Tempo detection (for beat-synced delay)
* Pitch tracking for shimmer effects or harmonizing
* GUI controls for PID tuning or delay modulation
* Export as a VST plugin using JUCE or Faust

---

## 📜 License

MIT License. Developed as a creative prototype combining control theory with digital audio.

---

## 🙌 Credits

Created by [Adrian Guel](https://github.com/AdrianGuel), inspired by real-time control systems and guitar effects design.
