'''
Purpose:
* Modifies code written for the c libraries
'''

###################
##### IMPORTS #####
###################

from decompressor.src.generic_bin_file_class import Generic_Bin_File_Class
from decompressor.src.bk_constants import BK_CONSTANTS

##################################
##### C LIBRARIES CODE CLASS #####
##################################

class C_LIBRARIES_CODE_CLASS(Generic_Bin_File_Class):
    '''
    Class for modifying code written for the c libraries
    '''
    def __init__(self, file_name:str):
        '''
        Constructor
        '''
        file_path:str = BK_CONSTANTS.EXTRACTED_FILES_DIR + file_name + BK_CONSTANTS.DECOMPRESSED_BIN_EXTENSION
        super().__init__(file_path)
    
    def disable_anti_tamper(self):
        '''
        Disables the anti-tampering functions for C Libraries assembly
        Thank You, Wedarobi! <3
        '''
        # code_10A00.c
        # if ((D_80379B90.unk4 != core2_D_803727F4) || (D_80379B90.unkC != D_80276574))
        self._write_bytes_from_int(0x10A1C, 0x00000000, byte_count=4)
        self._write_bytes_from_int(0x10A30, 0x1000, byte_count=2)
    
    def patch_yum_yum_crash_fix(self):
        '''
        Fixes a vanilla bug: 
        When a yumyum in TTC tries to eat a sprite in a cube,
        the game treats it as an actor, derefs an invalid pointer,
        and segfaults.
        Thank You, Wedarobi! <3
        '''
        # Write fix handler over vanilla debug strings
        # Might be replacing "u32 sns_get_next_key_in_range(void)"?
        # Part 1
        self._write_bytes_from_int(0x1D5EC, 0x03E00008, byte_count=4)
        self._write_bytes_from_int(0x1D5F0, 0x00000000, byte_count=4)
        # Part 2
        self._write_bytes_from_int(0x1D5F4, 0x1100000D, byte_count=4)
        self._write_bytes_from_int(0x1D5F8, 0x00000000, byte_count=4)
        self._write_bytes_from_int(0x1D5FC, 0x8D0A0000, byte_count=4)
        self._write_bytes_from_int(0x1D600, 0x000A4E02, byte_count=4)
        self._write_bytes_from_int(0x1D604, 0x34010080, byte_count=4)
        self._write_bytes_from_int(0x1D608, 0x55210008, byte_count=4)
        self._write_bytes_from_int(0x1D60C, 0x3C098000, byte_count=4)
        self._write_bytes_from_int(0x1D610, 0x012A4826, byte_count=4)
        # Part 3
        self._write_bytes_from_int(0x1D614, 0x3C010040, byte_count=4)
        self._write_bytes_from_int(0x1D618, 0x0121482A, byte_count=4)
        self._write_bytes_from_int(0x1D61C, 0x11200003, byte_count=4)
        self._write_bytes_from_int(0x1D620, 0x00000000, byte_count=4)
        self._write_bytes_from_int(0x1D624, 0x080E1C22, byte_count=4)
        self._write_bytes_from_int(0x1D628, 0x00000000, byte_count=4)
        self._write_bytes_from_int(0x1D62C, 0x080E1C28, byte_count=4)
        self._write_bytes_from_int(0x1D630, 0x00000000, byte_count=4)
    
    def booting_up_map(self, map_id:int=0x1F):
        '''
        When loading the game, this is the location the player boots up at
        Typically used to skip the Rareware & N64 logo cutscene and the concert
        '''
        # func_8023DBA4
        # default: MAP_1F_CS_START_RAREWARE
        self._write_bytes_from_int(0x18B, map_id, byte_count=1)