#! /usr/bin/python3

#scapy lets us probe, scan or attack networks.
import scapy.all as scapy
#argparse lets us use arguments as input in our code
import argparse

#A function that creates arguments, can be use by the user to input an IP range
def get_argument():
    #We create an object of argparse
    parser = argparse.ArgumentParser()
    #We store the values of the target IP range
    parser.add_argument("-t", "--target", dest= "target", help= "The range of IP addres that you want to send the ARP request. EX: 192.168.1.0/24")
    #We capture the arguments
    args = parser.parse_args()
    #We make sure the arguments are not empthy
    if not args.target:
        #code to handle the error
        raise argparse.ArgumentTypeError("[-] Please specify an IP range, use --help for more info")
    else:
        #If everything is correct we return the arguments
        return args

#Function that allow us to scan the ip address provided for MAC adresses
def scan(ip):
    #this send an ARP request to the ip range provided
    arp_request = scapy.ARP(pdst = ip)
    #stored in broadcast, this make sure to send the broadcast MAC adress
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    #make a packet of a request combining both ARP request and Broadcast
    arp_request_broadcast = broadcast/arp_request
    #stored the reponse of the ARP request, ans store the packets answered and unans store the packets unanswered
    ans_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]

    #List of clients
    client_list = []
    #print to the terminal the response of the answered packets iterating in the list of answers
    for element in ans_list:
        #Dictionary that stored the information of the clients
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        #We append the values of the dictionary to the list
        client_list.append(client_dict)
    #Return the client list with the IP and the MAC addresses of the clients
    return client_list

#Function that print the results in the scan function   
def print_result(result_list):
    #print a table of IP/MAC response content
    print('IP\t\t\tMAC Address\n-----------------------------------------------')
    #We now iterate through the list to print the results
    for client in result_list:
        #print result of the client
        print(client["ip"] + "\t\t" + client["mac"])

#We store the argument provided by the user      
args = get_argument()
#Variable that store the output of the scan
scan_result = scan(args.target)
#We call the function print result to print the information of the clients
print_result(scan_result)

