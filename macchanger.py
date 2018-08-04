#!/usr/bin/env python3

import subprocess
import sys

def handle_args(argv):
    """produce config based on passed arguments"""
    config = {"network": "wlan0"} #default config to return
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

def exit_on_error(returncode, message):
    """if command has non-zero exit code, print given error message to stderr
    and then exit with error code 1
    """
    if returncode != 0: #if command has failed, print given message to stderr and exit
        print(message, file=sys.stderr)
        sys.exit(1)

def main():
    #create an iterable so we can use next() then pass to handle_args
    config = handle_args(iter(sys.argv))
    network = config["network"]
    pipe = subprocess.PIPE #used to pipe command output to *_result variables

    down_result = subprocess.run(f"ip link set {network} down", shell=True, stderr=pipe) #send stderr output to down_result.stderr
    exit_on_error(down_result.returncode, "Could not set network down")

    #only output macchanger stdout if command succeeded - otherwise nothing of value to show
    mac_result = subprocess.run(f"macchanger -r {network}", shell=True, stderr=pipe, stdout=pipe)
    exit_on_error(mac_result.returncode, "Could not change MAC")
    #saved output is a byte string - convert to UTF-8, strip away the trailing newline character, then print it.
    print(mac_result.stdout.decode("utf-8").strip())

    up_result = subprocess.run(f"ip link set {network} up", shell=True, stderr=pipe)
    exit_on_error(up_result.returncode, "Could not set network up")

    result = subprocess.run("systemctl restart NetworkManager", shell=True, stderr=pipe)
    exit_on_error(result.returncode, "Could not restart NetworkManager")


if __name__ == "__main__":
    print("If you would like more updates and more things adding please feel free to donate to this Bitcoin address 14bnKzJWjYHYFndBuRbhth6aTbKGPjwmjg")
    main()
