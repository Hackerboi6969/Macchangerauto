#!/usr/bin/env python3

# Copyright 2018 Hackerboi6969
#
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

import subprocess as sp
from subprocess import PIPE
import sys

HELP = """Usage: ./macchanger.py arg [value]

ARGS:
  -e    --eth0          use eth0 as interface
  -i    --interface     specify interface as [value]
  -v    --verbose       give verbose error output
  -h    --help          show this help dialog

INTERFACE VALUES:
Will either be in form wlanX or wlpXsX depending on OS.
Default value is wlan0."""

# ANSI Escape Sequences for colours:
# \033[ starts escape sequence
# 30-39 are colours
# 0 = reset to default, 1 = bold, 3 = italic, 4 = underscore, 5 = blink
# options are semi-colon delimited
# m signifies end of escape sequence
RED = "\033[31;1m"
BOLD = "\033[1m"
NORMAL = "\033[0m"

class Config:
    """Configurable options for the running
    of the script set/got from here"""

    def __init__(self, iface, verbose):
        self.iface = iface
        self.verbose = verbose

def init_config(args):
    """Return instance of Config() after
    parsing script arguments for changed options"""

    iface = "wlan0"
    verbose = False
    next(args) # go past arg 0 (how script was called)

    for arg in args:
        if arg in ["-e", "--eth0"]:
            iface = "eth0"
        elif arg in ["-i", "--interface"]:
            try:
                iface = next(args)
            except StopIteration: #if "-i" was the last argument passed
                print("Must provide interface value", file=sys.stderr)
                sys.exit(1)
        elif arg in ["-v", "--verbose"]:
            verbose = True
        elif arg in ["-h", "--help"]:
            print(HELP)
            sys.exit(0) # exit code 0 because no errors
        else:
            print(HELP)
            sys.exit(1) # exit code 1 is standard exit error code

    return Config(iface, verbose)

def set_network(mode, conf):
    """Attempt to set network up/down by calling external
    command `ip` for specified interface"""

    result = sp.run(f"ip link set {conf.iface} {mode}", shell=True, stderr=PIPE)
    if result.returncode != 0:
        if conf.verbose:
            # stderr/stdout stored as byte strings, convert to UTF-8 and strip end newline char.
            stderr = result.stderr.decode("utf-8").strip()
            raise Exception(f"Could not set network {mode}: {stderr}")
        raise Exception(f"Could not set network {mode}")

def change_mac(conf):
    """Try to change MAC with external command `macchanger` for specified interface"""

    result = sp.run(f"macchanger -r {conf.iface}", shell=True, stderr=PIPE, stdout=PIPE)
    if result.returncode != 0:
        try:
            # try to set network up after failed attempt to change MAC
            set_network("up", conf)
        except Exception:
            if conf.verbose:
                stderr = result.stderr.decode("utf-8").strip()
                raise Exception(f"Could not change MAC, network down: {stderr}")
            raise Exception("Could not change MAC, network down")
        if conf.verbose:
            stderr = result.stderr.decode("utf-8").strip()
            raise Exception(f"Could not change MAC, network up: {stderr}")
        raise Exception("Could not change MAC, network up")
    stdout = result.stdout.decode("utf-8").strip()
    # convert str -> list, splitting on newline chars. New MAC is given on the 3rd output line,
    # so access the 3rd element of new list with [2] (lists are 0-indexed).
    new_mac = stdout.splitlines()[2]
    return new_mac

def restart_nm(conf):
    """Restart NetworkManager, otherwise network will not work properly"""

    result = sp.run("systemctl restart NetworkManager", shell=True, stderr=PIPE)
    if result.returncode != 0:
        if conf.verbose:
            stderr = result.stderr.decode("utf-8").strip()
            raise Exception(f"Could not restart NetworkManager: {stderr}")
        raise Exception("Could not restart NetworkManager")

def main():
    args = iter(sys.argv) # create iterable for nicer argument parsing
    conf = init_config(args)
    print("Donate BTC to support development: 14bnKzJWjYHYFndBuRbhth6aTbKGPjwmjg")

    # as soon as an error is encountered, script will go to except block and exit
    try:
        set_network("down", conf)
        new_mac = change_mac(conf)
        print(f"{BOLD}{new_mac}{NORMAL}")
        set_network("up", conf)
        restart_nm(conf)
    except Exception as err:
        print(f"{RED}Error:{NORMAL} {err}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
