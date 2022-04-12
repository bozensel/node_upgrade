from pprint import pprint
from ttp import ttp
import json
import time
import re
from ttp import ttp
from netmiko import ConnectHandler
import os
from termcolor import colored
import sys

def version_parser(data_to_parse):
    ttp_template = template_version

    parser = ttp(data=data_to_parse, template=ttp_template)
    parser.parse()

    # print result in JSON format
    results = parser.result(format='json')[0]
    #print(results)

    #converting str to json. 
    result = json.loads(results)
    
    return(result)

def bof_parser(data_to_parse):
    ttp_template = template_bof

    parser = ttp(data=data_to_parse, template=ttp_template)
    parser.parse()

    # print result in JSON format
    results = parser.result(format='json')[0]
    #print(results)

    #converting str to json. 
    result = json.loads(results)
    
    return(result)

  targetnode = {
'device_type': 'nokia_sros',
'ip': '172.29.6.137',
'username': 'user',
'password': 'password',
'port': 22,
}

remote_connect = ConnectHandler(**targetnode)
remote_connect.send_command("environment no more\n")
output = remote_connect.send_command_timing("admin redundancy synchronize config") # It's the 1st prerequisite command needs to be run before the upgrade.  
#print(output)
output2 = remote_connect.send_command_timing("\nadmin redundancy synchronize boot-env") # It's the 2st prerequisite command needs to be run before the upgrade.  
#print(output2)

time.sleep(60)


bof_output = remote_connect.send_command_timing("show bof")
#print(bof_output)
bof_parser(bof_output)

version_output = remote_connect.send_command_timing("show version")
#print(version_output)

print(f"It looks the current release is {version_parser(version_output)[0]['show_version']['Current_Release']}.")
print(f"""The 'primary-image' configured as {bof_parser(bof_output)[0]['bof_output']['primary_image']}.
The 'secondary-image' configured as {bof_parser(bof_output)[0]['bof_output']['secondary_image']}. 
Could you please confirm if you would like to upgrade to release {bof_parser(bof_output)[0]['bof_output']['primary_image']} from release {version_parser(version_output)[0]['show_version']['Current_Release']}?
""")

answer = input("Please press 'Y' for yes, 'N' for no, 'Q' to quit: ")

if answer == 'Y':
    if version_parser(version_output)[0]['show_version']['Current_Release'] not in bof_parser(bof_output)[0]['bof_output']['secondary_image']:
        print(colored("As a recommendation, current release should be saved as a 'secondary-image' incase there is a problem while new release is being installed.", "yellow"))
        print(f"Current release: {version_parser(version_output)[0]['show_version']['Current_Release']} secondary-image in bof: {bof_parser(bof_output)[0]['bof_output']['secondary_image']}")
    if version_parser(version_output)[0]['show_version']['Current_Release'] in bof_parser(bof_output)[0]['bof_output']['secondary_image']: # It case of a failure of primary-image, node will come up with secondary-image (with current one). 
        print(colored("GOOD! It looks secondary-image configured as current release.", "green"))
        print("'bof save' is being run in the node. It might take time...")
        bof_save_output2 = remote_connect.send_command_timing("bof save") # It should be saved otherwise there can be a problem in upgrading progress. 
        print(bof_save_output2)
        print("bof is saved with 'bof save' command.")

upgrade_counter = False

while True:
    if answer == 'Q':
        print(colored("You have cancelled the program.", "yellow"))
        break
    elif answer == "Y":
        print(f"The node is going to be rebooted to release {bof_parser(bof_output)[0]['bof_output']['primary_image']}.")
        answer_node_reboot_upgrade = input("Please confirm to run 'admin reboot now' for upgrade purpose. Press 'Y' to yes, 'N' to no, 'Q' to quit: ")
        if answer_node_reboot_upgrade == 'Y':
            remote_connect.send_command_timing("admin reboot now") # Right after this step, node will be reloaded and will come up with new release. 
            upgrade_counter = True 
            break
        elif answer_node_reboot_upgrade == 'N':
            print(colored("The node upgrade process is cancelled.", "yellow"))
            break
        elif answer_node_reboot_upgrade == 'Q':
            print(colored("The node upgrade process is cancelled.", "yellow"))
            break
    elif answer == "N":
        print(colored("The upgrade process is cancelled.", "yellow"))
        break
        
if upgrade_counter == True:
    print("The node is rebooted for upgrade purpose.")
    time.sleep(300) # The node needs to come up normally in 5 minutes. 
    version_output_after_upgrade = remote_connect.send_command_timing("show version") # Get the new release information. 
    new_release = version_parser(version_output_after_upgrade)[0]['show_version']['Current_Release']
    if new_release in bof_parser(bof_output)[0]['bof_output']['primary_image']: # Check if the new release in the primary-image under bof. If yes, which means the node is upgraded successfully. 
        print(colored("SUCCESS! The node is successfully upgraded.", "green"))
    elif new_release == version_parser(version_output)[0]['show_version']['Current_Release']: # Check if the new release is same with the previous one. If yes, which means the node is not upgraded, and it comes up with the same release as secondary-image under bof configured with current release, it was not upgraded with the new release information. 
        print(colored("FAIL! It looks the node comes up with current release. Please check all image files of new release.", "red")) 
    
