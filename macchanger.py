#!/usr/bin/env python3
# Copyright 2018 Hackerboi6969
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
