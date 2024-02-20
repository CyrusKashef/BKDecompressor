'''
Purpose:
* Class to run the functions that implement modifying the ROM

ToDo:
* Add more features
'''

###################
##### IMPORTS #####
###################

# import argparse
import json

from decompressor.src.bk_rom_class import BK_ROM_CLASS
from decompressor.src.bk_constants import BK_CONSTANTS
from decompressor.src.assembly.assembly import ASSEMBLY_CLASS

####################
##### ARGPARSE #####
####################

######################################
##### MODIFICATION PROCESS CLASS #####
######################################

class MODIFICATION_PROCESS_CLASS():
    '''
    Class to run the functions that implement modifying the ROM
    '''
    def __init__(self):
        pass

    def _extract_decompress_files(self, old_rom_path:str):
        '''
        Extracts the assets and assembly files
        '''
        self._bk_rom = BK_ROM_CLASS(old_rom_path)
        self._bk_rom.clear_extracted_files_dir(BK_CONSTANTS.BIN_EXTENSION)
        self._bk_rom.extract_asset_table_pointers()
        self._bk_rom.extract_assembly_files()
        self._bk_rom.clear_extracted_files_dir(BK_CONSTANTS.COMPRESSED_BIN_EXTENSION)
    
    def _run_config_features(self):
        '''
        Pass
        '''
        with open(BK_CONSTANTS.CONFIG_FILE_PATH) as json_file:
            config_data:dict = json.load(json_file)
        assembly_object = ASSEMBLY_CLASS()
        if(config_data["DISABLE_ANTI_TAMPERING"]):
            assembly_object.disable_anti_tamper()
        if(config_data["PATCH_YUM_YUM_CRASH_FIX"]):
            assembly_object.patch_yum_yum_crash_fix()
        if(config_data["BOOT_TO_FILE_SELECT"]):
            assembly_object.boot_to_file_select()
        if(config_data["SKIP_JIGGY_JIG"]):
            assembly_object.skip_jiggy_jig()
        if(config_data["ENABLE_FALLPROOF"]):
            assembly_object.enable_fallproof()
        if(config_data["ENABLE_EXIT_TO_WITCHS_LAIR"]):
            assembly_object.enable_exit_to_witchs_lair()
        if(config_data["START_GAME_WITH_ALL_MOVES"]):
            assembly_object.start_file_with_all_moves()
        assembly_object.set_jigsaw_puzzle_costs(jigsaw_puzzle_list=[
            config_data["WORLD_PUZZLE_COSTS"]["MUMBOS_MOUNTAIN"],
            config_data["WORLD_PUZZLE_COSTS"]["TREASURE_TROVE_COVE"],
            config_data["WORLD_PUZZLE_COSTS"]["CLANKERS_CAVERN"],
            config_data["WORLD_PUZZLE_COSTS"]["BUBBLEGLOOP_SWAMP"],
            config_data["WORLD_PUZZLE_COSTS"]["FREEZEEZY_PEAK"],
            config_data["WORLD_PUZZLE_COSTS"]["GOBIS_VALLEY"],
            config_data["WORLD_PUZZLE_COSTS"]["MAD_MONSTER_MANSION"],
            config_data["WORLD_PUZZLE_COSTS"]["RUSTY_BUCKET_BAY"],
            config_data["WORLD_PUZZLE_COSTS"]["CLICK_CLOCK_WOOD"],
            config_data["WORLD_PUZZLE_COSTS"]["GRUNTILDA_FIGHT"],
            config_data["WORLD_PUZZLE_COSTS"]["DOUBLE_HEALTH"]
        ])
        assembly_object.set_note_door_values(note_door_list=[
            config_data["NOTE_DOOR_COSTS"]["50_NOTE_DOOR"],
            config_data["NOTE_DOOR_COSTS"]["180_NOTE_DOOR"],
            config_data["NOTE_DOOR_COSTS"]["260_NOTE_DOOR"],
            config_data["NOTE_DOOR_COSTS"]["350_NOTE_DOOR"],
            config_data["NOTE_DOOR_COSTS"]["450_NOTE_DOOR"],
            config_data["NOTE_DOOR_COSTS"]["640_NOTE_DOOR"],
            config_data["NOTE_DOOR_COSTS"]["765_NOTE_DOOR"],
            config_data["NOTE_DOOR_COSTS"]["810_NOTE_DOOR"],
            config_data["NOTE_DOOR_COSTS"]["828_NOTE_DOOR"],
            config_data["NOTE_DOOR_COSTS"]["846_NOTE_DOOR"],
            config_data["NOTE_DOOR_COSTS"]["864_NOTE_DOOR"],
            config_data["NOTE_DOOR_COSTS"]["882_NOTE_DOOR"]
        ])
        assembly_object.set_transformation_costs(transformation_cost_list=[
            config_data["TRANSFORMATION_COSTS"][BK_CONSTANTS.TERMITE],
            config_data["TRANSFORMATION_COSTS"][BK_CONSTANTS.CROCODILE],
            config_data["TRANSFORMATION_COSTS"][BK_CONSTANTS.WALRUS],
            config_data["TRANSFORMATION_COSTS"][BK_CONSTANTS.PUMPKIN],
            config_data["TRANSFORMATION_COSTS"][BK_CONSTANTS.BEE]
        ])
        assembly_object.save_all_assembly_changes()
    
    def _insert_compress_files(self, new_rom_path:str):
        '''
        Appends asset files and inserts assembly files
        '''
        self._run_config_features()
        self._bk_rom.append_asset_table_pointers()
        self._bk_rom.insert_assembly_files()
        self._bk_rom.rename_bk_rom()
        self._bk_rom.calculate_new_crc()
        self._bk_rom.save_as_new_rom(new_rom_path)
        self._bk_rom.clear_extracted_files_dir(BK_CONSTANTS.COMPRESSED_BIN_EXTENSION)

if __name__ == '__main__':
    old_rom_path:str = "C:/Users/Cyrus/Documents/VS_Code/BKDecompressor/BKDecompressor/Banjo-Kazooie.z64"
    new_rom_path:str = "C:/Users/Cyrus/Documents/VS_Code/BKDecompressor/BKDecompressor/Banjo-Kazooie-NEW.z64"
    modification_process_obj = MODIFICATION_PROCESS_CLASS()
    modification_process_obj._extract_decompress_files(old_rom_path)
    modification_process_obj._insert_compress_files(new_rom_path)