#!/usr/bin/env python
import subprocess
import optparse
import re


def get_user_input():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Display interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Assign new MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface. Use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC, use --help for more info.")
    return options


def macjumbler(interface, new_mac):
    print("[+] Assigned new MAC address to " + interface + " >> " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


# Display the MAC address
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_user_input()
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

macjumbler(options.interface, options.new_mac)

# Check MAC returned is the address the user entered
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address successfully changed >> " + current_mac)
else:
    print("[-] MAC didn't get changed.")