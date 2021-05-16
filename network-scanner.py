#! /usr/bin/python3

#scapy lets us probe, scan or attack networks.
from re import VERBOSE
import scapy.all as scapy

#Function that allow us to scan the ip address provided
def scan(ip):
    #this send an ARP request to the ip range provided
    arp_request = scapy.ARP(pdst = ip)
    #stored in broadcast, this make sure to send the broadcast MAC adress
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    #make a packet of a request comabining both ARP request and Broadcast
    arp_request_broadcast = broadcast/arp_request
    #stored the reponse of the ARP request, ans store the packets answered and unans store the packets unanswered
    ans_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]
    #print a table of IP/MAC response content
    print('IP\t\t\tMAC Address\n-----------------------------------------------')
    #print to the terminal the response of the answered packets
    for element in ans_list:
        print(element[1].psrc +'\t\t'+ element[1].hwsrc)
    

  

#We call the function scan
ip_address = "192.168.1.0/24"
scan(ip_address)