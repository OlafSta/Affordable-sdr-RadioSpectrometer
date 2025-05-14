# This code loads the processed hdf5 data and displays it as a waterfall graph. 
# The first function is the general version, while the sendon function marks the alocated frequencies from 500-2000MHz.

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

    if groups_data:
        batch_output_file = f"{output_file}_{part}.png"
        waterfall_save(main_central, sample_rate, sub_duration, batch_output_file, groups_data)


####################


frequency_plan = [
    {"range": "456 – 459 MHz", "use": "Ship Comm"},
    {"range": "459 – 460 MHz", "use": "Land Mobile"},
    {"range": "460 – 470 MHz", "use": "Mobile Pg"},
    {"range": "470 – 694 MHz", "use": "TV Astro"},
    {"range": "694 – 790 MHz", "use": "Mobile"},
    {"range": "790 – 862 MHz", "use": "Fixed/Mobile"},
    {"range": "862 – 890 MHz", "use": "Rail/GSM"},
    {"range": "890 – 942 MHz", "use": "Multi-use"},
    {"range": "942 – 960 MHz", "use": "Mixed"},
    {"range": "960 – 1164 MHz", "use": "Aero Nav"},
    {"range": "1164 – 1215 MHz", "use": "Aero Nav"},
    {"range": "1215 – 1240 MHz", "use": "Sat Nav"},
    {"range": "1240 – 1300 MHz", "use": "Sat/Amat"},
    {"range": "1300 – 1350 MHz", "use": "Aero/Amat"},
    {"range": "1350 – 1400 MHz", "use": "Fixed Links"},
    {"range": "1400 – 1427 MHz", "use": "Astro Sat"},
    {"range": "1427 – 1429 MHz", "use": "Fixed/Space"},
    {"range": "1429 – 1452 MHz", "use": "Fixed/Mobile"},
    {"range": "1452 – 1492 MHz", "use": "Broad Sat"},
    {"range": "1492 – 1518 MHz", "use": "Fixed/Mobile"},
    {"range": "1518 – 1525 MHz", "use": "Sat Comm"},
    {"range": "1525 – 1530 MHz", "use": "Space Op"},
    {"range": "1530 – 1535 MHz", "use": "SAR Sat"},
    {"range": "1535 – 1559 MHz", "use": "SAR Sat"},
    {"range": "1559 – 1610 MHz", "use": "Aero Nav"},
    {"range": "1610 – 1610.6 MHz", "use": "Aero Sat"},
    {"range": "1610.6 – 1613.8 MHz", "use": "Aero Sat"},
    {"range": "1613.8 – 1621.35 MHz", "use": "Aero Sat"},
    {"range": "1621.35 – 1626.5 MHz", "use": "Aero Sat"},
    {"range": "1626.5 – 1660 MHz", "use": "Sat Term"},
    {"range": "1660 – 1660.5 MHz", "use": "Radio Sat"},
    {"range": "1660.5 – 1668 MHz", "use": "Radio Sat"},
    {"range": "1668 – 1668.4 MHz", "use": "Sat/Radio"},
    {"range": "1668.4 – 1670 MHz", "use": "Sat/Radio"},
    {"range": "1670 – 1675 MHz", "use": "Met Sat"},
    {"range": "1675 – 1690 MHz", "use": "Met Sat"},
    {"range": "1690 – 1700 MHz", "use": "Met Sat"},
    {"range": "1700 – 1710 MHz", "use": "Met Sat"},
    {"range": "1710 – 1930 MHz", "use": "Mob Voice"},
    {"range": "1930 – 1970 MHz", "use": "IMT Mobile"},
    {"range": "1970 – 1980 MHz", "use": "IMT Mobile"},
    {"range": "1980 – 2010 MHz", "use": "IMT Sat"},
    {"range": "2010 – 2025 MHz", "use": "PMSE"},
    {"range": "2025 – 2110 MHz", "use": "Fixed/Space"},
    {"range": "2110 – 2120 MHz", "use": "Fixed"}
]


def waterfall_save(main_central, sample_rate, sub_duration, output_file, groups_data):
    # Determine overall frequency boundaries in MHz
    arr = np.sort(main_central)
    L = (arr[0] - sample_rate/2) / 1e6  # left boundary in MHz
    R = (arr[-1] + sample_rate/2) / 1e6  # right boundary in MHz

    # Determine time axis (assuming uniform number of rows across groups)
    min_rows = min(arr.shape[0] for arr in groups_data)
    time_axis = np.linspace(0, min_rows * sub_duration, min_rows)

    # Combine groups for the waterfall image (assumed side by side)
    combined_waterfall = np.hstack(groups_data)

    fig, ax = plt.subplots(figsize=(50, 6))
    im = ax.imshow(
        combined_waterfall,
        aspect="auto",
        extent=[L, R, time_axis[-1], time_axis[0]],
        cmap="viridis",
        vmin=-70,
        vmax=40
    )
    plt.colorbar(im, label="Power (dB)")

    # For each allocated frequency band, draw red vertical lines at the edges and
    # display the band label at the top of the plot.
    for band in frequency_plan:
        try:
            # Parse the frequency range (e.g., "456 – 459 MHz")
            parts = band["range"].replace("MHz", "").split("–")
            if len(parts) != 2:
                continue
            start_freq = float(parts[0].strip())
            end_freq = float(parts[1].strip())

            # Skip bands outside the plotted frequency range.
            if end_freq < L or start_freq > R:
                continue

            # Clip boundaries to the waterfall plot range.
            x0 = max(start_freq, L)
            x1 = min(end_freq, R)

            # Draw red vertical lines at the start and end frequencies.
            ax.axvline(x=x0, color='red', linestyle='-', linewidth=2)
            ax.axvline(x=x1, color='red', linestyle='-', linewidth=2)

            # Use the provided short label.
            label = band.get("use", band.get("uses", [""])[0])
            x_center = (x0 + x1) / 2
            # Place the label just above the plot (using axis transform)
            ax.text(x_center, 1.02, label, ha='center', va='bottom',
                    transform=ax.get_xaxis_transform(), color='red', fontsize=10)
        except Exception as e:
            print("Error processing band:", band, e)

    # (Optional) Add axis labels or a title here if desired.
    # ax.set_xlabel("Frequency (MHz)")
    # ax.set_ylabel("Time (s)")
    # ax.set_title("Waterfall Plot with Allocated Frequency Regions")

    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close(fig)


def generate_waterfall_plot(output_hdf5, sub_duration, output_file='waterfall'):
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

            for dataset_name in sorted(group.keys(), key=lambda x: float(x)):
                power = group[dataset_name][:]
                group_segments.append(power)

            if group_segments:
                group_array = np.array(group_segments)
                groups_data.append(group_array)
                main_central.append(central)

            current_total_jumps += 1

            if current_total_jumps >= max_total_jumps:
                batch_output_file = f"{output_file}_{part}.png"
                waterfall_save(main_central, sample_rate, sub_duration, batch_output_file, groups_data)
                part += 1
                groups_data = []
                main_central = []
                current_total_jumps = 0

    # Save any remaining groups.
    if groups_data:
        batch_output_file = f"{output_file}_{part}.png"
        waterfall_save(main_central, sample_rate, sub_duration, batch_output_file, groups_data)
