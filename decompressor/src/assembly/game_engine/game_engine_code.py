'''
Purpose:
* Modifies code written for the game engine
'''

###################
##### IMPORTS #####
###################

from decompressor.src.generic_bin_file_class import Generic_Bin_File_Class
from decompressor.src.bk_constants import BK_CONSTANTS

#############################
##### C LIBRARIES CLASS #####
#############################

class GAME_ENGINE_CODE_CLASS(Generic_Bin_File_Class):
    '''
    Class for modifying code written for the game engine
    '''
    def __init__(self, file_name:str):
        '''
        Constructor
        '''
        file_path:str = BK_CONSTANTS.EXTRACTED_FILES_DIR + file_name + BK_CONSTANTS.DECOMPRESSED_BIN_EXTENSION
        super().__init__(file_path)
    
    #################
    ##### WARPS #####
    #################
    
    def booting_up_map(self, map_id:int):
        '''
        When loading the game, this is the location the player boots up at
        Typically used to skip the Rareware & N64 logo cutscene and the concert
        Decomp:
        * code_14420.c#L271
        * code_956B0.c#L67
        '''
        self._write_bytes_from_int(0x1467F, map_id, byte_count=1)
        self._write_bytes_from_int(0x9580B, map_id, byte_count=1)
    
    #####################
    ##### CUTSCENES #####
    #####################
    
    def skip_jiggy_jig(self):
        '''
        Treats all instances of touching the Jiggy as if
        the player was underwater/in air/a transformation.
        '''
        # Skips Triggers For Jiggy Count < 3
        self._write_bytes_from_int(0x5780, 0x28410000, byte_count=4)
        # Skips Triggers For Collecting All Jinjos
        self._write_bytes_from_int(0x579C, 0x10000004, byte_count=4)
        # Always Runs Jiggy Jig Function For Transformations/Flying/Swimming
        self._write_bytes_from_int(0xF020, 0x00000000, byte_count=4)

    def enable_fallproof(self):
        '''
        Player will not receive fall damage when in tumble state.
        '''
        self._write_bytes_from_int(0x2D69C, 0x00000000, byte_count=4)
        self._write_bytes_from_int(0x2D6A0, 0x00000000, byte_count=4)
    
    ######################
    ##### PAUSE MENU #####
    ######################
    
    def enable_exit_to_witchs_lair(self):
        '''
        Allows players to exit the level by selecting
        'Exit To Witch's Lair' in the pause menu.
        '''
        # Disable Exit To Witch's Lair From TRUE to FALSE
        self._write_bytes_from_int(0x8BBF8, 0x00001025, byte_count=4)
        # Disable Debug Byte
        self._write_bytes_from_int(0x8BCE7, 0x00, byte_count=1)
    
    #################
    ##### MOVES #####
    #################
    
    def start_file_with_all_moves(self):
        '''
        Pass
        '''
        self._write_bytes_from_int(0xE84E, 0x0F98, byte_count=2)
    
    ###########################
    ##### TRANSFORMATIONS #####
    ###########################
    
    def set_transformation_costs(self, transformation_cost_dict:dict):
        '''
        Pass
        '''
        self._write_bytes_from_int(0x4A7E6, transformation_cost_dict[BK_CONSTANTS.TERMITE], byte_count=2)
        self._write_bytes_from_int(0x4A7EE, transformation_cost_dict[BK_CONSTANTS.CROCODILE], byte_count=2)
        self._write_bytes_from_int(0x4A7F6, transformation_cost_dict[BK_CONSTANTS.WALRUS], byte_count=2)
        self._write_bytes_from_int(0x4A7FE, transformation_cost_dict[BK_CONSTANTS.PUMPKIN], byte_count=2)
        self._write_bytes_from_int(0x4A7F6, transformation_cost_dict[BK_CONSTANTS.BEE], byte_count=2)