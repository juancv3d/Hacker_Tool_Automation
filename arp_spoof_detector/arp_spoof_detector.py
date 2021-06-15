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

# functions that capture packets or data of an interface


def sniff(interface):
    # this capture de packet of an specify interface, not sotring info in the memory
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


# function that print the packet to the terminal
def process_sniffed_packet(packet):
    # Check if this packet has a layer
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        print(packet.show)


# sotred the values of the get argument function
args = get_argument()
# call the sniff function
sniff(args.interface)
