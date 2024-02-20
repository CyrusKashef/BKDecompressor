'''
Purpose:
*
'''

###################
##### IMPORTS #####
###################

from decompressor.src.generic_bin_file_class import Generic_Bin_File_Class
from decompressor.src.bk_constants import BK_CONSTANTS

######################################
##### CLANKERS CAVERN CODE CLASS #####
######################################

class CLANKERS_CAVERN_CODE_CLASS(Generic_Bin_File_Class):
    '''
    Pass
    '''
    def __init__(self, file_name:str):
        '''
        Constructor
        '''
        file_path:str = BK_CONSTANTS.EXTRACTED_FILES_DIR + file_name + BK_CONSTANTS.DECOMPRESSED_BIN_EXTENSION
        super().__init__(file_path)
    
    def disable_anti_tamper(self):
        '''
        Disables the anti-tampering functions for Clanker's Cavern assembly
        Thank You, Wedarobi! <3
        '''
        self._write_bytes_from_int(0x1984, 0x1000, byte_count=2)