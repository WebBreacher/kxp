#!/usr/bin/python -tt
'''
-------------------------------------------------------------------------------
Name:        KXP - Kismet XML Parser
Purpose:     Extract the proper BSSIDs from a Kismet .netxml file given an SSID
Author:      Micah Hoffman (@WebBreacher)
-------------------------------------------------------------------------------

Usage = ./kxp.py kismet_log.netxml
'''

import os, sys
import xml.etree.ElementTree as ET


#=================================================
# Constants and Variables
#=================================================
filter_out = []

#=================================================
# Functions & Classes
#=================================================

# The entire bcolors class was taken verbatim from the Social Engineer's Toolkit
# check operating system
def check_os():
    if os.name == "nt":
        operating_system = "windows"
    if os.name == "posix":
        operating_system = "posix"
    return operating_system

#
# Class for colors
#
if check_os() == "posix":
    class bcolors:
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'

        def disable(self):
            self.PURPLE = ''
            self.CYAN = ''
            self.BLUE = ''
            self.GREEN = ''
            self.YELLOW = ''
            self.RED = ''
            self.ENDC = ''

# if we are windows or something like that then define colors as nothing
else:
    class bcolors:
        PURPLE = ''
        CYAN = ''
        DARKCYAN = ''
        BLUE = ''
        GREEN = ''
        YELLOW = ''
        RED = ''
        ENDC = ''

        def disable(self):
            self.PURPLE = ''
            self.CYAN = ''
            self.BLUE = ''
            self.GREEN = ''
            self.YELLOW = ''
            self.RED = ''
            self.ENDC = ''

def main():

    print bcolors.GREEN + "\n[Start] " + bcolors.CYAN + "Starting the KXP script. Hang on."

    # Check how many command line args were passed and provide HELP msg if not right
    if len(sys.argv) == 2:
        kismet_log_file=sys.argv[1]
    else:
        print bcolors.RED + "[Error] " + bcolors.ENDC + "You need to enter in the NET XML Kismet logfile such as: %s [kismet_logfile.netxml]\n" % sys.argv[0]
        sys.exit()

    # Open the kismet_log_file (or try to)
    try:
        tree = ET.parse(kismet_log_file)

    except (IOError) :
        print bcolors.RED + "[Error] " + bcolors.ENDC + "Can't read file the logfile you entered."
        sys.exit()

    print bcolors.GREEN + "[Info] " + bcolors.CYAN + "Kismet Net XML file successfully read."

    # User enters in the SSIDs as a comma sep list
    print bcolors.YELLOW + "[Input]" + bcolors.ENDC + " the names of the SSIDs you want the BSSIDs for. If multiple, separate with commas. "
    target_ssids = sys.stdin.readline()
    target_ssid = target_ssids.split(",")

	##########
	# Real Work
	##########
    root = tree.getroot()
          
    # Cycle through the XML doc looking for the SSIDs that the user entered above
    for target in target_ssid:
        target = target.strip()
        target_counter = 0
        print bcolors.BLUE + "[Searching] " + bcolors.ENDC + "Now searching for " + bcolors.GREEN + "%s" % target

		# Cycle through the XML file and pull out the specific info
        for wireless_net in root.findall('wireless-network'):
            for ssid in wireless_net.findall('SSID'):
                essid = ssid.find('essid').text
                if essid == target:
                    target_counter += 1
                    bssid = wireless_net.find('BSSID').text
                    filter_out.append(bssid)
        print bcolors.YELLOW + "[Status] " + bcolors.ENDC + "Found %d networks with '%s' name." % (target_counter, target)
        
    print bcolors.GREEN + "[Finished] " + bcolors.ENDC + "Found %d total networks to filter. They are below.\n" % len(filter_out)
    
    ########
    # Output options
    # Regular Comma-Sep list of the BSSIDs
    #out_string = ','.join(filter_out)
	
    # Kismet config file "filter" content
    out_string = 'filter_tracker=ANY(!' + ',!'.join(filter_out) + ')'
    print out_string


#=================================================
# START
#=================================================

if __name__ == "__main__": main()