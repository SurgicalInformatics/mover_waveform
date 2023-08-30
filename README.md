# MOVER Waveform Cleaning

This is the code repo for cleaning MOVER waveform data. The decode function is from the 'waveform_decode.py' file in the original MOVER data repo 

## Issues

1. Is there a data dictionary for the waveform data. What's the difference between 'ECG1' and 'GE_ECG'?
2. Is there existing open source cleaning code for inconsistent waveforms? The half of 'ECG1' is a straight line, for example (id=696793e068608e7c)

![id=696793e068608e7c](./fig/ecg2.png)

![](./fig/ecg1.png)

Another example is 'GE-ECG', while the first and second half of waveform have different scales.

![geecg](./fig/geecg.png)

![geecg](./fig/geecg2.png)
