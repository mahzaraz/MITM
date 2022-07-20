import subprocess
import optparse
import re

print("Mac Address Changer Started")


def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i", "--interface", dest="interface", help="interface type to change")
    parse_object.add_option("-m", "-mac", dest="mac_address", help="use to type new mac address")
    return parse_object.parse_args()


def change_mac_address(user_interface, user_mac_address):
    subprocess.call(["ifconfig", user_interface, "down"])
    subprocess.call(["ifconfig", user_interface, "hw", "ether", user_mac_address])
    subprocess.call(["ifconfig", user_interface, "up"])


def control_new_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))

    if new_mac:
        return new_mac.group(0)
    else:
        return None


(inputs, arguments) = get_user_input()
change_mac_address(inputs.interface, inputs.mac_address)
final_mac = control_new_mac(str(inputs.interface))

if final_mac == inputs.mac_adress:
    print("Mac Address Changed")
else:
    print("Please, Try Again. Some Thing is Wrong!")
