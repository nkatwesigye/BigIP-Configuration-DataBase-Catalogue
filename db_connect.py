#!/bin/python
# make and close mysql_database connections 
# @nkatwesigye@gmail.com 
from subprocess import call
import os
import subprocess
import time
import sys
import getopt
import xmlrpclib
import base64
import sys
import mysql.connector

class db_connection(object):
    def create_db_connection(self,connection_password,database_name,host='127.0.0.1'):
       self.connection_password = connection_password
       self.cnx = mysql.connector.connect(user='root'\
       , password=self.connection_password,host=host,database= database_name)
       self.cursor = self.cnx.cursor()
    def close_db_connection(self):
       self.cursor.close()
       self.cnx.close()
