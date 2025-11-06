# SPARK — Synergistic Planetary Autonomous Robotic Kinetics

**Tagline:** A research-grade hexapedal platform optimized for rugged-terrain locomotion, modular payload integration, and edge-aware perception — developed as a student research project and demonstration prototype.

---

## Badges

[![Runner-up: Vigyan Bharti 2024](https://raw.githubusercontent.com/JaideepChouhan/SPARK-Hexapod-v1/refs/heads/main/assets/Vigyan%20Bharti%202024.jpeg)]()
[![3rd Runner-up: IEEE JECRC 2024](https://raw.githubusercontent.com/JaideepChouhan/SPARK-Hexapod-v1/refs/heads/main/assets/IEEE-project%20expo.jpeg)]

---

## Table of Contents

* [Executive Summary](#executive-summary)
* [Specifications & Bill of Materials (Key Components)](#specifications--bill-of-materials-key-components)
* [System Architecture Overview](#system-architecture-overview)
* [Mechanical Design & Kinematics](#mechanical-design--kinematics)
* [Electronics & Power System](#electronics--power-system)
* [Control, Locomotion & Interaction](#control-locomotion--interaction)
* [Perception & Communication](#perception--communication)
* [Testing, Validation & Performance Metrics](#testing-validation--performance-metrics)
* [How to Build / Run the Demo (for recruiters/interviewers)](#how-to-build--run-the-demo-for-recruitersinterviewers)
* [Contributing & Contact](#contributing--contact)

---

## Executive Summary

SPARK is a compact hexapedal research platform (prototype) engineered to experiment with gait dynamics, fault-tolerant locomotion, and human–robot interfaces on constrained hardware. Built as a student project with an emphasis on reproducibility and modularity, SPARK demonstrates:

* deterministic servo-based joint control across 6 legs (12 actuated DOF),
* real-time video feedback and teleoperation, and
* on-device low-latency voice interaction and command parsing (DETROIT local voice modality — prototype).

The project is intended to be a technical portfolio piece suitable for interviews, industrial demos, and academic discussions. The repository contains CAD renders, photos, firmware examples (safe-to-share), experiment logs, and schematic/BOM references for components used in the prototype.

---

## Specifications & Bill of Materials (Key Components)

> The table below lists the core parts used in the SPARK prototype. Quantities, nominal ratings, and short-purpose notes are included so a technical reviewer can quickly evaluate the hardware choices.

| Component                                  |       Quantity | Nominal Specs / Notes                                                                                                                  |
| ------------------------------------------ | -------------: | -------------------------------------------------------------------------------------------------------------------------------------- |
| Chassis & structural parts (PLA printed)   |              — | PLA prints from Blender 4.3 exports; lightweight, easy iteration; fast-prototype tolerancing shown in `hardware/images/`               |
| Legs (6)                                   |              6 | Each leg: 2 DOF (hip + knee) — 12 actuated joints total                                                                                |
| TowerPro SG90 micro servo                  |             12 | Operating voltage: 4.8–6.0 V; stall torque ~1.8–2.2 kg·cm (@4.8V); PWM control (50 Hz typical) — used for actuation in prototype       |
| PCA9685 PWM driver                         |             1+ | I²C-controlled 16-channel PWM expander; cascading supported for >16 channels; used for servo multiplexing and synchronized PWM outputs |
| Arduino UNO (ATmega328P)                   |              1 | Main microcontroller for real-time servo timing, gait sequencer, and deterministic low-level control                                   |
| HC-05 Bluetooth module                     |              1 | SPP / classic Bluetooth for phone-based manual teleoperation; persistent tele-op channel used in demos                                 |
| PS2 controller + receiver                  | 1 (controller) | Legacy controller used for trial tele-op and manual experiments (redundant input modality)                                             |
| ESP32-CAM                                  |              1 | Monocular streaming camera for live video feedback (embedded on 'head' position)                                                       |
| Power supply — SMPS                        |              1 | 12 V / 20 A switching supply (prototype bench PSU or custom SMPS used during tests)                                                    |
| 7805 linear regulators (for 5V rails)      |       multiple | Inline regulation from 12 V -> 5 V rails for controller and servo bus (note: 7805 will dissipate heat; see power notes)                |
| Passive components, connectors, harnessing |       assorted | JST connectors, shrouded header pins for modular subassemblies                                                                         |

**Note on servos:** SG90 servos are hobby-grade micro-servos; they are appropriate for low-mass prototype limbs but have limited torque and thermal characteristics. For payload-heavy or field-deployable designs, upgrade to coreless/metal-gear high-torque servos or brushless actuators.

---

## System Architecture Overview

SPARK’s architecture follows a layered control paradigm:

1. **Hardware layer** — mechanical links, servos, power distribution, and sensing (ESP32-CAM, optional IMU).
2. **Firmata/low-level firmware** (Arduino UNO) — deterministic PWM generation via PCA9685, servo calibration routines, and safety limit enforcement.
3. **Gait sequencer & mid-level controller** — parameterized gait primitives (tripod/ripple/wave); interpolators convert endpoint trajectories into synchronized joint setpoints.
4. **Operator & HRI layer** — multiple tele-op modalities (HC-05 phone app, PS2 controller) and a local voice modality (DETROIT) running on a laptop for speech preprocessing and command dispatch.
5. **Data & telemetry** — run logs, timestamped experiment CSVs, and video captures for post-run analysis in `experiments/`.

The software is organized to keep computationally heavy processing (e.g., model training, complex IK) on an external laptop/RPi, while the UNO handles real-time low-latency actuation.

---

## Mechanical Design & Kinematics

### Kinematic Summary

* **Topology:** Hexapod with symmetric leg placement for stable tripod gaits.
* **Per-leg DOF:** 2 DOF (hip pitch, knee pitch). Hip yaw/roll are not implemented on the prototype but are part of the SPARK 2.0 roadmap.
* **Kinematic model:** Denavit–Hartenberg inspired link frames for simple FK; inverse kinematics solved analytically for 2-DOF planar legs to compute joint setpoints from desired foot coordinates.

### Manufacturing & Materials

* Prototyped in PLA using FDM printers. Exploded assembly drawings and annotated renders are located in `hardware/images/`.
* Joints use mechanical fasteners and heat-set threaded inserts where repeated assembly/disassembly is expected.

---

## Electronics & Power System

### Electrical Topology

* **Primary bus:** 12 V from SMPS → distributed to power management section.
* **Regulation:** multiple 7805 linear regulators stepping 12 V down to 5 V rails for Arduino, PCA9685, and the servo bus. The servo bus receives regulated 5 V supply; ground commonization is enforced.

### Power Considerations & Thermal Notes

* **Current draw:** 12 SG90 servos under load can draw substantial transient current (peak servo stall currents up to ~1 A per servo). Although SG90 average currents are lower, design for peak aggregated draw is essential: SMPS rated at 20 A provides headroom for simultaneous actuation.
* **7805 limitations:** 7805 linear regulators dissipate (Vin - Vout) × Iout as heat. Driving the entire servo bus through linear regulators from 12 V will cause significant thermal dissipation at high currents. In prototype we used multiple parallel 7805 regulators and heat-sinks; for production a dedicated DC–DC buck converter with high efficiency is recommended.
* **Decoupling & filtering:** Place bulk electrolytic capacitors near PCA9685/servo connectors and local ceramic decoupling on logic rails to mitigate voltage dips during concurrent servo actuation.

### Electrical Safety

* Include reverse-polarity protection, fuse-protected power rails, and thermal cut-offs for sustained stall conditions.

---

## Control, Locomotion & Interaction

### Gait Primitives

* Implemented gait modes: **Tripod**, **Ripple**, and **Static Wave** — parametrized by duty factor, stride length, and phase offsets.
* Gait state machine supports: `IDLE`, `CALIBRATE`, `WALK`, `RECOVERY`, and `MANUAL_OVERRIDE`.

### Low-level Control

* **Servo mapping:** PWM pulse widths are mapped to joint angles via linear calibration polynomials stored in EEPROM on the UNO for fast boot calibration.
* **Safety checks:** Joint soft-limits, watchdog timeout for teleop link loss, and servo pulse clamping to prevent over-travel.

### Human–Robot Interaction

* **Teleoperation:** Primary tele-op via HC-05 and a custom mobile app or serial terminal. PS2 controller driver exists as a legacy input method for rapid manual testing.
* **Voice interaction (DETROIT):** Local voice command recognition and synthesis pipeline used for on-stage demos (prototype-level): feature extraction (MFCC), compact classifier, and a finite-state command parser.

---

## Perception & Communication

* **Video:** ESP32-CAM mounted on the head assembly streams low-latency video for operator situational awareness.
* **Telemetry:** Simple CSV logs and timestamped images saved during experimental runs; telemetric replay scripts provided in `experiments/`.
* **Future sensors:** IMU and depth sensors are planned to enable closed-loop foothold selection and SLAM.

---

## Testing, Validation & Performance Metrics

* **Unit tests:** calibration utilities for pulse-to-angle linearization and watchdog behavior for serial link loss.
* **Integration tests:** scripted gait runs with stopwatch timings, energy profiling, and success-rate statistics (steps completed vs. slips).
* **Performance metrics recorded:** forward walking speed (cm/s), energy-per-meter (J/m), step success rate, average servo temperature during run, and time-to-failure under continuous operation.

---

## How to Build / Run the Demo (for recruiters/interviewers)

> These instructions are intended to let a reviewer run safe demonstrations and evaluate the system without requiring production-grade hardware.

1. **Hardware prep**

   * Install 12× SG90 servos into leg assemblies and wire each servo connector to the PCA9685 channels following the channel map in `firmware/arduino_uno/CHANNEL_MAP.md`.
   * Ensure the 12 V SMPS is configured and verified with a multimeter. Connect SMPS ground to the Arduino ground before powering logic.
   * Use separate power rails or adequately sized regulators for the servo bus and logic rail. Verify 5 V presence on the servo connector pins.

2. **Firmware**

   * Open `firmware/arduino_uno/` in Arduino IDE (set board to Arduino/Genuino UNO). Load `servo_calibrate.ino` first to calibrate servo endpoints.
   * Load `gait_sequencer.ino` for the primary walking demo. Ensure the PCA9685 library and Adafruit PCA9685 driver are installed.

3. **Teleoperation**

   * Pair the HC-05 with a mobile device and use the serial terminal or provided phone UI to send manual movement commands.
   * Optional: connect PS2 receiver and use the `ps2_demo.ino` sketch for alternative control.

4. **Video & Telemetry**

   * Power up ESP32-CAM and open the stream URL (printed by the module) on a browser to observe the live feed.
   * Collect logs in `experiments/` for performance analysis.

---

## Contact

**E-mail:** jaideepchouhan123@gmail.com

**Linkedin:** https://linkedin.com/in/jd0214

---
