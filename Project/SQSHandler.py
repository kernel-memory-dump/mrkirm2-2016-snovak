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

class MessagePlaceHolder:
    """ Used to emulate SQS.Message class if a new Message has to be constructed from scratch """
    def __init__(self):
        self.message_attributes = {}
        self.body = ""
    def delete(self):
        print("placeholder delete invoked")

# used to extract ID from each message, attribute name is set by SQSHandler, user can set id via SQSMessage.set_id()
SQS_MESSAGE_ID_ATTRIBUTE = "msg-id"
# sender may set this to a final value in order to indicate that transcation includes a certain number of messages
# otherwise, the receiver is free to process messages as it sees fit
SQS_MESSAGE_TOTAL_COUNT = "total-msg-count"

class SQSMessage:
        """Wrapper for SQS messages"""
        def __init__(self, msg_body="", sqs_message=None):
            """ Use case scenarios:
                1. To wrap an exisisting message by passing a SQS.Message as 'sqs_message' argument
                2. To create a payload for queue.send_message method
            """
            if sqs_message is None:
                # create placeholder that can hold message attributes and body, required for 
                # send message invokation
                self.original_message = MessagePlaceHolder()
                self.original_message.body = msg_body
            else:
                self.original_message = sqs_message

        def set_message_body(self, payload):
            self.original_message.body = payload

        def get_message_body(self):
            return self.original_message.body

        def set_string_attribute(self, key, value):
            self.original_message.message_attributes[key] = {'StringValue' : value,'DataType': 'String'}

        def get_string_attribute(self, key):
            if self.original_message.message_attributes is None or key not in self.original_message.message_attributes:
                return None

            return self.original_message.message_attributes.get(key).get('StringValue')

        def set_number_attribute(self, key, value):
            self.original_message.message_attributes[key] = {'StringValue' : str(value),'DataType': 'Number'}

        def get_number_attribute(self, key):
            if self.original_message.message_attributes is None or key not in self.original_message.message_attributes:
                return None

            return int(self.original_message.message_attributes.get(key).get('StringValue'))

        def set_id(self, value):
            self.set_string_attribute(SQS_MESSAGE_ID_ATTRIBUTE, value)

        def get_id(self):
            return self.get_string_attribute(SQS_MESSAGE_ID_ATTRIBUTE)

        def set_total_number(self, value):
            self.set_number_attribute(SQS_MESSAGE_TOTAL_COUNT, value)

        def get_total_number(self):
            return self.get_number_attribute(SQS_MESSAGE_TOTAL_COUNT)

        def delete(self):
            self.original_message.delete()

        def get_as_queue_payload(self):
            """ Transforms MessageWrapper into queue.send_message argument type """
            print(str(self.original_message.message_attributes))
            return {
                "MessageBody" : self.original_message.body,
                "MessageAttributes" : self.original_message.message_attributes
                }



class SQSInbox:
    """Keeps track of received messages, prevents message duplication, maintains FIFO order
       Inbox is marked as full, after 'self.size'  messages have been received
    """
    def __init__(self, queue, size):
        self.inbox_map = {}
        self.size = size

    def is_full(self):
        """Attempts to upload specified file to current bucket

        Args:
            src (int): The first parameter.
            s3_key (str): The second parameter.
        Returns:
            None
        Raises:
            S3HandlerError if field 'bucket' is not initialized
        """
        return len(self.inbox_map.keys()) == self.size

    def put_msg(self, msg):
        self.inbox_map[msg.get_id()] = msg

    def delete_all_messages(self):
        for key in sorted(self.inbox_map.iterkeys()):
            self.inbox_map[key].delete()

    def inbox_to_str(self):
        pass

    def get_messages(self):
        values = []
        for key in sorted(self.inbox_map):
            values.append(self.inbox_map[key])
        return self.inbox_map.values()

    def clear(self):
        """ Empties the SQS inbox """
        self.inbox_map = {}

    def contains(self, msg):
        """ Checks if this messages was already placed in the inbox

        Args:
            msg (SQSMessage) - wrapped message
        Returns:
            (bool) True if message was found in inbox, False otherwise
        """

        return msg.get_id() in self.inbox_map



class SQSHandler:
    """Wrapper for SQS resource"""
    def __init__(self, queue_name, size=10, msg_attributes=None):
        """ Contructor, optional params include size and msg_attributes list required for receiving messages
        Args:
            queue_name (str): SQS queue name
            size (int): inbox size, number of messages to be received until inbox is full
            msg_attributes(list): list of messages attributes to be fetched when receiving messages, required only if handler is used to receive messages
                                  by default, the list always include 'msg-id'  value and 'total-msg-count'
        """
        self.sqs_resource = boto3.resource('sqs')
        self.queue_name = queue_name
        # sqs create checks if an SQS queue with the specified name already exists
        # if it exists, reference to existing queue is returned, not an error
        self.__queue = self.sqs_resource.create_queue(QueueName=self.queue_name)
        self.inbox = SQSInbox(self.__queue, size)
        if msg_attributes is None:
            self.msg_attributes = [SQS_MESSAGE_ID_ATTRIBUTE, SQS_MESSAGE_TOTAL_COUNT]
        else:
            # implicitly append 'msg-id' attribute
            msg_attributes.append(SQS_MESSAGE_ID_ATTRIBUTE)
            msg_attributes.append(SQS_MESSAGE_TOTAL_COUNT)
            self.msg_attributes = msg_attributes

    def receive_messages(self, count=10):
        messages = self.__queue.receive_messages(MaxNumberOfMessages=count, WaitTimeSeconds=10, MessageAttributeNames=self.msg_attributes, VisibilityTimeout=1)
        if messages is None or len(messages) is 0:
            return

        for msg in messages:
            # wrap BOTO3 message

            sqs_message = SQSMessage("", msg)
            # sanity check
            if sqs_message.get_id() is None:
                print("Skipping invalid msg:" + sqs_message.get_message_body())
                continue
            # check if inbox size has to be adjusted
            if sqs_message.get_total_number() != None and self.get_queue_size() != sqs_message.get_total_number():
                print("Received first message, adjusting inbox size to:" + str(sqs_message.get_total_number()))
                self.set_queue_size(sqs_message.get_total_number())
            # verify id , make sure its not a duplicate
            if self.inbox.contains(sqs_message):
                print("found duplicate msg, skipping it")
                continue
            # mark as processed
            #sqs_message.delete()
            print("Processing received msg:" + str(sqs_message.get_id()))

            self.inbox.put_msg(sqs_message)

    def send_message(self, msg):
        """ Sends specified SQSMessage (wrapped msg) via current queue
        Args:
            msg (SQSMessage): Wrapped message containing body and attributes
        """
        # unpack dictionary payload as input arguments
        self.__queue.send_message(**msg.get_as_queue_payload())

    def get_inbox(self):
        #returns wrapped inbox
        return self.inbox

    def is_inbox_full(self):
        return self.inbox.is_full()

    def get_outbox(self):
        # returns messages queued for sending
        pass

    def get_queue_size(self):
        return self.inbox.size

    def set_queue_size(self, size):
        self.inbox.size = size

    def delete(self):
        self.__queue.delete()

    

########## ERRORS #################################################
class SQSHandlerError(Exception):
    """Wrapper for SQS resource error"""
    pass
