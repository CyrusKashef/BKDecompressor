'''
Purpose:
* Class for running the ROM extracting and inserting workflows.

Extract & Decompress Workflow:
1) Extracts & decompresses all of the assets from the asset pointer table
2) Extracts & decompresses all of the assembly files, split into code and data

Compress & Insert Workflow:
1) Appends all of the assets to the end of the ROM
2) Adjusts the asset pointer table
3) Inserts assembly files to their hardcoded location
4) Renames the Banjo-Kazooie ROM name string
5) Calculates and sets the new CRC checksum values
6) Saves Banjo-Kazooie ROM file
7) Clears extracted files folder

TODO:
* Modify Assembly pointers to properly adjust for resizing and positioning
'''

###################
##### IMPORTS #####
###################

import os

from decompressor.src.generic_bin_file_class import Generic_Bin_File_Class
from decompressor.src.compression_class import COMPRESSION_CLASS
from decompressor.src.bk_constants import BK_CONSTANTS

########################
##### BK ROM CLASS #####
########################

class BK_ROM_CLASS(Generic_Bin_File_Class):
    '''
    Runs the ROM extracting and inserting workflows.
    '''
    def __init__(self, file_path:str):
        '''
        Constructor
        '''
        super().__init__(file_path)
        self._create_extracted_files_directory()
        # Variables
        self._append_address:int = BK_CONSTANTS.ROM_END_INDEX
        self._assembly_file_list:list = []
    
    #################
    ##### SETUP #####
    #################
        
    def _create_extracted_files_directory(self):
        '''
        Creates an extracted files directory.
        '''
        print(f"INFO: _create_extracted_files_directory: Creating extracted files directory...")
        if(not os.path.exists(BK_CONSTANTS.EXTRACTED_FILES_DIR)):
            os.mkdir(BK_CONSTANTS.EXTRACTED_FILES_DIR)
        print(f"INFO: _create_extracted_files_directory: Creation complete!")
        
    def _create_custom_files_directory(self):
        '''
        Creates a custom files directory.
        '''
        print(f"INFO: _create_custom_files_directory: Creating custom files directory...")
        if(not os.path.exists(BK_CONSTANTS.CUSTOM_FILES_DIR)):
            os.mkdir(BK_CONSTANTS.CUSTOM_FILES_DIR)
        print(f"INFO: _create_custom_files_directory: Creation complete!")

    ################################
    ##### EXTRACT & DECOMPRESS #####
    ################################

    # ASSET TABLE

    def _extract_asset_by_pointer(self, pointer_index_start:int, file_name:str):
        '''
        Extracts a singular compressed bin file from the ROM
        '''
        asset_index_start:int = self._read_bytes_as_int(pointer_index_start, 4) + BK_CONSTANTS.ASSET_TABLE_OFFSET
        asset_index_end:int = self._read_bytes_as_int(pointer_index_start + 0x8, 4) + BK_CONSTANTS.ASSET_TABLE_OFFSET
        file_path:str = f"{BK_CONSTANTS.EXTRACTED_FILES_DIR}{file_name}{BK_CONSTANTS.COMPRESSED_BIN_EXTENSION}"
        with open(file_path, "wb+") as comp_file:
            comp_file.write(self._file_content[asset_index_start:asset_index_end])

    def extract_asset_table_pointers(self):
        '''
        Extracts all of the compressed bin files from the ROM into an individual bin file and
        runs the decompression algorithm to create the decompressed bin file.
        '''
        print(f"INFO: extract_asset_table_pointers: Extracting and decompressing all assets...")
        for asset_id in range(
                BK_CONSTANTS.ASSET_TABLE_START_ID,
                BK_CONSTANTS.ASSET_TABLE_END_ID + 0x1):
            pointer_index_start:int = BK_CONSTANTS.ASSET_TABLE_START_INDEX + asset_id * BK_CONSTANTS.ASSET_TABLE_INTERVAL
            if(asset_id % 0x100 == 0):
                asset_id_hex_str:str = self._convert_int_to_hex_str(asset_id)
                pointer_hex_str:str = self._convert_int_to_hex_str(pointer_index_start, byte_count=4)
                print(f"DEBUG: extract_asset_table_pointers: Asset Id 0x{asset_id_hex_str} -> Pointer 0x{pointer_hex_str}")
            file_name:str = self._convert_int_to_hex_str(asset_id, byte_count=2)
            self._extract_asset_by_pointer(pointer_index_start, file_name)
            compressed_obj = COMPRESSION_CLASS(file_name, BK_CONSTANTS.COMPRESSED_STR)
            compressed_obj.decompress_file_main()
        print(f"INFO: extract_asset_table_pointers: Extraction and decompression complete!")

    # ASSEMBLY FILES

    def _get_assembly_address(self, upper_index:int, lower_index:int):
        '''
        Given the upper and lower index,
        grabs the values at the indices and formulates
        the ROM address of the Assembly code.
        '''
        upper_val:int = self._read_bytes_as_int(upper_index, byte_count=2)
        lower_val:int = self._read_bytes_as_int(lower_index, byte_count=2)
        if(lower_val > 0x7FFF):
            upper_val -= 1
        assembly_address:int = upper_val * 0x10000 + lower_val
        return assembly_address

    def _obtain_assembly_address_list(self):
        '''
        Grabs every assembly file's starting and ending ROM addresses.
        Returns a list of assembly addresses sorted by start addresses.
        '''
        assembly_address_list:list = []
        for asm_name in BK_CONSTANTS.ASSEMBLY_POINTER_DICT:
            assembly_dict:dict = BK_CONSTANTS.ASSEMBLY_POINTER_DICT[asm_name]
            start_upper_index:int = assembly_dict[BK_CONSTANTS.START_UPPER_STR]
            start_lower_index:int = start_upper_index + assembly_dict[BK_CONSTANTS.LOWER_OFFSET_STR]
            start_address:int = self._get_assembly_address(start_upper_index, start_lower_index)
            end_upper_index:int = assembly_dict[BK_CONSTANTS.START_UPPER_STR] + BK_CONSTANTS.END_OFFSET
            end_lower_index:int = end_upper_index + assembly_dict[BK_CONSTANTS.LOWER_OFFSET_STR]
            end_address:int = self._get_assembly_address(end_upper_index, end_lower_index)
            assembly_address_list.append((start_address, end_address, asm_name))
        return sorted(assembly_address_list)

    def _extract_file_by_address(self, file_name:str, start_address:int, end_address:int):
        '''
        Extracts a file by the starting and ending addresses
        '''
        file_path:str = f"{BK_CONSTANTS.EXTRACTED_FILES_DIR}{file_name}{BK_CONSTANTS.COMPRESSED_BIN_EXTENSION}"
        with open(file_path, "wb+") as comp_file:
            comp_file.write(self._file_content[start_address:end_address])

    def _extract_and_decompress_section(self, start_address:int, end_address:int):
        '''
        Extracts and decompresses a portion of the ROM.
        '''
        file_name:str = self._convert_int_to_hex_str(start_address)
        self._extract_file_by_address(file_name, start_address, end_address)
        compressed_obj = COMPRESSION_CLASS(file_name, BK_CONSTANTS.COMPRESSED_STR)
        compressed_obj.decompress_file_main()
        return file_name

    def extract_assembly_files(self):
        '''
        For each assembly file, extract and decompress
        the assembly code and data portions.
        '''
        print(f"INFO: extract_assembly_files: Extracting assembly files...")
        assembly_address_list:list = self._obtain_assembly_address_list()
        for start_address, end_address, asm_name in assembly_address_list:
            data_address:int = self._file_content.find(BK_CONSTANTS.BK_COMPRESSED_FILE_HEADER + b"\x00", start_address + 1, end_address)
            code_file_name:str = self._extract_and_decompress_section(start_address, data_address)
            data_file_name:str = self._extract_and_decompress_section(data_address, end_address)
            self._assembly_file_list.append((start_address, end_address, code_file_name, data_file_name, asm_name))
        print(f"INFO: extract_assembly_files: Extracting complete!")

    #####################################
    ##### COMPRESSION AND INSERTION #####
    #####################################
    
    # Asset Table

    def _append_file_to_rom(self, file_name:str):
        '''
        Adds the asset file to the back of the Banjo-Kazooie ROM.
        '''
        file_path:str = f"{BK_CONSTANTS.EXTRACTED_FILES_DIR}{file_name}{BK_CONSTANTS.COMPRESSED_BIN_EXTENSION}"
        with open(file_path, "rb") as comp_file:
           self._file_content.extend(bytearray(comp_file.read()))

    def _adjust_asset_pointer_table(self,
            pointer_index_start:int, compressed_content_length:int):
        '''
        Adjusts the asset pointer table to reflect the new locations of the asset files.
        '''
        end_address:int = self._append_address + compressed_content_length
        pointer_start_address:int = self._append_address - BK_CONSTANTS.ASSET_TABLE_OFFSET
        self._write_bytes_from_int(pointer_index_start, pointer_start_address, 4)
        pointer_end_address:int = end_address - BK_CONSTANTS.ASSET_TABLE_OFFSET
        self._write_bytes_from_int(pointer_index_start + 0x08, pointer_end_address, 4)
        self._append_address:int = end_address

    def append_asset_table_pointers(self):
        '''
        Readies all asset files for insertion and recalculates the CRC checksum values.
        '''
        print(f"INFO: append_asset_table_pointers: Start...")
        self._append_address:int = BK_CONSTANTS.ROM_END_INDEX
        custom_files_list = os.listdir(BK_CONSTANTS.CUSTOM_FILES_DIR)
        extracted_files_list = os.listdir(BK_CONSTANTS.EXTRACTED_FILES_DIR)
        for asset_id in range(BK_CONSTANTS.ASSET_TABLE_START_ID, BK_CONSTANTS.ASSET_TABLE_END_ID + 0x1):
            pointer_index_start:int = BK_CONSTANTS.ASSET_TABLE_START_INDEX + asset_id * BK_CONSTANTS.ASSET_TABLE_INTERVAL
            if(asset_id % 0x100 == 0):
                asset_id_hex_str:str = self._convert_int_to_hex_str(asset_id)
                pointer_hex_str:str = self._convert_int_to_hex_str(pointer_index_start, byte_count=4)
                print(f"DEBUG: append_asset_table_pointers: Asset Id 0x{asset_id_hex_str} -> Pointer 0x{pointer_hex_str}")
            file_name:str = self._convert_int_to_hex_str(asset_id, byte_count=2)
            raw_file_name:str = file_name + BK_CONSTANTS.RAW_BIN_EXTENSION
            decompressed_file_name:str = file_name + BK_CONSTANTS.DECOMPRESSED_BIN_EXTENSION
            if(raw_file_name in custom_files_list):
                file_type:str = BK_CONSTANTS.RAW_STR
            elif(raw_file_name in extracted_files_list):
                file_type:str = BK_CONSTANTS.RAW_STR
            elif(decompressed_file_name in custom_files_list):
                file_type:str = BK_CONSTANTS.DECOMPRESSED_STR
            elif(decompressed_file_name in extracted_files_list):
                file_type:str = BK_CONSTANTS.DECOMPRESSED_STR
            else:
                raise Exception(f"ERROR: append_asset_table_pointers: Pointer '{self._convert_int_to_hex_str(pointer_index_start)}' file not found!")
            compressed_obj = COMPRESSION_CLASS(file_name, file_type)
            compressed_content_length:int = compressed_obj.compress_asset_file_main()
            self._append_file_to_rom(file_name)
            self._adjust_asset_pointer_table(pointer_index_start, compressed_content_length)
        while(len(self._file_content) % 0x10 != 0):
            self._file_content.extend(bytearray(b"\xAA"))
        print(f"INFO: append_asset_table_pointers: Complete!")

    # ASSEMBLY FILES

    def _combine_code_and_data_files(self,
            compressed_code_file_path:str,
            compressed_data_file_path:str,
            new_file_path:str):
        '''
        Adds the compressed code and data files to form one assembly file.
        '''
        with open(compressed_code_file_path, "rb") as code_file:
            combined_content = code_file.read()
        with open(compressed_data_file_path, "rb") as data_file:
            combined_content += data_file.read()
        while(len(combined_content) % 0x10 != 0):
            combined_content += b"\x00"
        new_file_length:int = len(combined_content)
        with open(new_file_path, "wb+") as assembly_file:
            assembly_file.write(combined_content)
        return new_file_length
    
    def _insert_file_to_rom(self, file_path:str, start_index:int):
        '''
        Inserts a file's content into the BK ROM.
        '''
        with open(file_path, "rb") as comp_file:
           for count, index in enumerate(bytearray(comp_file.read())):
            self._file_content[start_index + count] = index

    def _adjust_assembly_pointer(self,
            assembly_address:int, upper_index:int, lower_index:int):
        '''
        Given an assembly address and indices,
        calculates and sets the new values.
        Functionally works, Game breaks :(
        '''
        start_upper_val:int = assembly_address // 0x10000
        start_lower_val:int = assembly_address & 0xFFFF
        if(start_lower_val > 0x7FFF):
            start_upper_val += 1
        self._write_bytes_from_int(upper_index, start_upper_val, byte_count=2)
        self._write_bytes_from_int(lower_index, start_lower_val, byte_count=2)

    def _calculate_and_set_assembly_pointers(self, asm_name:str, start_address:int, new_file_length:int):
        '''
        Calculates and writes the new assembly pointers.
        Functionally works, Game breaks :(
        '''
        start_upper_index:int = BK_CONSTANTS.ASSEMBLY_POINTER_DICT[asm_name][BK_CONSTANTS.START_UPPER_STR]
        start_lower_index:int = start_upper_index + BK_CONSTANTS.ASSEMBLY_POINTER_DICT[asm_name][BK_CONSTANTS.LOWER_OFFSET_STR]
        self._adjust_assembly_pointer(start_address, start_upper_index, start_lower_index)
        end_address:int = start_address + new_file_length
        end_upper_index:int = BK_CONSTANTS.ASSEMBLY_POINTER_DICT[asm_name][BK_CONSTANTS.START_UPPER_STR]
        end_lower_index:int = end_upper_index + BK_CONSTANTS.ASSEMBLY_POINTER_DICT[asm_name][BK_CONSTANTS.LOWER_OFFSET_STR]
        self._adjust_assembly_pointer(end_address, end_upper_index, end_lower_index)
        return end_address

    def _rom_padding(self, curr_address:int, end_address:int, padding:int=0xFF):
        '''
        Adds padding to a section of the ROM.
        '''
        while(curr_address < end_address):
            self._write_bytes_from_int(curr_address, padding, 1)
            curr_address += 1
        return curr_address

    def insert_assembly_files(self):
        '''
        Inserts the assembly files into the ROM.
        Currently uses previously hardcoded ROM addresses.
        Future plan: Have these hardcoded ROM addresses adjustable.
        '''
        print(f"INFO: insert_assembly_files: Start...")
        for start_address, end_address, code_file_name, data_file_name, asm_name in self._assembly_file_list:
            # Compress Files
            compressed_code_obj = COMPRESSION_CLASS(code_file_name, BK_CONSTANTS.DECOMPRESSED_STR)
            compressed_code_file_path = compressed_code_obj.compress_assembly_file()
            compressed_data_obj = COMPRESSION_CLASS(data_file_name, BK_CONSTANTS.DECOMPRESSED_STR)
            compressed_data_file_path:int = compressed_data_obj.compress_assembly_file()
            # Add Compressed Files Together
            new_file_path:str = BK_CONSTANTS.EXTRACTED_FILES_DIR + asm_name + BK_CONSTANTS.COMPRESSED_BIN_EXTENSION
            new_file_length:int = self._combine_code_and_data_files(
                compressed_code_file_path,
                compressed_data_file_path,
                new_file_path)
            self._insert_file_to_rom(new_file_path, start_address)
            # curr_address:int = self._calculate_and_set_assembly_pointers(asm_name, start_address, new_file_length)
            curr_address:int = start_address + new_file_length
            curr_address:int = self._rom_padding(curr_address, end_address, 0x00)
        self._rom_padding(curr_address, end_address, 0xFF)
        print(f"INFO: insert_assembly_files: Complete!")

    ####################
    ##### CHECKSUM #####
    ####################

    def _unsigned_long(self, int_val:int):
        '''
        Returns the last four bytes of the given integer.
        '''
        return int_val & 0xFFFFFFFF
    
    def _rotate_left(self, j:int, b:int):
        '''
        Rotate left machine language function.
        '''
        return self._unsigned_long(j << b) | (j >> (-b & 0x1F))

    def calculate_new_crc(self):
        '''
        Calculates the new CRC checksum values for Banjo-Kazooie.
        '''
        print(f"INFO: append_asset_table_pointers: Calculating New CRC Checksum...")
        t1 = t2 = t3 = t4 = t5 = t6 = BK_CONSTANTS.CIC
        for check_index in range(BK_CONSTANTS.CHECK_ROM_START_INDEX, BK_CONSTANTS.CHECK_ROM_END_INDEX, 0x4):
            d = self._read_bytes_as_int(check_index, byte_count=4)
            t6d = self._unsigned_long(t6 + d)
            if(t6d < t6):
                t4 = self._unsigned_long(t4 + 1)
            t6 = t6d
            t3 ^= d
            r = self._rotate_left(d, d & 0x1F)
            t5 = self._unsigned_long(t5 + r)
            if(t2 > d):
                t2 ^= r
            else:
                t2 ^= t6 ^ d
            t1 = self._unsigned_long(t1 + (t5 ^ d))
        crc1 = self._unsigned_long((t6 ^ t4) + t3)
        crc2 = self._unsigned_long((t5 ^ t2) + t1)
        self._write_bytes_from_int(BK_CONSTANTS.CRC1_INDEX_START, crc1, 4)
        self._write_bytes_from_int(BK_CONSTANTS.CRC2_INDEX_START, crc2, 4)
        print(f"INFO: append_asset_table_pointers: New CRC Checksum Set!")

    ##########################
    ##### POST FUNCTIONS #####
    ##########################

    def rename_bk_rom(self, bk_rom_name:str="BKDecompressor"):
        '''
        Renames the string at the beginning of the Banjo-Kazooie ROM file.
        '''
        if(len(bk_rom_name) > 20):
            raise Exception(f"ERROR: rename_bk_rom: BK ROM Name cannot exceed 20 characters: '{bk_rom_name}'")
        while(len(bk_rom_name) < 20):
            bk_rom_name += " "
        self._write_bytes_from_str(0x20, bk_rom_name)

    def save_as_new_rom(self, new_file_path:str):
        '''
        Saves the Banjo-Kazooie Rom to new destination.
        '''
        print(f"INFO: save_as_new_rom: Saving new ROM to '{new_file_path}'...")
        self._save_changes(new_file_path)
        print(f"INFO: save_as_new_rom: New ROM saved!")
    
    def clear_extracted_files_dir(self, filter:str):
        '''
        Removes bin files from the extracted files directory that end with a certain filter
        '''
        print(f"INFO: _clear_extracted_files_dir: Cleaning files ending in {filter}...")
        bin_files_list = os.listdir(BK_CONSTANTS.EXTRACTED_FILES_DIR)
        for file_name in bin_files_list:
            if(file_name.endswith(filter)):
                os.remove(os.path.join(BK_CONSTANTS.EXTRACTED_FILES_DIR, file_name))
        print(f"INFO: _clear_extracted_files_dir: Cleaning complete!")