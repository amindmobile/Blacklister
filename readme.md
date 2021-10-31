# Mikrotik and Synology blacklist generator.


This script will help you create Mikrotik (and for Synology in the nearest future) firewall rules to block unwanted 
networks and IP addresses.

This script is supposed to work with the source lists of networks and IP addresses from 
[this website](https://www.iblocklist.com/). Thus, you must register on the above site and receive a your personal link 
to the list of ip addresses or networks you need to block on your devices. 

* The link to the list must be added to the script configuration file. 
* In the near future I will post instructions on how to do this. 
* And I will make it so that you can add such links simply when you run the script, without forcing you to edit the 
configuration file.

At the moment: 
* The script already allows you to get a ready-made set of rules for the Mikrotik firewall: BOGON and DROP.
(Just wait for instructions how to add links.)
* The script understands links to .zip archive format and 'cidr' file format in it. 
