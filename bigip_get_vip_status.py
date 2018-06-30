#!/bin/python
# makes an api call to an F5 node and dumps the results into a mysql table on the local host 
# @nkatwesigye@gmail.com

from __future__ import print_function, unicode_literals
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from subprocess import call
from f5.bigip import ManagementRoot
from  db_connect import db_connection
from generate_credentials import rsa_decrypt_credentials
import os
import subprocess
import time
import sys
import getopt
import xmlrpclib
import base64
import sys
import mysql.connector
import generate_credentials as cred

def usage():
  print ("Usage:")
  print ("     User must supply  either of these options -s -f -u -k -d  for the script to work")
  print ('     Usage: '+sys.argv[0]+' -s <F5 device name> -h <help > -d <db_sceret_password_file>-k <Private key file name> -u <user> -f <secret_password file name> [option]')
  print ('     Example: #python bigip_get_vip_status.py -u administrator -s 10.33.32.197 -f secret_file.txt -k id_rsa.pem ')

class vip_details(db_connection):

    def __init__(self,F5_server,F5_username,F5_credentials):
     self.F5_server       =   F5_server
     self.F5_username     =   F5_username
     self.F5_credentials  =   F5_credentials

    def get_vip_details(self):
        db_connection = self.cursor
        mgmt = ManagementRoot(self.F5_server,self.F5_username,str(self.F5_credentials))
        #pools = mgmt.tm.ltm.pools.get_collection()
        vips = mgmt.tm.ltm.virtuals.get_collection()
        for vip in vips:
            #print (dir(vip))
            vip_partition=str(vip.destination.split("/")[1])
            vip_ipaddress=str(vip.destination.split("/")[2])
            vip_name = vip.name
            db_connection.execute('insert into vip_status values ("%s","%s","%s","%s")\
            ON DUPLICATE KEY UPDATE F5_device_name="%s",vip_name="%s",vip_ipaddress="%s",\
            vip_partition="%s"' % ( F5_devicename,vip_name,vip_ipaddress,vip_partition,\
            F5_devicename,vip_name,vip_ipaddress,vip_partition))
            self.cnx.commit()

if __name__ == "__main__":
    if len(sys.argv) == 1:
      usage()
      sys.exit(2)

    # Get user input
    try:
      options, args = getopt.getopt(sys.argv[1:],'s:d:f:u:k:h',['F5device=','Secret_password_file=','User=','Private_key=','help'])
    except getopt.GetoptError as e:
      usage()
      sys.exit(2)

    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-s', '--F5server'):
           F5_server = arg
        elif opt in ('-u', '--User'):
           F5_username = arg
        elif opt in ('-f','--Secret_password_file'):
           F5_secret_password_file = arg
        elif opt in ('-d','--db_password_file'):
           db_sec_file = arg
        elif opt in ('-k','--Privatekey_file'):
           Private_key_file = arg
        else:
           usage()
           sys.exit(2)

    print (F5_username)
    print (F5_server)
    print (F5_secret_password_file)
    print (Private_key_file)
    F5_devicename = str(F5_server)
    # decrypt F5 credentials
    rsa_decrypt_credentials(Private_key_file,F5_secret_password_file)
    # create connection object to the F5_device
    vip_obj = vip_details(F5_server,F5_username,cred.cred_decrypted)
    # decrypt Database Credentials
    rsa_decrypt_credentials(Private_key_file,db_sec_file)
    # create db_connection object
    vip_obj.create_db_connection(cred.cred_decrypted,'f5_inventory')
    # Get f5 VIP details
    vip_obj.get_vip_details()
    # Close db_connection
    vip_obj.close_db_connection()
