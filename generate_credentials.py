#!/bin/python
# takes an ecrypted file , decrepty and passes a clear text string to be used for authentication 
# @nkatwesigye@gmail.com
from __future__ import print_function, unicode_literals
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from subprocess import call
import os
import subprocess
import time
import sys
import base64
import sys


def rsa_decrypt_credentials(private_key_file,encrypted_credentials):
    ''' takes private key and encrypted credentials file , decrypts credentials 
    and returns decrypted string ''' 
    global cred_decrypted
    # read key file
    with open(private_key_file) as f: key_text = f.read()
    # create a private key object
    privkey = RSA.importKey(key_text)
    # create a cipher object
    cipher = PKCS1_v1_5.new(privkey)
    # decode base64
    with open(encrypted_credentials) as fh: full_text = fh.read()
    cipher_text = base64.b64decode(full_text)
    # decrypt
    plain_text     = cipher.decrypt(cipher_text, None)
    cred_decrypted = plain_text.decode('utf-8').strip()
    return cred_decrypted

