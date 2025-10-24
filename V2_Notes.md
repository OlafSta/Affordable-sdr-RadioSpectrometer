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

## 3. FFT calculation
Batch mode?
Apply window?

The SDR and the code capture IQ sample of the signal.
These represent the radio wavefrom in a complex form, both amplitude and phase.
This signal is a time domain signal, meaning that its amplitude (voltage) changes over time.
What the FFT does is convert that time-domain signal into a frequency-domain representation.
Each recording is converted into a power vs frequency plot (insert a image here) <img width="890" height="434" alt="FFT" src="https://github.com/user-attachments/assets/365145b0-792b-423c-9787-c4d0f8e4da47" />
  Once this is repeated multiple times we can represent the amplitude with a colour and stack each of the lines vertically to give a waterfall graph. ie each fft in the code give one horizontal line in the waterfall plot.

The FFT is a much faster way of computing the DFT. for a 1-million-point FFT the DFT does *10^12* operations while the FFT does only 20 million operations.
So why is this a bottle neck in my vanilla V1 system code??

### FFT as bottle neck ###
1. Looping in Python.
2. Reading data in the HDF5 file, we do thousands of small reads from the disk which adds latency.
3. np.fft.fft(raw_samp) calls the FFT which is fast but then it is looped over many times in a loop it makes the loop slow.
4. writing the data on the disk as it is being processed, this could be done in packages instead.

### Fixes ###
#### 1. Batch calculation (Vectorize)
Instead of calling the FFT one-by-one, we want to stack multiple samples and process it in one go
#### 2. FFTW through pyFFTW
Using a much faster fft library

#### 3. Power of two FFT size

#### 4. Outsourcing the FFT to the GPU??
gpu or parallel calculation 

#### 5. Increase the accuracy of the calculation
Apply a window


# Time is not real !! ?? 
Well the time axis in the original is not a ture representation of time, its mearly a aproximation of the time passed.




