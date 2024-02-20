'''
Purpose:
* Modifies data written for the game engine
'''

###################
##### IMPORTS #####
###################

from decompressor.src.generic_bin_file_class import Generic_Bin_File_Class
from decompressor.src.bk_constants import BK_CONSTANTS

#############################
##### C LIBRARIES CLASS #####
#############################

class GAME_ENGINE_DATA_CLASS(Generic_Bin_File_Class):
    '''
    Class for modifying code written for the game engine
    '''
    def __init__(self, file_name:str):
        '''
        Constructor
        '''
        file_path:str = BK_CONSTANTS.EXTRACTED_FILES_DIR + file_name + BK_CONSTANTS.DECOMPRESSED_BIN_EXTENSION
        super().__init__(file_path)
    
    ######################
    ##### PAUSE MENU #####
    ######################
        
    def adjust_menu_for_witchs_lair(self):
        '''
        Changes the positioning, ordering, and sprite of
        the pause menu when 'Exit To Witch's Lair' is added.
        '''
        # Positioning
        self._write_bytes_from_int(0x8F5C, 0x002D, byte_count=2) # "RETURN TO GAME"
        self._write_bytes_from_int(0x8F6C, 0x004C, byte_count=2) # "EXIT TO WITCH'S LAIR"
        self._write_bytes_from_int(0x8F7C, 0x006B, byte_count=2) # "VIEW TOTALS"
        self._write_bytes_from_int(0x8F8C, 0x008A, byte_count=2) # "SAVE AND QUIT"
        # Ordering
        self._write_bytes_from_int(0x8F60, 0x3DCCCCCD, byte_count=4) # "EXIT TO WITCH'S LAIR"
        self._write_bytes_from_int(0x8F70, 0x3E4CCCCD, byte_count=4) # "VIEW TOTALS"
        self._write_bytes_from_int(0x8F80, 0x3E99999A, byte_count=4) # "SAVE AND QUIT"
        # Sprite
        self._write_bytes_from_int(0x8F6E, 0x05, byte_count=1) # Give "EXIT TO WITCH'S LAIR" the Gruntilda Sprite