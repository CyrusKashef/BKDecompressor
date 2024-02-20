'''
Purpose:
* Modifies code written for Spiral Mountain
'''

###################
##### IMPORTS #####
###################

from decompressor.src.generic_bin_file_class import Generic_Bin_File_Class
from decompressor.src.bk_constants import BK_CONSTANTS

######################################
##### SPIRAL MOUNTAIN CODE CLASS #####
######################################

class SPIRAL_MOUNTAIN_CODE_CLASS(Generic_Bin_File_Class):
    '''
    Class for modifying code written for Spiral Mountain
    '''
    def __init__(self, file_name:str):
        '''
        Constructor
        '''
        file_path:str = BK_CONSTANTS.EXTRACTED_FILES_DIR + file_name + BK_CONSTANTS.DECOMPRESSED_BIN_EXTENSION
        super().__init__(file_path)
    
    def disable_anti_tamper(self):
        '''
        Disables the anti-tampering functions for Spiral Mountain
        Thank You, Wedarobi! <3
        '''
        self._write_bytes_from_int(0x1D4, 0x1000, byte_count=2)
        self._write_bytes_from_int(0x1EC, 0x1000, byte_count=2)
        self._write_bytes_from_int(0x204, 0x1000, byte_count=2)
        self._write_bytes_from_int(0x3FA4, 0x00000000, byte_count=4)