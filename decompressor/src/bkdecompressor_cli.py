###################
##### IMPORTS #####
###################

import os
import json
import argparse

from decompressor.src.bk_constants import BK_CONSTANTS
from decompressor.src.modification_process import MODIFICATION_PROCESS_CLASS

####################
##### WORKFLOW #####
####################

### Default Action Option
default_option = "extract"
if(os.path.exists(BK_CONSTANTS.EXTRACTED_FILES_DIR)):
    default_option = "compile"

### Read Config File
with open(BK_CONSTANTS.CONFIG_FILE_PATH) as json_file:
    config_data:dict = json.load(json_file)
original_rom_path:str = config_data["ORIGINAL_ROM_PATH"]
new_rom_path:str = config_data["NEW_ROM_PATH"]
if(not os.path.isfile(original_rom_path)):
    error_message:str = \
        "ERROR: Original ROM Path listed in config.json does not exist.\n" + \
        "  - Option 1: The ROM Path simply does not exist.\n" + \
        "  - Option 2: The ROM Path is still an empty string.\n" + \
        "  - Option 3: The ROM Path is relative and you're not running this in the right folder.\n" + \
        "  - Option 4: Open a ticket with a developer."
    print(error_message)
    exit(0)

### Arg Parser
parser = argparse.ArgumentParser(
    prog="BK Decompressor",
    description="What the program does",
    epilog="Text at the bottom of help",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    "-a",
    "--action",
    choices=["extract", "compile"],
    default="compile",
    help=("extract:\n" + \
          "  * Takes all files out of the ROM.\n" + \
          "  * Files that were compressed will be decompressed and will end in '-Decompressed.bin'.\n" + \
          "  * Files that were decompressed by default will end in '-Raw.bin'.\n\n" + \
          "compile:\n" + \
          "  * For every file extracted, checks if there's a replacement in 'custom_files'.\n" + \
          "  * All assets get appended to the back of the ROM.\n" + \
          "  * All assembly files get inserted back to their original location.")
    )

### Main
args = parser.parse_args()
modification_process_obj = MODIFICATION_PROCESS_CLASS()
if(args.action == "extract"):
    modification_process_obj._extract_decompress_files(args.originalromfile)
elif(args.action == "compile"):
    new_rom_file:str = args.newromfile
    if(args.newromfile == ""):
        new_rom_file:str = (args.originalromfile).replace(".z64", "-NEW.z64")
    modification_process_obj._insert_compress_files(args.originalromfile, new_rom_file)