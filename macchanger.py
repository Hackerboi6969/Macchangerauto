#!/usr/bin/env python3

import subprocess
import sys

def handle_args(argv):
    """produce config based on passed arguments"""
    config = { "network": "wlan0" } #default config to return
    for argument in argv:
        if argument == "-e" or argument == "--eth0": #easy toggle for eth0
            config["network"] = "eth0"
        elif argument == "-i" or argument == "--interface":
            try:
                config["network"] = next(argv)
            except StopIteration: #if no interface was specified ("-i" is last arg)
                print("Must provide an interface!", file=sys.stderr) #write to stderr
                sys.exit(1)
    return config

def main():
    #create an iterable so we can use next() then pass to handle_args
    config = handle_args(iter(sys.argv))
    network = config["network"]

    subprocess.call(f"ip link set {network} down", shell=True)
    subprocess.call(f"macchanger -r {network}", shell=True)
    subprocess.call(f"ip link set {network} up", shell=True)
    subprocess.call("systemctl restart NetworkManager", shell=True)

if __name__ == "__main__":
    print("If you would like more updates and more things adding please feel free to donate to this Bitcoin address 14bnKzJWjYHYFndBuRbhth6aTbKGPjwmjg")
    main()
