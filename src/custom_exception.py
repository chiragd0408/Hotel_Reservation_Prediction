import traceback    # to track the error 
import sys          # system library


class Custom_excecption(Exception):

    def __init__(self,error_message, error_detail:sys):
        super().__init__(error_message)  # For inheriate use super
        self.error_message = self.get_detailed_error_message(error_message,error_detail)

    @staticmethod             # method became independent
    def get_detailed_error_message(error_message, error_detail:sys):

        _ , _ , exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename         # in which file the error occured
        line_number = exc_tb.tb_lineno


        return f"Error in {file_name} , line {line_number} : {error_message}"
    
    def __str__(self):
        return self.error_message
