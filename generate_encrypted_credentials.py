#!/bin/python 
# takes a string and creates an rsa encrypted file 
#@nkatwesigye@tesla.com

from __future__ import print_function, unicode_literals
import getpass
import base64
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def generate_secret_file(private_key,secret_file,password):
	key_text = open(private_key,"r").read()
	# import key via rsa module
	pubkey = RSA.importKey(key_text)
	# create a cipher via PKCS1.5
	cipher = PKCS1_v1_5.new(pubkey)
	# encrypt
	cipher_text = cipher.encrypt(str(password))
	# do base64 encode
	cipher_text = base64.b64encode(cipher_text)

	fh = open(secret_file,'w')
	fh.write(cipher_text)
	#.decode('utf-8'))
	fh.close()

if __name__ == "__main__":
	Secret_file = raw_input("Please Enter the Encrypted File name: ")
	Private_key = raw_input("Please Enter your Private key File name: ")
	F5Credential_PASSWORD = getpass.getpass("Please Enter the Password: ")
  	generate_secret_file(Private_key,Secret_file,F5Credential_PASSWORD)
