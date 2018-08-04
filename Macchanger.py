#!/usr/bin/env python3
import subprocess
import sys
print("If you would like more updates and more things adding please feel free to donate to this Bitcoin address")

network="eth0"

for argument in sys.argv:
	if argument == "-w":
		network= "wlan0"

subprocess.call(f"ip link set {network} down", shell=True)
subprocess.call(f"macchanger -r {network}", shell=True)
subprocess.call(f"ip link set {network} up", shell=True)
subprocess.call("systemctl restart NetworkManager", shell=True)



