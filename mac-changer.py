#! /usr/bin/python3

#Subprocess lets us run commands in the shell
import subprocess
#argparse lets us put arguments to our .py file
import argparse
#re lets us search for patterns in a text
import re

#A function that create argumentas and can be use by the user 
#and specify the interface and the MAC address that the program needs to work correctly
def get_argument():
    #We create an object of argparse
    parser = argparse.ArgumentParser()
    #We can now store values in interface and new_mac and provide help for the user if needed
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change MAC address. Ex: wlan0")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address that the user want to use. Ex: 00:11:22:33:44:55")
    #We capture the arguments
    args = parser.parse_args()
    #We check that the arguments are not empthy
    if not args.interface:
        #code to handle error
        raise argparse.ArgumentTypeError("[-] please specify an interface, use --help for more info.")
    elif (not args.new_mac):
        #code to hamdle error
        raise argparse.ArgumentTypeError("[-] please specify a mac address, use --help for more info.")
    #we return the values given by the user is everything is correct
    return args

#This function run the commands neccesary to change the mac address
#Use the two inputs the interface and the MAC address that need to be changed
def change_mac(interface, new_mac): 
    #printint an information of whats happening
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    #Here we change the MAC address of the interface provided
    #First we shut down the interface
    subprocess.run(["ifconfig",interface,"down"])
    #Second we change the MAC address
    subprocess.run(["ifconfig",interface,"hw","ether",new_mac])
    #Then we start again the interface
    subprocess.run(["ifconfig",interface,"up"])
    


#This function check and return the current MAC address of the interface
def get_current_mac(interface):
    #We stored the ouput of the ifconfig command to check whetther or not the MAC address was succesfully changed
    ifconfig_result = subprocess.check_output(["ifconfig", args.interface ])
    #Now we search for a RegEx pattern within the ouput of the ifconfig and stored for later use
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig_result))
    #Check if there is any mac address in the output
    if mac_result:
        return mac_result.group(0)
    else:
        print("[-] Could not read MAC address")

#We call the function get argument of te user
args = get_argument()
#We call the function get current mac address and stored in a varibale
current_mac = get_current_mac(args.interface)
#We print the output of the current MAC
print("Current MAC =" + str(current_mac))

#Check whether the MAC address that we want to change is already set
if current_mac == args.new_mac:
   #Print a message that tell the user that the new MAC address in the argument is alredy set
   print("[-] The MAC address is currently " + args.new_mac + " use another MAC address")
else:
    #We called the function and add the output of the get argument function
    change_mac(args.interface, args.new_mac)
    #Then we check is the changed MAC address is the one that we provided
    current_mac = get_current_mac(args.interface)
    if current_mac == args.new_mac:
        #Print message to let the user know that the MAC address was sucesfully changed
        print("[+] MAC address was successfully changed to " + args.new_mac)
    else:
        #Print mesage to let the user know that the MAC did not changed
        print("[-] MAC address did not changed")

