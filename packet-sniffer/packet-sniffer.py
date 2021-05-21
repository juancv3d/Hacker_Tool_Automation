#! /usr/bin/python3

#scapy lets us probe, scan or attack networks.
import scapy.all as scapy

#functions that capture packets or data of an interface
def sniff(interface):
    #this capture de packet of an specify interface, not sotring info in the memory
    scapy.sniff(iface= interface, store= False, prn= process_sniffed_packet)

#function that print the packet to the terminal
def process_sniffed_packet(packet):
    #print the capture information
    print(packet)

sniff("eth0")