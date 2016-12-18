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


from EC2Handler import EC2Handler
from EC2Handler import *

import sys

# python Vezba2.py instanceID amiID
def main():
    # inform user of proper usage if input arguments are invalid
    if len(sys.argv) != 3:
        print("Error, invalid usage, examples of valid usage:\n\tpython Vezba2.py instanceID AMI_ID\n\tpython Vezba.py None AMI_ID")
        sys.exit(1)
        return
    # Parse input arguments
    handler = None
    IMAGE_ID = sys.argv[2]
    instance_id = sys.argv[1]

    #FETCH all EC2 instances, using Boto3 resource, wrap all instances with EC2Handler
    wrapped_instances = fetch_wrapped_instances()

    output_file = open('output.txt','w')
    output_file.write("Existing instances states:\n")
    instance_with_id_exists = False

    for wrapped_instance in wrapped_instances:
        output_file.write(wrapped_instance.instance_as_str())
        if(wrapped_instance.instance_id == instance_id):
            print("Found instance with specified ID")
            instance_with_id_exists = True
            handler = wrapped_instance
            

    if instance_with_id_exists:
        print("Instance with specified ID " + str(instance_id) + " was found.")
    else:
        print("Did not find instance with specified ID! Creating new instance")
        handler = EC2Handler()
        handler.create_instance()
        instance_id = handler.instance_id
        output_file.write("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        output_file.write("\nNewly created instance:" + handler.instance_as_str())

    
    # check if current instance should be started?
    if not handler.is_running():
        print("Starting instance with id:" + str(handler.instance_id))
        handler.start_instance()

    handler.print_instance_state()
    print("Waiting 60 seconds, after which instance with ID: " + str(instance_id) + " will be stopped and terminated")
    time.sleep(60)
    print("Stopping instance with id: " + str(handler.instance_id))
    handler.stop_instance()
    handler.print_instance_state()
    print("Terminating instance with id: " + str(handler.instance_id))
    handler.terminate_instance()
    handler.print_instance_state()
    # write instance state

    output_file.write(handler.instance_as_str()) 
    output_file.close() 

if __name__ == '__main__':
    main()