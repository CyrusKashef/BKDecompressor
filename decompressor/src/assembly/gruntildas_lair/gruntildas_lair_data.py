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
##### GRUNTILDAS LAIR DATA CLASS #####
######################################

class GRUNTILDAS_LAIR_DATA_CLASS(Generic_Bin_File_Class):
    '''
    Pass
    '''
    def __init__(self, file_name:str):
        '''
        Constructor
        '''
        file_path:str = BK_CONSTANTS.EXTRACTED_FILES_DIR + file_name + BK_CONSTANTS.DECOMPRESSED_BIN_EXTENSION
        super().__init__(file_path)
    
    #############################
    ##### NOTE DOORS VALUES #####
    #############################
    
    def read_note_door_values(self):
        '''
        Pass
        '''
        note_door_list:list = []
        for curr_index in range(
                BK_CONSTANTS.NOTE_DOOR_COST_START_INDEX,
                BK_CONSTANTS.NOTE_DOOR_COST_END_INDEX,
                BK_CONSTANTS.NOTE_DOOR_COST_INTERVAL):
            note_door_value:int = self._read_bytes_as_int(curr_index, byte_count=2)
            note_door_list.append(note_door_value)
        return note_door_list
    
    def set_note_door_values(self,
            note_door_list:list=BK_CONSTANTS.DEFAULT_NOTE_DOOR_LIST):
        '''
        Pass
        '''
        for index_count, curr_index in enumerate(range(
                BK_CONSTANTS.NOTE_DOOR_COST_START_INDEX,
                BK_CONSTANTS.NOTE_DOOR_COST_END_INDEX,
                BK_CONSTANTS.NOTE_DOOR_COST_INTERVAL)):
            note_door_value:int = note_door_list[index_count]
            if(note_door_value != None):
                self._write_bytes_from_int(curr_index, note_door_value, byte_count=2)
    
    ###############################
    ##### JIGSAW PUZZLE COSTS #####
    ###############################
    
    def read_jigsaw_puzzle_costs(self):
        '''
        Pass
        '''
        jigsaw_puzzle_list:list = []
        for curr_index in range(
                BK_CONSTANTS.JIGSAW_PUZZLE_COST_START_INDEX,
                BK_CONSTANTS.JIGSAW_PUZZLE_COST_END_INDEX,
                BK_CONSTANTS.JIGSAW_PUZZLE_COST_INTERVAL):
            jigsaw_puzzle_cost:int = self._read_bytes_as_int(curr_index, byte_count=1)
            jigsaw_puzzle_list.append(jigsaw_puzzle_cost)
        return jigsaw_puzzle_list
    
    def set_jigsaw_puzzle_costs(self,
            jigsaw_puzzle_list:list=BK_CONSTANTS.DEFAULT_JIGGY_PUZZLE_LIST):
        '''
        Pass
        '''
        total_bit_requirement:int = 0
        current_bit_offset = BK_CONSTANTS.JIGSAW_PUZZLE_STARTING_BIT_OFFSET
        for index_count, curr_index in enumerate(range(
                BK_CONSTANTS.JIGSAW_PUZZLE_COST_START_INDEX,
                BK_CONSTANTS.JIGSAW_PUZZLE_COST_END_INDEX,
                BK_CONSTANTS.JIGSAW_PUZZLE_COST_INTERVAL)):
            jigsaw_puzzle_cost:int = jigsaw_puzzle_list[index_count]
            if(jigsaw_puzzle_cost == None):
                needed_bits = self._read_bytes_as_int(curr_index + 0x1, byte_count=1)
                total_bit_requirement += needed_bits
                self._write_bytes_from_int(curr_index + 0x2, current_bit_offset, byte_count=2)
                current_bit_offset += needed_bits
            else:
                needed_bits = max(jigsaw_puzzle_cost.bit_length(), 1)
                total_bit_requirement += needed_bits
                self._write_bytes_from_int(curr_index, jigsaw_puzzle_cost, byte_count=1)
                self._write_bytes_from_int(curr_index + 0x1, needed_bits, byte_count=1)
                self._write_bytes_from_int(curr_index + 0x2, current_bit_offset, byte_count=2)
                current_bit_offset += needed_bits
        if(total_bit_requirement > BK_CONSTANTS.JIGSAW_PUZZLE_ALLOTED_BIT_COUNT):
            error_message:str = \
                f"ERROR: set_jigsaw_puzzle_costs: " + \
                f"Attempted to use {total_bit_requirement}/{BK_CONSTANTS.jigsaw_puzzle_alloted_bit_count} alloted bits"
            print(error_message)
            raise SystemError(error_message)