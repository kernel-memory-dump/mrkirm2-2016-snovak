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

INIT_SCRIPT = "ec2_init_template.sh"


def write_to_log(line):
    log_file = open("log.txt", "a")
    from datetime import datetime
    time_part = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file.write(time_part + ":" + line)
    log_file.close()

def main():
    print("Firing up EC2 server instance...")
    handler = EC2Handler()

    handler.create_instance(INIT_SCRIPT)
    if handler.ec2_instance is None:
        print("Fatal error: failed to create EC2 instance!")
        return


if __name__ == '__main__':
    main()