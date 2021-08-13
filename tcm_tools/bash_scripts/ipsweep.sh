#!/bin/bash

# Check if there is any input by the user before starting the attack
if [ "$1" == "" ]; then
    echo "[-] No arguments supplied. Please enter the IP address of the target."
    echo "[-] Example: ./ipsweep.sh 192.168.1.1"
    exit 1
else
# This is used to iterate over 1 to 254 and check if the IP is up or down
for ip in `seq 1 254`; do
ping -c 1  $1.$ip  | grep "64 bytes" | cut -d " " -f 4 | tr -d ":" & # The & is used to run the command mulitple times at the same time
done
fi
# this is used to iterate through every ip found with the ipsweep
# for ip in (cat ip.txt); do nmap $ip; done

