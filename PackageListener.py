import scapy.all as sc
import scapy.layers.http


def listener(interface):
    sc.sniff(iface=interface, store=False, prn=analyze)


def analyze(packet):
    # packet.show()
    if packet.haslayer(scapy.layers.http.HTTPRequest):
        if packet.haslayer(sc.Raw):
            print(packet[sc.Raw].load)


listener("eth0")
