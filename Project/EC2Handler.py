#!/usr/bin/python3

 #############################################################################
 #
 #
 #
 # DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
 #                 Version 2, December 2004
 #
 #      Everyone is permitted to copy and distribute verbatim or modified
 #      copies of this license document, and changing it is allowed as long
 #      as the name is changed.
 #
 #         DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE, 
 #         TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
 #
 #         0. You just DO WHAT THE FUCK YOU WANT TO
 #
 #  -----------------------------------------------------
 #  Sebastian Novak @ GitHub https://github.com/kernel-memory-dump
 #  -----------------------------------------------------
 #
 #
 # @author  Sebastian Novak
 #
 #
 #############################################################################

import boto3
import sys
import time
import json
from argparse import ArgumentParser

IMAGE_ID = "ami-b73b63a0"
DEFAULT_SECURITY_GROUP = "mrkrm2" 
DEFAULT_INSTANCE_TYPE = "t2.micro"
DEFAULT_KEYNAME = "aws-mrkirm2-key"
PUBLIC_IP_AVAILABLE_STATES =  ["running"]
PRIVATE_IP_AVAILABLE_STATES = [ "running", "stopping", "stopped"]
TERMINATE_ALLOWED_STATES = ["pending", "rebooting", "running", "shutting-down", "stopped", "stopping", "terminating"]
STOP_ALLOWED_STATES = ["pending", "rebooting", "running", "shutting-down", "stopping", "terminating"]

def fetch_all_available_instances():
    ec2 = boto3.resource('ec2')
    return ec2.instances.all()

def wrap_instances(instances):
    ec2_handlers = []
    for instance in instances:
        ec2_handlers.append(EC2Handler(instance, instance.id))
    return ec2_handlers

def fetch_wrapped_instances():
    instances = fetch_all_available_instances()
    return wrap_instances(instances)

########## ERRORS #################################################
class EC2HandlerError(Exception):
    pass

#

class EC2Handler:
    """Wraps EC2 instance resource, maintains persistent ec2 instance state through field-access interceptor"""

    def __init__(self, ec2_instance=None , instance_id=None):
        self.ec2_instance = ec2_instance 
        self.instance_id = instance_id
        self.ec2 = boto3.resource('ec2')

    def __getattribute__(self, name):
        """Intercept calls to 'self.ec2_instance' and fetch a fresh EC2 instance in  order to maintain consistent instance state

        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        # fetch EC2 instance state
        if name == 'ec2_instance':
            fresh_ec2_instance = boto3.resource('ec2').Instance(self.instance_id)
            object.__setattr__(self, 'ec2_instance', fresh_ec2_instance)

        return object.__getattribute__(self, name)

    def __load_init_script_as_string(self, path_to_init_script):
        try:
            bash_script = open(path_to_init_script, "r")
            script_content = bash_script.read()
            return script_content
        except:
            print("Failed to load")
            return ""

    def create_instance(self, path_to_init_script=None):
        """Create a new EC2 instance, using default type

        """
        init_user_data = ""
        if path_to_init_script is not None:
            init_user_data = self.__load_init_script_as_string(path_to_init_script)

        created_instances = self.ec2.create_instances(
                        ImageId = IMAGE_ID,
                        MinCount = 1,
                        MaxCount = 1,
                        KeyName = DEFAULT_KEYNAME,
                        SecurityGroups = [DEFAULT_SECURITY_GROUP],
                        InstanceType = DEFAULT_INSTANCE_TYPE,
                        UserData=init_user_data)

        # wait until instance is READY, state will be pending!
        try:
            self.instance_id = created_instances[0].id
            self.ec2_instance = created_instances[0]
            self.ec2_instance.wait_until_running()
        except:
            print("Instance did not start, create_instance failed!")
            print("Exception type:", str(sys.exc_info()[0]))
            print("Exception info:", str(sys.exc_info()[1]))
            return
        print("Created new instance with id:" + str(self.ec2_instance.id))
    
    def start_instance(self):
        """Attempts to start currently wrapped EC2 instance

        Args:
            None
        Returns:
            None
        Raises:
            EC2HandlerError if field 'ec2_instance' is not initialized
        """
        if self.ec2_instance == None:
            print ("Error, cannot start, EC2Handler assigned instance is None!")
            raise EC2HandlerError("Error, cannot start, EC2Handler assigned instance is None!")

        self.ec2_instance.start()
        self.ec2_instance.wait_until_running()
    
    def stop_instance(self):
        """Attempts to start currently wrapped EC2 instance

        Args:
            None
        Returns:
            None
        Raises:
            EC2Handler if field 'ec2_instance' is not initialized
        """
        if self.ec2_instance == None:
            print ("Error, perform stop_instance(), EC2Handler assigned instance is None!")
            raise EC2HandlerError("Error, cannot start, EC2Handler assigned instance is None!")
        if self.get_instance_state() not in STOP_ALLOWED_STATES:
            print ("Error cannot perform stop when instance is in state:" + str(self.get_instance_state()))
            raise EC2HandlerError("Error cannot perform stop when instance is in state:" + str(self.get_instance_state()))
        self.ec2_instance.stop()
        self.ec2_instance.wait_until_stopped()

    def terminate_instance(self):
        """Attempts to start currently wrapped EC2 instance

        Args:
            None
        Returns:
            None
        Raises:
            EC2HandlerError if field 'ec2_instance' is not initialized
        """
        if self.ec2_instance == None:
            print ("Error, cannot perform terminate_instance(), EC2Handler assigned instance is None!")
            raise EC2HandlerError("Error, cannot perform terminate_instance(), EC2Handler assigned instance is None!")
        print("terminating instance with id" + str(self.ec2_instance.instance_id))
        if self.get_instance_state() not in TERMINATE_ALLOWED_STATES:
            print ("Error cannot perform terminate when instance is in state:" + str(self.get_instance_state()))
            raise EC2HandlerError("Error cannot perform terminate when instance is in state:" + str(self.get_instance_state()))
        self.ec2_instance.terminate()
        self.ec2_instance.wait_until_terminated()
    
    def is_running(self):
        return self.get_instance_state() == "running"
            
    def get_instance_state(self):
        return self.ec2_instance.state['Name']

    def get_instance_states_as_json(self):
        pass  

    def print_instance_state(self):
        print(str(self.instance_as_str()))

    def instance_as_str(self):
        try:
            return_value = "\nInstance description:\n"
            return_value += "\nInstance id:" + str(self.instance_id)
            return_value += "\nImage id:"  + str(self.ec2_instance.image_id)
            return_value += "\nInstance type:" + str(self.ec2_instance.instance_type)
            return_value += "\nInstance state:" + str(self.ec2_instance.state['Name'])
            #verify that public_ip can be acquired
            if self.ec2_instance.state['Name'] in PUBLIC_IP_AVAILABLE_STATES:
                return_value +="\nInstance public IP: " + str(self.ec2_instance.public_ip_address)
            # verify that private_ip can be fetched 
            if self.ec2_instance.state['Name'] in PRIVATE_IP_AVAILABLE_STATES:
                return_value +="\nInstance private: " + str(self.ec2_instance.private_ip_address)
            return_value += "\n================="
            return return_value
        except:
            print("Exception type:", str(sys.exc_info()[0]))
            print("Exception info:", str(sys.exc_info()[1]))
            return None
    
