import scapy.all as scapy
from scapy.layers.l2 import ARP, Ether
import optparse


def user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i", "--ip_address", dest="ip_address", help="Enter ip address")
    (inputs, arguments) = parse_object.parse_args()

    if not inputs.ip_address:
        print("Enter Ip Address")
    return inputs


def scan_network(ip):
    arp_request_package = ARP(pdst=ip)
    broadcast_package = Ether(dst="ff:ff:ff:ff:ff:ff")
    packages = broadcast_package / arp_request_package
    (answered_list, unanswered_list) = scapy.srp(packages, timeout=1)
    answered_list.summary()


user_ip_address = user_input()
scan_network(user_ip_address.ip_address)
