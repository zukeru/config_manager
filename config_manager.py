#!/usr/bin/python
"""
SYNOPSIS

    config_manager.py

DESCRIPTION

    This software uses github to manage application configs. This is a config manager agent.
    
EXAMPLES

    None.

EXIT STATUS

    Module will raise an exception on abnormal termination.

AUTHOR

    Grant Zukel

INITIAL VERSION

    30-Sep-15

COPYRIGHT

    This script is in owned and (C) 2013 by Grant Zukel.  All rights are reserved.
    Use of this program without written permission is prohibited.    

VERSION HISTORY
    
    1.0   Initial version

"""
import collections
from ConfigParser import SafeConfigParser
import base64
import logging
import logging.config
import os
import psutil
import psycopg2
import random
from subprocess import Popen, PIPE
import sys
import time
import uuid
from boto.ec2 import cloudwatch
from boto.utils import get_instance_metadata
import datetime
from pygithub3 import Github

def shell_command_execute(command, logger):
    p = Popen(command, stdout=PIPE, shell=True)
    (output, err) = p.communicate()
    return output

def get_status(repo_location, logger):
    command = "cd %s; git fetch origin; git cherry master origin/master; "%repo_location
    git_status = shell_command_execute(command, logger)
    return git_status

def update_local(repo_location, logger):
    try:
        command = "cd %s; git pull; "%repo_location
        git_pull = shell_command_execute(command, logger)
        return 'success'
    except Exception as e:
        logger.error(str(e))
        return 'failure'
    
def replace_config(repo_location,enviroment,application_name,config_name,config_location, logger):
    try:
        replace_command = ("cp %s%s%s%s %s%s" % (repo_location,enviroment,application_name,config_name,config_location,config_name))
        replace_status = shell_command_execute(replace_command, logger)  
        return 'success'  
    except Exception as e: 
        logger.error(str(e))
        return 'failure'

def restart_application_name(application_name, restart_application, logger):
    try:
        if restart_application == 'true':
            reload_command = "service %s reload" % application_name
            reloaded = shell_command_execute(reload_command) 
            return reloaded
    except Exception as e:
        logger.error(str(e))
        return 'failure'
    
if __name__ == '__main__':
    #load loagger
    try:
        url = os.path.dirname(os.path.realpath(__file__)) + '/logging.ini'
        logging.config.fileConfig(url)
        logger = logging.getLogger('root')
    except Exception as e:
        logger.error(str(e))

    try:
        parser = SafeConfigParser()
        parser.read((os.path.dirname(os.path.realpath(__file__))) +'/config.ini')
        config_repo = parser.get('Github', 'config_repo')
        enviroment = parser.get('Github', 'enviroment')
        application_name = parser.get('Github', 'application_name')
        config_location = parser.get('Github', 'config_location')
        config_name = parser.get('Github', 'config_name')
        update_interval = parser.get('Github', 'update_interval')
        restart_application = parser.get('Github', 'restart_application')
        repo_location = parser.get('Github', 'repo_location')
    except Exception as e:
        logger.error(str(e))
    
    while True:
        try:
            if repo_location:    
                git_status = get_status(repo_location, logger)
                if git_status:
                    update_local = update_local(repo_location, logger)
                    if update_local == 'success':
                        replace_configs = replace_config(repo_location,enviroment,application_name,config_name,config_location, logger)
                        if replace_configs == 'success':
                            restart_application_name(application_name, restart_application, logger)
                        else:
                            logger.error('There has been an issue replacing the config. Please check the log.')
        except Exception as e:
            logger.error(str(e))
            sys.exit(2)
        time.sleep(float(update_interval))
 
        