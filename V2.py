import h5py
import numpy as np
import matplotlib.pyplot as plt

################
from rtlsdr import RtlSdr


###############
from datetime import datetime
import time


def RecordRTL(start, end, duration, fft_size, file_path, gain=40):
    """
    Sweeps frequencies between 'start' and 'end'.
    
    Saves raw IQ samples into HDF5 groups.
    Each group = one center frequency span of 2 MHz.
    """

    if start >= end:
        print("Error: Start frequency must be lower than end frequency")
        return

    sample_rate = 2e6
    sdr = RtlSdr()
    sdr.sample_rate = sample_rate
    sdr.gain = gain

    num_samples = int(sample_rate * duration)

    try:
        with h5py.File(file_path, 'w') as hdfile:
            while start < end:
                center_freq = start + sample_rate / 2
                sdr.center_freq = center_freq

                group = hdfile.create_group(f"{center_freq/1e6:.3f}")

                _ = sdr.read_samples(2048)  # Flush tuner DC bias
                samples = sdr.read_samples(num_samples)

                group.create_dataset("samples", data=samples, dtype='complex64')

                # Store metadata
                group.attrs.update({
                    'center_freq': center_freq,

                    'sample_rate': sample_rate,
                    'duration': duration,
                    'gain': gain,
                    'fft_size': fft_size,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                })

                print(f"✔ Recorded {center_freq/1e6:.3f} MHz")
                start += sample_rate


    finally:
        sdr.close()


def FlatFieldCalibration(input_hdf5, max_frames=5000):
    """
    Calculates averaged amplitude correction curve across all datasets.
    """

    sum_fft = None
    count = 0

    with h5py.File(input_hdf5, 'r') as file:
        for group in file.values():
            samples = group["samples"][:]
            fft_size = group.attrs["fft_size"]
            window = np.hanning(fft_size)

            num_chunks = len(samples) // fft_size

            for i in range(min(num_chunks, max_frames)):
                chunk = samples[i*fft_size:(i+1)*fft_size] * window
                amplitude = np.abs(np.fft.fftshift(np.fft.fft(chunk)))

                if sum_fft is None:
                    sum_fft = amplitude
                else:
                    sum_fft += amplitude

                count += 1

    correction_curve = sum_fft / count
    correction_curve[correction_curve == 0] = 1e-12

    return correction_curve



def ProcessRTL(input_hdf5, output_hdf5, calibration_array=None):
    """
    Produces BOTH:
      - averaged spectrum
      - full waterfall
    """

    with h5py.File(input_hdf5, "r") as f_in, h5py.File(output_hdf5, "w") as f_out:

        for name in sorted(f_in.keys(), key=lambda x: float(x)):
            group_in = f_in[name]
            group_out = f_out.create_group(name)

            samples = group_in["samples"][:]
            fft_size = group_in.attrs["fft_size"]

            window = np.hanning(fft_size)

            num_frames = len(samples) // fft_size
            waterfall = np.zeros((num_frames, fft_size))

            # Compute waterfall + averaged power
            avg_power = np.zeros(fft_size)

            for i in range(num_frames):
                chunk = samples[i*fft_size:(i+1)*fft_size] * window
                fft_result = np.fft.fftshift(np.fft.fft(chunk))
                power = np.abs(fft_result)**2

                waterfall[i, :] = 10*np.log10(power + 1e-12)
                avg_power += power


            # Apply averaging
            avg_power /= num_frames
            avg_db = 10*np.log10(avg_power + 1e-12)

            # Apply flat-field correction if provided
            if calibration_array is not None and len(calibration_array) == fft_size:
                avg_db -= calibration_array
                waterfall -= calibration_array
            elif calibration_array is not None:
                print("⚠ Calibration array size mismatch — skipping.")


            # Store output
            group_out.create_dataset("spectrum_avg_db", data=avg_db, dtype='float32')
            group_out.create_dataset("waterfall_db", data=waterfall, dtype='float32')

            # Copy metadata
            for k,v in group_in.attrs.items():
                group_out.attrs[k] = v
            


def generate_waterfall_plot(processed_hdf5, output_base='waterfall', batch_size=20):
    """
    Reads processed waterfall data from HDF5 and generates multi-panel waterfall images.
    
    batch_size controls how many frequency groups get placed into one image row.
    """
    
    groups_data = []
    centers = []
    batch_index = 1

    with h5py.File(processed_hdf5, "r") as f:
        group_names = sorted(f.keys(), key=lambda x: float(x))

        for g in group_names:
            group = f[g]
            if "waterfall_db" not in group:
                print(f"⚠ Skipping {g} — no waterfall dataset found")
                continue

            waterfall = np.array(group["waterfall_db"])

            centers.append(group.attrs["center_freq"])
            groups_data.append(waterfall)

            # once enough groups collected — save batch
            if len(groups_data) >= batch_size:
                save_waterfall_image(groups_data, centers, output_base, batch_index)
                batch_index += 1
                groups_data, centers = [], []

    # save any remaining frequencies
    if groups_data:
        save_waterfall_image(groups_data, centers, output_base, batch_index)


def save_waterfall_image(groups_data, centers, output_base, batch_index):
    """
    Stitches multiple waterfall matrices side-by-side into one figure.
    """

    # Sort by frequency
    sorted_pairs = sorted(zip(centers, groups_data), key=lambda x: x[0])
    centers_sorted, groups_sorted = zip(*sorted_pairs)

    # Ensure equal row count (time consistency)
    min_rows = min(g.shape[0] for g in groups_sorted)
    trimmed = [g[:min_rows, :] for g in groups_sorted]

    # Combine into a single large waterfall
    waterfall_full = np.hstack(trimmed)

    # Compute frequency scale
    #sample_rate = list(groups_data[0].shape)[-1]  # width = FFT size
    # Correct: read sample rate from metadata, not matrix size
    sample_rate =float(groups_sorted[0].attrs['sample_rate'] if hasattr(groups_sorted[0], "attrs") else 1 )

    
    L = (centers_sorted[0] - 1e6) / 1e6
    R = (centers_sorted[-1] + 1e6) / 1e6

    fft_size = groups_sorted[0].shape[1]         # number of bins
    seconds_per_frame = fft_size / sample_rate

    print(seconds_per_frame)

    time_end = min_rows * seconds_per_frame

    fig = plt.figure(figsize=(48, 6))
    plt.imshow(
        waterfall_full,
        cmap='viridis',
        aspect='auto',
        extent=[L, R, time_end, 0],
        vmin=np.percentile(waterfall_full, 1),
        vmax=np.percentile(waterfall_full, 99)
    )

    plt.colorbar(label="Power (dB)")
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Time (seconds)")
    plt.title(f"Waterfall Sweep (Batch {batch_index})")

    file_name = f"{output_base}_{batch_index}.png"
    plt.savefig(file_name, bbox_inches="tight", dpi=300)
    plt.close()

    print(f"✔ Saved {file_name}")




def stack_images_ver(image_paths, output_path, no_stack=False):
    images = [Image.open(path) for path in image_paths]

    max_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)

    stacked = Image.new("RGB", (max_width, total_height), (255, 255, 255))

    y_offset = 0
    for img in images:
        padded = Image.new("RGB", (max_width, img.height), (255, 255, 255))
        padded.paste(img, (0, 0))
        stacked.paste(padded, (0, y_offset))
        y_offset += img.height

    stacked.save(output_path)



