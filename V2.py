def RecordRTL(start, end, duration, fft_size, file_path, gain=40):
    '''
    start = begining frequency
    end = end frequency
    duration = how long each recording will be
    fft_size = how accurate will the display be
    file_path = location where the hdf5 file will be saved to
    gain = the gain setting used on the RTL sdr
    
    Example -> RecordRTL(106e6,165e6,4,512, "18102025_Time_Test.h5)
    '''

    
    if start >= end:  #prevent while loop for going for ever
        print("Error")
        return

    sample_rate = 2e6
    
    sdr = RtlSdr() #open the sdr
    sdr.sample_rate = sample_rate #set sample rate of sdr 2MHz
    sdr.gain = gain #set this to auto??


    num_samples = int(sample_rate*duration)
    num_rows = num_samples // fft_size

    try:  #error cathcing
        with h5py.File(file_path, 'w') as hdfile:  #open a hdf5 file
            while start < end:
                center_freq = start + sample_rate/2
                sdr.center_freq = center_freq #center frequency 

                group = hdfile.create_group(f"{center_freq/1e6:.1f}")
    
                #Add recording here......
                _ = sdr.read_samples(2048) #gets rid of samples thats are 
                samples = sdr.read_samples(fft_size * num_rows)
                
                group.create_dataset("samples" , data=samples, dtype='complex64') #Compress data
                
                group.attrs['center_freq'] = center_freq 
                group.attrs['sample_rate'] = sample_rate
                group.attrs['duration'] = duration
                #subduration??
                group.attrs['gain'] = gain
                group.attrs['time_stamp'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                group.attrs['fft_size'] = fft_size
                
                start += sample_rate #moves to next center freq. 
                
    except Exception as e:
        print(f"Error: {e}")

    finally:
        sdr.close()
            
        

def Process(input_hdf5, output_hdf5, calibration_array=None):
    """
    Processes raw SDR data in an HDF5 file using FFT to generate averaged power spectra.
    
    input_hdf5: path to raw file from RecordRTL()
    output_hdf5: path to save processed FFT data
    sub_duration: duration of each sub-block (seconds) for averaging
    calibration_array: optional calibration correction array (same length as fft_size)
    """

    with h5py.File(input_hdf5, "r") as input_file, h5py.File(output_hdf5, "w") as output_file:
        sorted_group_names = sorted(input_file.keys(), key=lambda x: float(x))

        for group_name in sorted_group_names:
            input_group = input_file[group_name]
            output_group = output_file.create_group(group_name)

            # Read attributes
            center_freq = input_group.attrs["center_freq"]
            sample_rate = input_group.attrs["sample_rate"]
            duration = input_group.attrs["duration"]
            fft_size = input_group.attrs["fft_size"]

            samples = np.array(input_group["samples"])
            num_samples = len(samples)
            num_frames = num_samples // fft_size

            print(f"Processing {group_name} MHz: {num_frames} FFT frames")

            # Pre-allocate array to hold averaged spectrum
            spectrum = np.zeros(fft_size)

            # Process FFT frames
            window = np.hanning(fft_size)

            for i in range(num_frames):
                chunk = samples[i*fft_size:(i+1)*fft_size]
                chunk = chunk * window
                fft_result = np.fft.fftshift(np.fft.fft(chunk, fft_size))
                power = np.abs(fft_result)**2
                spectrum += power

            # Average the power spectrum
            spectrum /= num_frames
            spectrum_db = 10 * np.log10(spectrum + 1e-12)  # avoid log(0)

            # Apply calibration if provided
            if calibration_array is not None:
                if len(calibration_array) == fft_size:
                    spectrum_db -= calibration_array
                else:
                    print("Warning: Calibration array length does not match FFT size.")

            # Save processed data
            output_group.create_dataset("power_spectrum_db", data=spectrum_db)
            output_group.attrs["center_freq"] = center_freq
            output_group.attrs["sample_rate"] = sample_rate
            output_group.attrs["fft_size"] = fft_size
            output_group.attrs["duration"] = duration
            output_group.attrs["time_stamp"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            output_group.attrs["num_frames"] = num_frames

        print(f"Processing complete. Output saved to {output_hdf5}")


def generate_waterfall_plot(output_hdf5, output_file="waterfall.png"):
    """
    Creates a combined waterfall plot from processed FFT data.
    """
    freqs = []
    spectra = []

    with h5py.File(output_hdf5, "r") as file:
        sorted_groups = sorted(file.keys(), key=lambda x: float(x.split()[0]))
        for group_name in sorted_groups:
            group = file[group_name]
            spectrum = group["power_spectrum_db"][:]
            spectra.append(spectrum)
            freqs.append(group.attrs["center_freq"])

    if not spectra:
        print("No spectra found in file.")
        return

    waterfall = np.vstack(spectra)
    freq_axis = np.array(freqs) / 1e6  # MHz
    plt.figure(figsize=(12, 6))
    plt.imshow(
        waterfall,
        aspect="auto",
        extent=[freq_axis[0], freq_axis[-1], 0, waterfall.shape[0]],
        cmap="viridis",
        vmin=np.min(waterfall),
        vmax=np.max(waterfall)
    )
    plt.colorbar(label="Power (dB)")
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Scan index")
    plt.title("Waterfall Spectrum")
    plt.tight_layout()
    plt.savefig(output_file, dpi=200)
    plt.close()
    print(f"Waterfall plot saved as {output_file}")
