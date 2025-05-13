============================
        REQUIREMENTS
============================

----------------------------
        Hardware
----------------------------

- RTL-SDR 
  I'm using the RTL-SDR v3 — it’s cheap and works well.
  SDRPlay also works, but needs a few tweaks in the code.

- Wideband Antenna 
  A discone antenna is ideal. Use a 50-ohm coaxial cable to connect it.

- External Hard Drive 
  Recordings take up a LOT of space!
  Get something with at least a few hundred GB free.

- Laptop (or Raspberry Pi)
  Works on both. On a Raspberry Pi, it’s a bit slower and might need minor code changes.

----------------------------
     Python Libraries
----------------------------

Install with pip:

    pip install h5py numpy matplotlib pyrtlsdr

Required Libraries:

- h5py        → for saving data in HDF5 format
- numpy       → for signal processing and math
- matplotlib  → for plotting waterfall graphs
- pyrtlsdr    → for controlling the RTL-SDR

(If using SDRPlay, you’ll also need `SoapySDR`)
