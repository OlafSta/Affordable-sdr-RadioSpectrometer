# Original code with no correction

def process_store(input_hdf5, output_hdf5,sub_duration):
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

                
                power_db = 10 * np.log10(power)

                output_group.create_dataset(dataset_name, data=power_db, dtype='float32')


###############
# This cod incorporates the edge correction

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

