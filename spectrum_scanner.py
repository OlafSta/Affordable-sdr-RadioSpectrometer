# This file contains all basic code bits from the scr directory in one place
# Part of this can be replaced with things like the modified waterfall plot that adds the frequency allocations 

import h5py
import numpy as np
import matplotlib.pyplot as plt

################
from rtlsdr import RtlSdr

###############
from datetime import datetime
import time


def RecordRtl(hdfile, central, samp, duration, sub_duration, gain=20):
    
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



  def main(start,end,duration,subduration, file_path):
    samplerate = 2e6 # 10e6

    if start < end:
        with h5py.File(file_path, "w") as hdfile:

            while start < end:
                center = start + (samplerate / 2)
                RecordRtl(hdfile, center, samplerate, duration, subduration, 40)
                start += samplerate   
    else:
        print("Error: start_freq is larger than end_freq, i.e. while loop will run forever")



def flat_field_correction(input_hdf5):
    ''' Computes a flat field correction array, by averaging over FFT amplitude data

    input_hdf5: Path to to HDF5 file containing the IQ data.
    Points: number of points in the data to get the correction curve.

    returns a flat_field array, correction factor to normalize FFT response.
    '''
    fft_sum = 0
    count = 0
    num = 10000

    with h5py.File(input_hdf5, 'r') as file:
        for group_name in sorted(file.keys(), key=lambda x: float(x)):
            group = file[group_name]
            for dataset_name in sorted(group.keys(), key= lambda x: float(x)):
                raw_samp = group[dataset_name][:]
                fft_result = np.fft.fftshift(np.fft.fft(raw_samp))
                amplitude = np.abs(fft_result)

                '''if fft_sum is None:
                    fft_sum = amplitude.copy()
                else:
                    fft_sum += amplitude'''
                fft_sum += amplitude
                count += 1

                if count>= num:
                    break
            if count>= num:
                break

    flat_field = fft_sum / count
    flat_field[flat_field == 0 ] = 1e-10
    return flat_field

def process_store2(input_hdf5, output_hdf5,sub_duration, flat_field): #exclude subdurtion in the final code
    '''Processes the IQ data,
    computes the FFT, applies flat field correction, and stors the results'''

    with h5py.File(input_hdf5, "r") as input_file, h5py.File(output_hdf5, "w") as output_file:
        sorted_group_names = sorted(input_file.keys(), key=lambda x: float(x))

        for group_name in sorted_group_names:
            input_group = input_file[group_name]
            output_group = output_file.create_group(group_name)

            sample_rate = input_group.attrs["sample_rate"]
            center_freq = input_group.attrs["center_freq"]
            #sub_duration = input_group.attrs['sub_dur']
            output_group.attrs["sample_rate"] = sample_rate
            output_group.attrs["center_freq"] = center_freq
            #output_group.attrs["sub_dur"] = sub_duration

            sorted_dataset_names = sorted(input_group.keys(), key= lambda x: float(x))
            for dataset_name in sorted_dataset_names:
                raw_samp = input_group[dataset_name][:]

                fft_result = np.fft.fftshift(np.fft.fft(raw_samp))
                power = np.abs(fft_result)

                corrected_power = power / flat_field

                corrected_power_db = 10 * np.log10(corrected_power)

                output_group.create_dataset(dataset_name, data=corrected_power_db, dtype='float32')

def waterfall_save(main_central, sample_rate, sub_duration, output_file, groups_data):
    arr = np.sort(main_central)

    L = (arr[0] - sample_rate/2) / 1e6
    R = (arr[-1] + sample_rate/2) / 1e6

    min_rows = min(arr.shape[0] for arr in groups_data)
    trimmed_groups = [arr[:min_rows, :] for arr in groups_data]
    time_axis = np.linspace(0, min_rows * sub_duration, min_rows)

    combined_waterfall = np.hstack(groups_data)

    fig = plt.figure(figsize=(50, 6))
    plt.imshow(
        combined_waterfall,
        aspect="auto",
        extent=[L, R, time_axis[-1], time_axis[0]],
        cmap="viridis",
        vmin=-70,
        vmax=40
        
    )
    plt.colorbar(label="Power (dB)")
    #plt.xlabel("Frequency (MHz)")
    #plt.ylabel("Time (s)")
    #plt.title("Combined Waterfall Plot (Side by Side)")
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close(fig)

def generate_waterfall_plot(output_hdf5, sub_duration,  output_file='waterfall'):
    groups_data = []
    main_central = []
    current_total_jumps = 0
    part = 1
    max_total_jumps = 25

    with h5py.File(output_hdf5, "r") as file:
        sorted_group_names = sorted(file.keys(), key=lambda x: float(x))

        for group_name in sorted_group_names:
            group = file[group_name]
            group_segments = []

            sample_rate = group.attrs["sample_rate"]
            central = group.attrs["center_freq"]
            #sub_duration = group.attrs["sub_dur"]
            

            for dataset_name in sorted(group.keys(), key=lambda x: float(x)):
                power = group[dataset_name][:]  # Load stored FFT power data
                group_segments.append(power)

            if group_segments:
                group_array = np.array(group_segments)
                groups_data.append(group_array)
                main_central.append(central)

            current_total_jumps += 1

            # Save waterfall if batch size is reached
            if current_total_jumps >= max_total_jumps:
                batch_output_file = f"{output_file}_{part}.png"
                waterfall_save(main_central, sample_rate, sub_duration, batch_output_file, groups_data)
                part += 1


                groups_data = []
                main_central = []
                current_total_jumps = 0

    # Save remaining data if any
    if groups_data:
        batch_output_file = f"{output_file}_{part}.png"
        waterfall_save(main_central, sample_rate, sub_duration, batch_output_file, groups_data)

def stack_images_ver(image_paths, output_path, no_stack):
    #non-original code
    
    images = [Image.open(path) for path in image_paths]

    max_width = max(image.width for image in images)
    total_height = sum(image.height for image in images)
    
    stacked_image = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))
    
    current_y = 0
    for image in images:
        if image.width < max_width:
            padded = Image.new('RGB', (max_width, image.height), color=(255, 255, 255))
            padded.paste(image, (0, 0))
            image = padded
        
        stacked_image.paste(image, (0, current_y))
        current_y += image.height
    
    stacked_image.save(output_path)

