import h5py
import numpy as np
import matplotlib.pyplot as plt
################
from rtlsdr import RtlSdr
###############
from datetime import datetime
import time


def RecordRtl(hdfile, central, samp, duration, sub_duration, gain=20):
    ''' This function records the raw IQ data in a hdf5 file,
    Its imputs are:
    - hdfile, path to the file location/name.
    - central, central frequency of the sdr.
    - samp, sample rate of the sdr, which also defines the bandwidth.
    - duration, length of the recording (not really a time measurment).
    - sub_duration, it is the sub division of the duration, it defines the resolution but also has some other effects '''
  
    sdr = RtlSdr()
    
    try:
        
        sdr.sample_rate = samp
        sdr.center_freq = central
        sdr.gain = gain

        samples_sub = int(samp * sub_duration)
        #sub_recordings_per_second = int(1 / sub_duration)
        total_sub_recordings = int(duration / sub_duration)

        group_name = f"{central/1e6:.1f}"
        group = hdfile.create_group(group_name)
        
        for i in range(total_sub_recordings):
            samples = sdr.read_samples(samples_sub)
    
            dataset_name = f"{i+1}"
            dataset = group.create_dataset(dataset_name, data=samples, dtype='complex64')

        group.attrs['center_freq'] = central
        group.attrs['sample_rate'] = samp 
        group.attrs['duration'] = duration
        group.attrs['time_stamp'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        group.attrs['sub_dur'] = sub_duration
    
    except Exception as e:
        print(f"{e}")

    finally:
        sdr.close()
        print(central)
