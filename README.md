meegi
=====

Toolkit for exploration of physiological signals onto tangible avatar representations

## How-to -- Augmentation

* computer 1, ?? patch

## How-to -- GUI

* computer 2, ?? patch

## How-to -- signals

Computer 3, software:

* tested with kubuntu 14.04
* OpemViBE 1.0

### DHCP server

The computer processing bitalino and openbci serves as a DHCP server on the local network, launch service with:

> service isc-dhcp-server start

LSL need multicast, enable this with:

> route add -net 224.0.0.0/4 dev eth0

### Signal acquisition and signal processing

Bitalino:

* plug respiration belt in analog 1, ECG in analog 3, EDA in analog 2 & 4
* pair bitalino with bluetooth, launch `./bitalino/client-bitalino.py` -- set the MAC address accordingly. 
* launch OpenViBE acquisiton server, grab bitalino LSL stream. Drift correction, 100ms, 32 chunk size (too small values may slow down drastically the computer).
* open OpenViBE designer and run `breath.xml`, `eda.xml` and `HR_auto.xml` scenarios.

OpenBCI:

* should work out of the box with the dongle, directly start OpenViBE acquisiton server with the right serial port selected (and the rights on it!). Select port 1025, same parameters as for bitalino (see `./processing/EEG_electrodes.txt` for electrodes placement).
* open OpenViBE designer and run `attention.xml`, `workload.xml`, `valence.xml`, `relax.xml`, `blinks.xml`, `muscle_noise.xml`
