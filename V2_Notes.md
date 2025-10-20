Here is a more indepth explination of the limitations of the inital model.


## 1. Opening and Closing the RTL Object

Each time the RTL-SDR object is opened in Python, it adds a delay. Over time, this delay becomes significant (see comparison at the end of this section).  
Currently, the SDR object is opened at each frequency jump.  

This issue is fixed by combining the main function with the `rtlsdr` function into a single function, and then opening the RTL-SDR once at the start of the recording or main function.  

The code for this fix can be found in the `V2.py` file.  

To compare the versions with and without the fix, data was collected using Excel. Several recordings of 4-second duration were made — the code recorded data at each frequency for 4 seconds before performing a frequency jump.  
Recordings were taken for 1, 2, 4, 8, 16, 20, 30, and 40 jumps using both versions of the recording function.  

The results were plotted in Excel, with time on the y-axis and the number of jumps on the x-axis.  
Knowing that each jump should ideally take 4 seconds (as set in the Python code), the average time per jump was found by fitting a slope to the plotted lines and comparing it to the expected 4-second value.  

- **V1 (vanilla)** code had a slope of **5.45 s/jump**  
- **V2** code had a slope of **4.5 s/jump**
<img width="1064/2" height="605/2" alt="image" src="https://github.com/user-attachments/assets/f13f3b0a-a213-4e16-99b3-16a3f6afbb12" />


## 2. Reduce the number of loops
This works by trying to change the way the data is represented 

## 3. FFT calculatio

