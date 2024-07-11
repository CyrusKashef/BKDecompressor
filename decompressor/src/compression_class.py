'''
Purpose:
* Class for running the compression and decompression algorithms on files
'''

###################
##### IMPORTS #####
###################

import zlib
import gzip
import shutil
import os

from decompressor.src.generic_bin_file_class import Generic_Bin_File_Class
from decompressor.src.bk_constants import BK_CONSTANTS

#############################
##### COMPRESSION CLASS #####
#############################

class COMPRESSION_CLASS(Generic_Bin_File_Class):
    '''
    Runs the compression and decompression algorithms on files.
    '''
    def __init__(self, asset_id_hex_str:str):
        '''
        Constructor
        '''
        self._asset_id_hex_str:str = asset_id_hex_str
        self._file_path:str = None
        self._file_content = None

    ###################
    ##### GENERIC #####
    ###################
    
    def _check_for_file(self, directory:str):
        '''
        Pass
        '''
        directory_files:list = os.listdir(directory)
        filtered_files:list = [file_name for file_name in directory_files if file_name.startswith(self._asset_id_hex_str)]
        list_length:int = len(filtered_files)
        file_name:str = None
        if(list_length == 1):
            file_name:str = filtered_files[0]
        elif(list_length > 1):
            print(f"ERROR: _check_for_file: {list_length} instances of file '{self._asset_id_hex_str}' were found.")
            exit(0)
        return file_name

    def _determine_file_path(self, check_directories:list=[BK_CONSTANTS.CUSTOM_FILES_DIR, BK_CONSTANTS.EXTRACTED_FILES_DIR]):
        '''
        Pass
        '''
        for directory in check_directories:
            file_name:str = self._check_for_file(directory)
            if(file_name):
                self._file_path:str = f"{directory}{file_name}"
                return
        print(f"ERROR: _determine_file_path: File '{self._asset_id_hex_str}' Not Found")
        exit(0)
    
    def get_file_path(self):
        '''
        Pass
        '''
        return self._file_path

    ######################
    ##### DECOMPRESS #####
    ######################
    
    def _decompress_file(self):
        '''
        Creates a decompressed version of a compressed file.
        '''
        try:
            compressor_obj = zlib.decompressobj(wbits=BK_CONSTANTS.WBITS)
            decompressed_file_bytes = compressor_obj.decompress(self._file_content[6:])
            decompressed_file_path:str = (self._file_path).replace(BK_CONSTANTS.COMPRESSED_BIN_EXTENSION, BK_CONSTANTS.DECOMPRESSED_BIN_EXTENSION)
            with open(decompressed_file_path, "wb+") as decompressed_file:
                decompressed_file.write(decompressed_file_bytes)
        except zlib.error as err:
            print(f"DEBUG: _decompress_file: File Path {self._file_path}")
            raise err
    
    ####################
    ##### COMPRESS #####
    ####################
    
    def _compress_asset_file(self, padding_byte:bytes, padding_interval:int):
        '''
        Compresses an asset file.
        Thank you Wedarobi! <3
        '''
        # Read Decompressed File
        # Align In-Game Post-Inflate Buffer To 16
        while(len(self._file_content) % 0x10):
            self._file_content.append(0x00)
        decompressed_file_length:int = len(self._file_content)
        # Deflate & Build
        compressed_body = gzip.compress(data=self._file_content, compresslevel=9, mtime=None)[10:-8]
        compressed_content = BK_CONSTANTS.BK_COMPRESSED_FILE_HEADER + decompressed_file_length.to_bytes(4, "big") + compressed_body
        # Align
        while(len(compressed_content) % padding_interval):
            compressed_content += padding_byte
        compressed_content_length:int = len(compressed_content)
        # Create Compressed File
        compressed_file_path:str = (self._file_path).replace(BK_CONSTANTS.CUSTOM_FILES_DIR, BK_CONSTANTS.EXTRACTED_FILES_DIR)
        compressed_file_path:str = (compressed_file_path).replace(BK_CONSTANTS.DECOMPRESSED_BIN_EXTENSION, BK_CONSTANTS.COMPRESSED_BIN_EXTENSION)
        with open(compressed_file_path, "wb+") as compressed_file:
            compressed_file.write(compressed_content)
        return compressed_file_path, compressed_content_length

    def _copy_raw_to_compressed(self):
        '''
        Copies a decompressed file to another file with the compressed extension.
        '''
        compressed_content_length:int = len(self._file_content)
        compressed_file_path:str = (self._file_path).replace(BK_CONSTANTS.CUSTOM_FILES_DIR, BK_CONSTANTS.EXTRACTED_FILES_DIR)
        compressed_file_path:str = (compressed_file_path).replace(BK_CONSTANTS.RAW_BIN_EXTENSION, BK_CONSTANTS.COMPRESSED_BIN_EXTENSION)
        shutil.copy(self._file_path, compressed_file_path)
        return compressed_file_path, compressed_content_length

    ##########################
    ##### MAIN FUNCTIONS #####
    ##########################

    def decompress_file_main(self):
        '''
        Runs the main workflow for prepping a file for modifying.
        The file may be decompressed or copied as raw.
        '''
        self._determine_file_path(check_directories=[BK_CONSTANTS.EXTRACTED_FILES_DIR])
        self._read_file()
        self._decompress_file()

    def compress_asset_file_main(self):
        '''
        Runs the main workflow for prepping a file for insersion.
        The file may be compressed or copied as raw.
        '''
        self._determine_file_path(check_directories=[BK_CONSTANTS.CUSTOM_FILES_DIR, BK_CONSTANTS.EXTRACTED_FILES_DIR])
        self._read_file()
        if(BK_CONSTANTS.DECOMPRESSED_BIN_EXTENSION in self._file_path):
            compressed_file_path, compressed_content_length = self._compress_asset_file(b"\xAA", 0x08)
        elif(BK_CONSTANTS.RAW_BIN_EXTENSION in self._file_path):
            compressed_file_path, compressed_content_length = self._copy_raw_to_compressed()
        else:
            raise Exception(f"Error: compress_file_main: Unidentified file type '{self._file_type}'")
        return compressed_file_path, compressed_content_length
    
    def compress_assembly_file(self):
        '''
        Compresses an assembly file.
        Thank you Wedarobi! <3
        '''
        self._determine_file_path(check_directories=[BK_CONSTANTS.CUSTOM_FILES_DIR, BK_CONSTANTS.EXTRACTED_FILES_DIR])
        self._read_file()
        while(len(self._file_content) % 0x10):
            self._file_content.append(0x00)
        decompressed_file_length:int = len(self._file_content)
        # Deflate & Build
        compressed_body = gzip.compress(data=self._file_content, compresslevel=9, mtime=None)[10:-8]
        compressed_content = BK_CONSTANTS.BK_COMPRESSED_FILE_HEADER + decompressed_file_length.to_bytes(4, "big") + compressed_body
        # Create Compressed File
        compressed_file_path:str = (self._file_path).replace(BK_CONSTANTS.CUSTOM_FILES_DIR, BK_CONSTANTS.EXTRACTED_FILES_DIR)
        compressed_file_path:str = (compressed_file_path).replace(BK_CONSTANTS.DECOMPRESSED_BIN_EXTENSION, BK_CONSTANTS.COMPRESSED_BIN_EXTENSION)
        with open(compressed_file_path, "wb+") as compressed_file:
            compressed_file.write(compressed_content)
        return compressed_file_path