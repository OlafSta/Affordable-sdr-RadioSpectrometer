Here is a more indepth explination of the limitations of the inital model.


# Opening and closing RTL object:
Each time the RTL sdr object is opened in python it adds a delay, this delay builds up to substantial over time (Compareson at the end of this section). 
Currently the SDR object is open at each frequency jump. 
This will be fixed by combining the main function with the rtlsdr function into one function, then opening up the rtl sdr at the start of each function.
