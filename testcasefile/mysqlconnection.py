#!/usr/bin/env python
# coding: utf-8
"""
Created on Thu Jan 13 19:09:09 2022

@author: Rohit Singh Chauhan
"""


import unittest
import mysql.connector
import sshtunnel
import os

import pathlib
BASE_DIR = os.path.dirname(os.path.realpath('__file__')) # This returns the erdr_ml directory path
import sys
sys.path.append(BASE_DIR)

import json
import logging

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

class MySqlConnection:

    def __init__(self, param_config_filepath = 'default', param_without_ssh = True, 
                 param_MYSQL_HOST = None, param_MYSQL_PORT = None,
                 param_MYSQL_USERNAME = None, param_MYSQL_PASSWORD = None,
                 param_MYSQL_SSH_HOST = None, param_MYSQL_SSH_PORT = None,
                 param_MYSQL_SSH_USERNAME = None, param_MYSQL_SSH_PASSWORD = None,
                 param_MYSQL_DATABASE = None
		 ):

        self.without_ssh = param_without_ssh
        default_config_filepath = f"{BASE_DIR}\config.json"

        if param_config_filepath != 'default':
            self.config_filepath = param_config_filepath

        else:
            self.config_filepath = default_config_filepath

        config = open(self.config_filepath)
        config_data = json.load(config)

        MYSQL_USERNAME = config_data['MYSQL_USERNAME']
        
        print(MYSQL_USERNAME)
        MYSQL_PASSWORD = config_data['MYSQL_PASSWORD']
        MYSQL_HOST = config_data['MYSQL_HOST']
        MYSQL_PORT = config_data['MYSQL_PORT']
        
        MYSQL_SSH_HOST = config_data['MYSQL_SSH_HOST']
        MYSQL_SSH_PASSWORD = config_data['MYSQL_SSH_PASSWORD']
        MYSQL_SSH_PORT = config_data['MYSQL_SSH_PORT']
        MYSQL_SSH_USERNAME = config_data['MYSQL_SSH_USERNAME']

        MYSQL_DATABASE = config_data['MYSQL_DATABASE']

        if param_MYSQL_HOST:
            self.MYSQL_HOST = param_MYSQL_HOST
        else:
            self.MYSQL_HOST = MYSQL_HOST
        
        if param_MYSQL_PORT:
            self.MYSQL_PORT = param_MYSQL_PORT
        else:
            self.MYSQL_PORT = MYSQL_PORT

        if param_MYSQL_USERNAME:
            self.MYSQL_USERNAME = param_MYSQL_USERNAME
        else:
            self.MYSQL_USERNAME = MYSQL_USERNAME
        
        if param_MYSQL_PASSWORD:
            self.MYSQL_PASSWORD = param_MYSQL_PASSWORD
        else:
            self.MYSQL_PASSWORD = MYSQL_PASSWORD
        
        if param_MYSQL_SSH_HOST:
            self.MYSQL_SSH_HOST = param_MYSQL_SSH_HOST
        else:
            self.MYSQL_SSH_HOST = MYSQL_SSH_HOST

        if param_MYSQL_SSH_PORT:
            self.MYSQL_SSH_PORT = param_MYSQL_SSH_PORT
        else:
            self.MYSQL_SSH_PORT = MYSQL_SSH_PORT

        if param_MYSQL_SSH_USERNAME:
            self.MYSQL_SSH_USERNAME = param_MYSQL_SSH_USERNAME
        else:
            self.MYSQL_SSH_USERNAME = MYSQL_SSH_USERNAME

        if param_MYSQL_SSH_PASSWORD:
            self.MYSQL_SSH_PASSWORD = param_MYSQL_SSH_PASSWORD
        else:
            self.MYSQL_SSH_PASSWORD = MYSQL_SSH_PASSWORD
        
        if param_MYSQL_DATABASE:
            self.MYSQL_DATABASE = param_MYSQL_DATABASE
        else:
            self.MYSQL_DATABASE = MYSQL_DATABASE

        print(self.MYSQL_HOST)
    

    def connect_without_ssh(self):
        
        LOGGER.info('Connecting to ' + self.MYSQL_HOST + '\n')
        
        print('Connecting to ' + self.MYSQL_HOST + '\n')
        
        self.connection = mysql.connector.connect(host = self.MYSQL_HOST, port = self.MYSQL_PORT, user = self.MYSQL_USERNAME, password = self.MYSQL_PASSWORD) 

        LOGGER.info('\nMYSQL Client without ssh created\n')
        print('\nMYSQL Client without ssh created\n')

        
    def connect_with_ssh(self):

        LOGGER.info('\nConnecting to ' + self.MYSQL_HOST + '\n')
        
        print('\nConnecting to ' + self.MYSQL_HOST + '\n')
        
        
        LOGGER.info('\nssh tunnel created\n')
        print('\nssh tunnel created\n')
        
        self.server.start()
        
        LOGGER.info('\nServer started\n')
        print('\nServer started\n')
        
        with sshtunnel.SSHTunnelForwarder(
                (self.MYSQL_SSH_HOST, self.MYSQL_SSH_HOST),
                ssh_username=self.MYSQL_SSH_USERNAME,
                ssh_password=self.MYSQL_SSH_PASSWORD,
                remote_bind_address=(self.MYSQL_HOST, self.MYSQL_PORT),
                local_bind_address=('127.0.0.1', 3306)
        ) as tunnel:
            self.connection = mysql.connector.connect(
                user=self.MYSQL_USERNAME,
                password=self.MYSQL_PASSWORD,
                host='127.0.0.1',
                database=self.MYSQL_DATABASE,
                port=3306)
        
        LOGGER.info('\nMYSQL Client with ssh created\n')
        print('\nMYSQL Client with ssh created\n')
        
        
    def connect(self):
        if(self.without_ssh == True):
            self.connect_without_ssh()
            self.mysql_connection = self.connection
        else:
            self.connect_with_ssh()
            self.mysql_connection = self.connection


    
        
    
if __name__ == '__main__':
    test_connection = MySqlConnection()
    test_connection.connect()
    



"""
What I want to do :
If param_config_filepath is 
    1. new given file
        Take all parameters from that file and ignore defaults
        If something new is used in the individual parameters, supercede the parameters from given file
        and use only that for that specific parameter and use parameters from the given file for all the rest of the parameters.
    2. default
        Read default filepath for config.json and use the parameters from that file
        If something new is used in the individual parameters, supercede the parameters from default file
        and use only that for that specific parameter and use defaults for all the rest of the parameters.

"""

