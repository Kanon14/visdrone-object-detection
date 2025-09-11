import sys

def error_message_detail(error, error_detail: sys):
    """
    Generates a detailed error message including the script name, line number, and error description.
    
    :param error: The error object that was raised.
    :param error_detail: The sys module, used to extract traceback details.
    :return: A formatted error message string.
    """
    # Extract traceback details
    _, _, exc_tb = error_detail.exc_info()
    
    # Get the file name where the error occurred
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # Construct the error message with script name, line number, and error description
    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))
    
    return error_message


class AppException(Exception):
    """
    Custom exception class for handling and formatting application-specific errors.
    """
    
    def __init__(self, error_message, error_detail):
        """
        Constructor for the AppException class.
        
        :param error_message: A brief description of the error.
        :param error_detail: The sys module for accessing traceback details.
        """
        super().__init__(error_message)
        
        # Generate a detailed error message using the error_message_detail function
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail)
        
    def __str__(self):
        """
        Returns the formatted error message when the exception is printed or logged.
        """
        return self.error_message