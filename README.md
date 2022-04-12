# node_upgrade
How to automate node upgrade process

The program checks the each step of the Nokia node release upgrade progress and warns/informs the user with relevant informations. 

The Python library Netmiko is used to send command to device. 

Sample Outputs when program is running: 

![image](https://user-images.githubusercontent.com/94804863/162928005-8656295b-e4ec-405f-8927-45f29189a9cc.png)

![image](https://user-images.githubusercontent.com/94804863/162928035-eb4e2868-e532-47eb-a85e-b5fd796b9e2c.png)

The following sample output in text format: 

A:SR7-3# admin redundancy synchronize boot-env
Syncing Boot environment
    boot option file : cf3:\bof.cfg ... OK
    boot loader      : cf3:\boot.ldr ...   ...   ...   ...   ... OK
    nvsys file       : cf3:\nvsys.info ... OK
    primary config : cf3:\load_balance_hash.cfg ... OK
    primary config : cf3:\load_balance_hash.ndx ... OK

It looks the current release is 16.0.R10.
The 'primary-image' configured as TiMOS-SR-20.7.R2/.
The 'secondary-image' configured as TiMOS-SR-16.0.R10.
Could you please confirm if you would like to upgrade to release TiMOS-SR-20.7.R2/ from release 16.0.R10?

Please press 'Y' for yes, 'N' for no, 'Q' to quit: Y
GOOD! It looks secondary-image configured as current release.
'bof save' is being run in the node. It might take time...
Writing BOF to cf3:/bof.cfg OK
Completed.
bof is saved with 'bof save' command.
The node is going to be rebooted to release TiMOS-SR-20.7.R2/.
Please confirm to run 'admin reboot now' for upgrade purpose. Press 'Y' to yes, 'N' to no, 'Q' to quit: Y
The node is rebooted for upgrade purpose.
SUCCESS! The node is successfully upgraded.

