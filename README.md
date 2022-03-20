# Raspberry Pi File Tree Editor

A set of tools to configure your raspberry pi's micro SD card before inserting it into raspberry for the first time. 

You can already setup wireless name and password, ssh parameters like port, generate and see ssh fingerprints before boot, change timezone, pi user password and place a script to run at first boot. More other improvements are coming, and I invite you to help.

PS: it might also work with other debian based distros, it all depends on what you want to do.

# Burn the raspbian image into an sd card

```
sudo dd if=2021-01-11-raspios-buster-armhf-full.img of=/dev/sda bs=4M conv=fsync
```

# How to

Just clone, edit the `setup_my_pi.py` with your configurations and run it. Don't forget to install paramiko:

```
pip3 install paramiko
git clone https://github.com/lattice0/raspberry_script_setup
cd raspberry_script_setup
cp setup_my_pi.py pi.py
chmod +x pi.py
#edit pi.py with your info
sudo ./pi.py
```
