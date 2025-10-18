# Affordable_sdr_radio_spectrometer / RFI_monitor

This project is a simple and affordable way to scan and image large portions of the radio spectrum using an RTL-SDR and Python. 

It records raw IQ data from the SDR, saves and oganises it into HDF5 files, and then processes and displays them as a waterfall graph. Its designed to be modular, affordable and relatively lightweight to use it to record out in the field.

This code was mainly focused on the 700 MHz to 2 GHz range with some tests also taken in the lower FM Radio range. But this depends on your antenna and SDR.

The start of this document will talk you through the basics of the inital code, the "Vanilla" version that contains quite a lot of bottel necks and other features that make it quite inneficient. There are other documents on this page that go into more detail on these bottel necks and the fixes that are impemented to fix them and make the overall system better.

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
# How to Use It ??
1. Install all required drivers and libraries, and make sure you have everything listed in the `requirements.md` file.  
2. Copy the code into a Python file.  
3. Plug the SDR into your laptop (**note:** do not attach the antenna yet).  
4. Take a baseline recording of your SDR at the midpoint of your scan bandwidth.  
   - Example: if you’re recording from 50–100 MHz, take a recording at 75 MHz.  
   - You can take multiple recordings and average the SDR response with no antenna attached.  
5. Attach the antenna to the SDR, making sure the setup is safe and stable (for example, don’t place the antenna in front of an open, running microwave).  
6. Set your parameters and run the main function to start recording.  
7. Process the flat-field correction array.  
8. Process the main recording (this step can take quite a while).  
9. Run the processed data through the waterfall display function to stack all the images and create a full waterfall plot.  
10. Stitch the waterfalls together using the provided function.  

---

# Limitations and Fixes
1. This system is **inefficient** and has the following bottlenecks:  
   - **Recording bandwidth** — limited by hardware.  
   - **Opening and closing the RTL object** — takes time and is repeated at each frequency hop (software).  
   - **FFT calculation** — currently done in a loop for each line. This could be optimized using C++ code, GPU acceleration, or by storing data in vectors instead of lists (software).  
   - **Too many loops** — can be improved through vectorization?? (software).  
2. **Time accuracy** — currently estimated, not measured. Possible fixes include:  
   - Measuring the delay between each measurement and modeling the system accordingly. (Measure and model)  
   - Timestamping each measurement and graphing based on those timestamps. (Timestamp)  
3. **Power calibration** — the measured power level is not absolute. The system needs calibration against a known reference source.  
4. **Usability** — add more user-friendly features and interface improvements.  

----

