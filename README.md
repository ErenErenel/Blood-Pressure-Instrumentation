# Blood Pressure Instrumentation 

This repository contains the signal processing pipeline used to extract physiological parameters from blood pressure waveform data acquired in a biomedical instrumentation lab. Analog conditioning (e.g., filtering, amplification) was done externally; this repo focuses on the digital analysis phase.

## DSP Pipeline Overview

- **Input:** Raw pressure waveform post-analog filtering
- **Steps:**
  - Bandpass filtering (0.48–4.8 Hz range preserved from analog stage)
  - Segmentation and trimming of usable data
  - Peak/trough detection to isolate cardiac oscillations
  - Frequency-domain analysis via periodogram
  - Extraction of:
    - **Heart rate** (e.g., 1.233 Hz → 74 bpm)
    - **Mean Arterial Pressure (MAP)** from oscillation envelope
    - **Systolic & Diastolic Pressure** using amplitude-based thresholds

## Results (Sample Data)

- **Estimated MAP:** 99.9 mmHg (peak amplitude at 44.43 s)
- **SBP:** 133.0 mmHg (7th oscillation)
- **DBP:** 76.3 mmHg (19th oscillation)
- **Heart Rate:** 74 bpm  
- **Peak detection accuracy:** >95%  
- **Error vs. reference:** <4%

## Files

- `DigitalSignalProcessing/`: Python scripts for time/frequency-domain analysis
- `BloodPressureInstrumentationExampleResult.pdf`: Final report with analysis outputs and plots

## Outcome

This DSP pipeline demonstrates accurate extraction of cardiovascular metrics from conditioned blood pressure waveforms, showcasing envelope analysis, frequency-domain validation, and segmentation-based peak detection.
