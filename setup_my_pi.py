#!/usr/bin/env python3
#Automatic wifi, shh, etc setup of a recently burned raspibian SD image

from ImageEditorClass import * #The class that will deal with the file tree of a linux image

#---------------------BEGIN USER SCRIPT---------------------
from io_utils import *

paramiko = []

#If you don't need ssh key keygen then you can comment `import paramiko`
#import paramiko

#TODO: implement automatic download and burn of raspbian image
#download_file("https://downloads.raspberrypi.org/raspbian_latest")

#Where is your SD card with a burnt Raspbian image located?
raspbian_root = "/media/lz/rootfs/"
raspbian_boot = "/media/lz/boot/"

raspbian = ImageEditor(raspbian_root)
raspbian_boot = ImageEditor(raspbian_boot)

#Changes user´s password - VERY IMPORTANT! PICK SECURE PASSWORD (LONG AND RANDOM)
raspbian.change_user_password(user="pi", password="raspberry123")

#Look at zones.txt in this diretory to know your zone, or just navigate through /usr/share/zoneinfo on any linux to find your timezone
raspbian.change_timezone("America/Sao_Paulo")

#Put your authorized key here (the public key that can control your pi without passwords)
authorized_keys = "ssh-rsa XXXX...XXXX == cardno:000000000000"

#Setup of authorized keys file
ssh_home_folder = "home/pi/.ssh/"
#if we use `autohrized_keys`, it gets wiped by the ssh service on first boot, so we create a new one
authorized_keys_location = ssh_home_folder + "authorized_keys_2"
raspbian.create_file(authorized_keys_location, authorized_keys)
raspbian.modify_file_permissions(authorized_keys_location, 0o600)
raspbian.modify_file_permissions(ssh_home_folder, 0o700)
raspbian.modify_ownership(ssh_home_folder, "pi", "pi")
raspbian.modify_ownership(authorized_keys_location, "pi", "pi")

fingerprint = []

#Creates ssh keys on raspbian and generates SHA256 fingerprints. It's called only if you imported paramiko
if paramiko:
	fingerprints = raspbian.ssh_keygen(paramiko, save_to = "etc/ssh/")

#Configures the SSH file of raspbian
sshd_config = read_file("file_models/sshd_config")
sshd_config = replace(sshd_config, [
	      	["^Port [0-9]*", "Port 2323"],
			["^HostKey /etc/ssh/ssh_host_ed25519_key", "#HostKey /etc/ssh/ssh_host_ed25519_key"],
			["^#*\s*PasswordAuthentication \w+", "PasswordAuthentication no"],
			["^#*\s*PubkeyAuthentication \w+", "PubkeyAuthentication yes"]])
sshd_config += "\nAuthorizedKeysFile     %h/.ssh/authorized_keys_2"
#TODO: this does not work. Why?
#sshd_config += "\nServerAliveInterval 60"
ssh_config_sd_location = "etc/ssh/sshd_config"
raspbian.create_file(ssh_config_sd_location, sshd_config)
raspbian.modify_file_permissions(ssh_config_sd_location, 0o600)

#Removes script that generates ssh keys on first boot (only needs to be run if we used paramiko to generate ssh keys)
if paramiko:
	raspbian.remove_file("etc/systemd/system/multi-user.target.wants/regenerate_ssh_host_keys.service", do_backup=False) 

#Activate and start ssh daemon on first boot, in the next boots it'll just start
commands = ("/usr/sbin/update-rc.d ssh enable && /usr/sbin/invoke-rc.d ssh start"
	    " && sudo apt-get update && sudo apt-get install -y curl git python-pip python3-pip screen" #Space before && is important
	    " && export DEBIAN_FRONTEND=noninteractive && curl -fsSL get.docker.com -o get-docker.sh && sudo sh get-docker.sh"
            " && sudo pip install docker-compose ")
raspbian.run_once_at_boot(commands)

#Begins or overrides wpa_supplicant.conf file for the rigth country
raspbian.begin_wpa_supplicant_file("BR")

#Configures wifi. Don't forget to put your country correctly
raspbian.add_new_wifi_network(network_ssid = "wifi-name", 
		  network_password = "wifi-password")

#You can add more than one network!
raspbian.add_new_wifi_network(network_ssid = "wifi-name-2", 
		  network_password = "wifi-password-2")

if fingerprints:
	print("your fingerprints: ")
	print(fingerprints)
