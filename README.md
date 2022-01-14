# ANCS for Unicorn pHAT (on Pi Zero)

This is a fork of [ancs4linux](https://github.com/pzmarzly/ancs4linux) to display notification on a [Unicorn pHAT LEDs](https://github.com/pimoroni/unicorn-hat) running on a Raspberry Pi Zero.

## Building

The project consists of two daemons running in background.

```bash
sudo apt-get install -y libgirepository1.0-dev
git clone https://github.com/cl3m/ancs4linux
sudo ./ancs4linux/autorun/install.sh
```

## Start

If you previously paired the devices, unpair them on both ends (remove them from known device list). To start run the following command. You should see a rainbow on the Unicorn then on your mobile device, open Settings -> Bluetooth. You should see a your device (default name PiZero). If it does not work, try to connect with [nRF Connect for Mobile](https://apps.apple.com/ch/app/nrf-connect-for-mobile/id1054362403).

```bash
sudo ./ancs4linux/autorun/run.sh
```

Autostart by adding the following line to */etc/rc.local*

```bash
sudo /home/pi/ancs4linux/autorun/run.sh &
```