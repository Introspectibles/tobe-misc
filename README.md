meegi
=====

Toolkit for exploration of physiological signals onto tangible avatar representations

## Public exhibition

### How-to -- Augmentation

* computer 1, ?? patch

### How-to -- GUI

* computer 2, ?? patch

### How-to -- signals

Computer 3, software:

* tested with kubuntu 14.04 and kubuntu 13.10 x64
    * dependencies: python-bluez (bitalino client)
* OpenViBE 1.0.1

#### DHCP server

The computer processing bitalino and openbci serves as a DHCP server on the local network. Set a *fixed* IP address, eg `192.168.200.2` and configure `/etc/dhcp/dhcpd.conf`:

> ddns-update-style none;
> option domain-name-servers 192.168.200.2;
> default-lease-time 600;
> max-lease-time 7200;
> option broadcast-address 192.168.200.255;
> subnet 192.168.200.0 netmask 255.255.255.0 {
>     range 192.168.200.200 192.168.200.254;
> }

Then launch service with:

> service isc-dhcp-server start

LSL need multicast, enable this with:

> route add -net 224.0.0.0/4 dev eth0

#### Signal acquisition and signal processing

Bitalino:

* plug respiration belt in analog 1, ECG in analog 3, EDA in analog 2 & 4
* pair bitalino with bluetooth, launch `./bitalino/client-bitalino.py` -- set the MAC address accordingly. 
* launch OpenViBE acquisiton server, grab bitalino LSL stream. Drift correction, 100ms, 32 chunk size (too small values may slow down drastically the computer).
* open OpenViBE designer and run `breath.xml`, `eda.xml` and `HR_auto.xml` scenarios.

OpenBCI:

* should work out of the box with the dongle, directly start OpenViBE acquisiton server with the right serial port selected (and the rights on it!). Select port 1025, same parameters as for bitalino (see `./processing/EEG_electrodes.txt` for electrodes placement).
* open OpenViBE designer and run `attention.xml`, `workload.xml`, `valence.xml`, `relax.xml`, `blinks.xml` and `muscle_noise.xml` (!)

## 2-users scenario

### Augmentation

?

### Signal acquisition and signal processing

FIXME: absolute path for lib lsl

Breathing and ECG require an OpenBCI board for each subject, see `sensors` folder.

Start accordingly 2 OpenViBE acquisition servers, set right ports in `config_acquisition_client_openbci.conf` and `configure config_acquisition_client_openbci_2.conf`.

Launch python script `./processing/SendStringMarkersGUI.py`, it'll be "Experiment Start/Stop" for the whole experiment, "Baseline" for first stage, "Segment" for second stage, "Trial" for third stage.


Finally, launch `./processing/coherence_openbci_first.xml`, `./processing/coherence_openbci_second.xml` and `./processing/coherence_sync.xml` to process data and feed to augmentation. First 2 to compute coherence for each subject, last one to compute a "sync" index, correlation between both heart rates.
