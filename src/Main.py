import h5py
import numpy as np
import matplotlib.pyplot as plt
################
from rtlsdr import RtlSdr
###############
from datetime import datetime
import time

def main1(start,end,duration,subduration, file_path):
  ''' this is the original main function, using this the process is a bit less user friendly 
  Parameters:
  - start and end, starting and last frequency of the spectrum being recorded.
  - duration, the length of the recording (not really a time duration).
  - subduration, this is how many disions per single duration.
  - file_path, name or location of file'''
  
    samplerate = 2e6 

    if start < end:
        with h5py.File(file_path, "w") as hdfile:

            while start < end:
                center = start + (samplerate / 2)
                RecordRtl(hdfile, center, samplerate, duration, subduration, 40)
                start += samplerate   
    else:
        print("Error: start_freq is larger than end_freq, i.e. while loop will run forever")

# example:

if __name__ == "__main__":
  
    main(104e6,108e6,4,0.1, "TodayFM.h5" )


################################

def main2():
  ''' This is main function is more user friendly and encapsulates all the functions in one. '''
