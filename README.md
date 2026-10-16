# Voice-Controlled CNC Pen Plotter

A 2.5D computer numerical control (CNC) pen plotter powered by an Arduino Uno and GRBL firmware. The system translates spoken drawing commands and text into calibrated G-code paths via a Python speech processing pipeline to execute automated vector plots.

---

## Overview

- **Firmware Engine:** Arduino Uno running GRBL v0.9 / v1.1
- **Shield & Drivers:** CNC Shield v3 with A4988 stepper drivers (1/16 microstepping)
- **Actuation:** Dual NEMA 17 stepper motors (X and Y axes) + micro servo motor (Z-axis pen lift)
- **Input Pipeline:** Python speech recognition pipeline parsing spoken prompts into geometric primitives, alphanumeric text, and motion vectors
- **Communication:** Serial over USB via Python `pyserial` streaming to the GRBL motion controller

---

## Hardware Architecture

| Component | Specification / Model | Function |
| :--- | :--- | :--- |
| **Microcontroller** | Arduino Uno R3 (ATmega328P) | Core motion planner & GRBL controller |
| **Expansion Shield** | CNC Shield v3 | Power distribution & driver breakouts |
| **Stepper Drivers** | A4988 (with heatsinks) | Current-regulated bipolar motor drive |
| **Drive Motors** | NEMA 17 (1.8° step angle) | CoreXY / Cartesian X & Y axis translation |
| **Pen Lift Actuator** | Micro Servo (SG90 / MG90S) | Z-axis pen up/down toggle |
| **Linear Motion** | 8mm smooth rods, LM8UU bearings, GT2 belts & pulleys | Mechanical gantry movement |
| **Power Supply** | 12V 5A DC switching supply | External motor and driver rail |

---

## Software Stack & Requirements

### System Requirements
- Python 3.8+
- Arduino IDE (for initial firmware flash)
- USB Serial drivers (CH340 / FTDI depending on board)

### Python Dependencies
```bash
pip install pyserial SpeechRecognition sounddevice numpy
