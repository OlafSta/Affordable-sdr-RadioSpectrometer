# Affordable-sdr-spectrometer-

This project is a simple and affordable way to scan and image large portions of the radio spectrum using an RTL-SDR and Python. 

It records raw IQ data from the SDR, saves and ogonises it into HDF5 files, and then processes and displays them as a waterfall graph. Its designed to be modular, affordable and relatively lightweight to use it to record out in the field.

This code was mainly focused on the 700 MHz to 2 GHz range with some tests also taken in the lower FM Radio range. But this depends on your antenna and SDR.


----
# How it works ?? 

 ```text
1. Start Script
     │
     ▼
2. Set Parameters
   (frequency range, sample rate, subdivisions, gain)
     │
     ▼
3. Frequency Hopping Loop
   ┌──────────────────────────────────────────┐
   │ For each frequency window:               │
   │   - Record IQ samples using RTL-SDR      │
   │   - Store raw data in HDF5 file          │
   └──────────────────────────────────────────┘
     │
     ▼
4. Process Data
   - Apply FFT to convert time → frequency domain
   - Normalize using baseline (optional)
     │
     ▼
5. Save Processed Data
   - Store FFT outputs in smaller HDF5 chunks
     │
     ▼
6. Display / Visualize
   - Generate waterfall image (freq vs. time)
   - Optionally add ComReg band overlays
 ```

----
 # How to use it?? 
 1. Install all the libraries and the code provided in the src directory.
 2. 
