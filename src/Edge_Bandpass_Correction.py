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
  

flat_field = flat_field_correction("Test.h5")



#########
# Some additional bits of code that let you plot the array and some other bits
'''
# Number of elements to display from the beginning, middle, and end
n = 5  # Adjust this number as needed

# Displaying the first few, middle, and last few numbers
middle_index = len(flat_field) // 2
print("First few elements:", flat_field[:n])
print("Middle elements:", flat_field[middle_index - n // 2:middle_index + n // 2])
print("Last few elements:", flat_field[-n:])

plt.figure(figsize=(10, 6))
plt.plot(flat_field, label='Flat Field Correction')
plt.xlabel('Freq.')
plt.ylabel('Amplitude')
plt.title('Flat Field Correction Array')
plt.legend()
plt.grid(True)
plt.show() '''
