#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    # Creates an instance of the OptionParser class
    parser = optparse.OptionParser()

    # This function updates various parts of the object with the information provided here
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change the MAC address for")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

    # This actually takes the input given in the command line and parses it and then returns updated versions of options and arguments objects.
    (options, arguments) =  parser.parse_args()

    # Error handling for the user not specifying the correct parameters in their command.
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.") 
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC address, use --help for more info.")
    # We only return the options object because we aren't using the parameters object.
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac + "...")

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    # Runs ifconfig and stores the output in our variable
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    # re.search returns matched instances as attributes of an object. We only have one match, so that will be group(0)
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")

# This function returns the options object which we are aptly naming options here to store it
options = get_arguments()

current_mac = get_current_mac(options.interface)
print("[+] Starting MAC is: " + str(current_mac))

# We call this function and can access the attributes of the options object added when the command was parsed. 
change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address successfully changed to: " + current_mac)
else:
    print("[-] Unable to change MAC address")
