import sys
import logging

def error_message_detail(error, message:sys):
    _,_,exc_tb = message.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script {0} at line number {1} with error message {2}".format(
        filename, exc_tb.tb_lineno, str(error))
    
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, message:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, message = message)
    
    def __str__(self):
        return self.error_message
    

