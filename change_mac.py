

#!/usr/bin/python

import subprocess, optparse, re


def get_arguments(): #gets arguments from query that launch mac_changer
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify an new_mac, use --help for more info")
    return (options)
    

def change_mac(args):
    interface = args[0]
    new_mac = args[1]
    
    subprocess.call(["sudo", "ifconfig", interface, "down"]) #shut down inerface
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac]) #change shutted down interface's mac-address
    subprocess.call(["sudo", "ifconfig", interface, "up"]) #launch interface


def get_current_mac(interface): 
    ifconfig_result = subprocess.check_output(["ifconfig", interface]) #save "ifconfig 'inteface'"s result
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result)) #find interface's mac_address
    
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Can't read mac address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC address = " + str(current_mac))

change_mac((options.interface, options.new_mac))

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac: #compare mac from query and changed mac
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address didn't get changed")
