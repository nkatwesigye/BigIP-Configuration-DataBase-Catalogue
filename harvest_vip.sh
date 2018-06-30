#!/bin/bash
# Discovery from F5_devices every 4 hours 
# @ nkatwesigye@gmail.com
# Takes a list of F5 assets and queries for VIP status , this is stored in an RDBMS 

# Assest name and user account variables 
useraccount = $2 
for device in ` cat F5_assets`; do
    python bigip_get_vip_status.py -u $username -s $device \ 
   -d secret_en_mysql -f secret2_file -k id_rsa.pem  
 done
