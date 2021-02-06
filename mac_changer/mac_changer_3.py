
import subprocess
import optparse
import re


parse = optparse.OptionParser()

def get_input():

    parse.add_option("-i","--interface", dest="interface",help="interface to change!")
    parse.add_option("-m", "--mac",dest="mac_address",help="new mac address")
    return parse.parse_args()

def change_mac(user_interface, user_mac):

    subprocess.call(["ifconfig", user_interface, "down"])
    subprocess.call(["ifconfig", user_interface, "hw", "ether", user_mac])
    subprocess.call(["ifconfig", user_interface, "up"])

def control_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig))

    if new_mac:
        return new_mac.group(0)
    else:
        return None


print("My mac changer started!")

(user_inputs,arguments) = get_input()
change_mac(user_inputs.interface,user_inputs.mac_address)
final_mac = control_mac(str(user_inputs.interface))

if final_mac == user_inputs.mac_address:
    print("operations has been changed")
else:
    print("Error")










