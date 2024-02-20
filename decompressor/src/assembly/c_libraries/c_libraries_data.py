'''
Purpose:
* Modifies data written for the c libraries
'''

###################
##### IMPORTS #####
###################

from decompressor.src.generic_bin_file_class import Generic_Bin_File_Class
from decompressor.src.bk_constants import BK_CONSTANTS

##################################
##### C LIBRARIES DATA CLASS #####
##################################

class C_LIBRARIES_DATA_CLASS(Generic_Bin_File_Class):
    '''
    Class for modifying data written for the c libraries
    '''
    def __init__(self, file_name:str):
        '''
        Constructor
        '''
        file_path:str = BK_CONSTANTS.EXTRACTED_FILES_DIR + file_name + BK_CONSTANTS.DECOMPRESSED_BIN_EXTENSION
        super().__init__(file_path)