# Affordable_sdr_radio_spectrometer / RFI_monitor

This project is a simple and affordable way to scan and image large portions of the radio spectrum using an RTL-SDR and Python. 

It records raw IQ data from the SDR, saves and ogonises it into HDF5 files, and then processes and displays them as a waterfall graph. Its designed to be modular, affordable and relatively lightweight to use it to record out in the field.

This code was mainly focused on the 700 MHz to 2 GHz range with some tests also taken in the lower FM Radio range. But this depends on your antenna and SDR.


----
# How it works ?? 

 ```text

1. Set Parameters and Run Code
   (frequency range, sample rate, subdivisions, gain)
     │
     ▼
2. Frequency Hopping Loop
   ┌──────────────────────────────────────────┐
   │ For each frequency window:               │
   │   - Record IQ samples using RTL-SDR      │
   │   - Store raw data in HDF5 file          │
   └──────────────────────────────────────────┘
     │
     ▼
3. Process Data
   - Apply FFT to convert time → frequency domain
   - Normalize using baseline (optional)
     │
     ▼
4. Save Processed Data
   - Store FFT outputs in smaller HDF5 chunks
     │
     ▼
5. Display / Visualize
   - Generate waterfall image (freq vs. time)
   - Optionally add ComReg band overlays
 ```

----
# How to use original main function ( main1() )? 
 1. Run all the libraries and the code provided in the src directory.
 2. 

# How to use new main2() function ? (Still working on it)
1. Run all the pyhton code into jupyter or anyother python interface.
2. 

