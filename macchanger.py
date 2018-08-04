#!/usr/bin/env python3

import subprocess
import sys
print("If you would like more updates and more things adding please feel free to donate to this Bitcoin address")

network = "eth0"

#create an iterable so we can use next()
iter_argv = iter(sys.argv)
for argument in iter_argv:
    if argument == "-w" or argument == "--wlan0": #backwards compatability
        network = "wlan0"
    elif argument == "-i" or argument == "--interface":
        try:
            network = next(iter_argv)
        except StopIteration: #if no interface was specified ("-i" is last arg)
            print("Must provide an interface!", file=sys.stderr) #write to stderr
            sys.exit(1)

subprocess.call(f"ip link set {network} down", shell=True)
subprocess.call(f"macchanger -r {network}", shell=True)
subprocess.call(f"ip link set {network} up", shell=True)
subprocess.call("systemctl restart NetworkManager", shell=True)
