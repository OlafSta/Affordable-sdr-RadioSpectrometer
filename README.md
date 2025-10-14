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
# How to use it ??
1. Install all drivers, libraries and ensure you have everything from the requirements.md file.
2. Copy the code into a python file.
3. Plug the SDR into your laptop (note to not attach the antenna)
4. Take a baseline recording of your SDR at the midpoint of your scan bandwidth, example if taking a recoring from 50-100MHz take a recording at 75MHz. You can take more recording and average out the SDR respons with no antenna.
5. Attach the antenna to the SDR making sure the setup it sound (for example dont place your antenna infront of a open running microwave)
6. Set your parameters and run the main function to take the recording.
7. Process the flat field correction array
8. Process the Main recording (this takes quite a long time)
9. Run the processed data through the waterfall display function that stacks all the images and and create a waterfall
10. Stitch the waterfalls together with another function.

----

# Limitations and Fixes:
1. This system is ineeficient and has the following bottlenecks
   - Recoring bandwidth (Hardware)
   - Opening and closing the RTL Object takes time and is repated at each frequency hop (Software)
   - Callculating the FFT is done in a loop for each line, Calculate this using C++ code insead, use a GPU to calcuate this in parallel, store the data in a vector over a list.
   - Reduce the number of loops (Vectorisation).
3. Time is not accurate.
4. The power level is not actually based on a real value and the system needs to be calibrated to a known source.
5. Add more user friendly features and interface.

----

