#! /usr/bin/python3

# scapy lets us probe, scan or attack networks.
import scapy.all as scapy
# argparse allow us input arguments
import argparse

# function that creates arguments inputs for the user to enter the IP of the victim and the ip of the gateway


def get_argument():
    # We create an object of argparse
    parser = argparse.ArgumentParser()
    # We store the values of the interface
    parser.add_argument("-i", "--interface", dest="interface",
                        help="The interface you are using to connect to the network. EX eth0, wlan0")
    # store the input
    args = parser.parse_args()
    # We make sure the arguments are not empthy
    if not args.interface:
        # code to handle the error
        raise argparse.ArgumentTypeError(
            "[-] Please specify the interface, use --help for more info")
    else:
        # If everything is correct we return the arguments
        return args

# Function that return the MAC address of an IP


def get_mac(ip):
    # this send an ARP request to the ip range provided
    arp_request = scapy.ARP(pdst=ip)
    # stored in broadcast, this make sure to send the broadcast MAC adress
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # make a packet of a request combining both ARP request and Broadcast
    arp_request_broadcast = broadcast/arp_request
    # stored the reponse of the ARP request, ans store the packets answered and unans store the packets unanswered
    ans_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # return the MAC address of the IP specified
    return ans_list[0][1].hwsrc

# functions that capture packets or data of an interface


def sniff(interface):
    # this capture de packet of an specify interface, not sotring info in the memory
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


# function that print the packet to the terminal
def process_sniffed_packet(packet):
    # Check if this packet has a layer
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            # Check if the real mac is the same as the response mac
            if real_mac != response_mac:
                print("[+] You are under attack!")
                # print(packet.show)
        except IndexError:
            pass


# sotred the values of the get argument function
args = get_argument()
# call the sniff function
sniff(args.interface)
