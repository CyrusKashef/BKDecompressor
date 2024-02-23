## Prerequisites

* Python Version 3.11
* pip

## Setup

In a terminal from the BKDecompressor folder, run the following:

> python -m pip install -r requirements.txt

> python setup.py install

## Configuration

Adjust the file located at .\decompressor\src\config.json
  - ORIGINAL_ROM_PATH: Where is your Banjo-Kazooie ROM?
    - Relative Path Examples:
      - Root Folder: Banjo-Kazooie.z64
      - Decompressor Folder: .\decompressor\Banjo-Kazooie.z64
    - Absolute Path Example:
      - C:\Users\Cyrus\Documents\VS_Code\BKDecompressor\BKDecompressor\Banjo-Kazooie.z64
  - NEW_ROM_PATH: Where do you want your new ROM to save to?
    - Same formatting as ORIGINAL_ROM_PATH
    - If left blank, will use ORIGINAL_ROM_PATH, but replace the end with '-NEW'
  - DISABLE_ANTI_TAMPERING: Are you modifying any assembly/using a below feature?
  - PATCH_YUM_YUM_CRASH_FIX: Fixes a crash when Yum-Yums touch a non-egg/red feather
  - BOOT_TO_FILE_SELECT: Boots the game to the file select instead of the N64 Logo
  - SKIP_JIGGY_JIG: When collecting a jiggy, the player will not be forced to do the Jiggy Jig
  - ENABLE_FALLPROOF: When falling from large heights, the player will not take damage
  - ENABLE_EXIT_TO_WITCHS_LAIR: Feature in pause menu to quickly leave a level
  - START_GAME_WITH_ALL_MOVES: New file starts the player with all the moves
  - WORLD_PUZZLE_COSTS: Adjusts how many jiggies are required to open a level
  - NOTE_DOOR_COSTS: Adjusts how many notes are required to open a note door
  - TRANSFORMATION_COSTS: Adjusts how many tokens are required to transform

## Modification Process Run

\path\to\python3.exe \path\to\decompressor\src\modification_process.py

example:
> C:\Users\USERNAME\AppData\Local\Programs\Python\Python311\python.exe .\decompressor\src\modification_process.py

## Command Line Run

\path\to\python3.exe \path\to\decompressor\src\bkdecompressor_cli.py

example:
> C:\Users\USERNAME\AppData\Local\Programs\Python\Python311\python.exe .\decompressor\src\bkdecompressor_cli.py

-a, --actions (Optional)
By default, actions checks if extracted_files directory exists. If it does not exist, run extract. If it does, run compile.
  - extract
    - Takes all files out of the ROM
    - Files that were compressed will be decompressed and will end in '-Decompressed.bin'
    - Files that were decompressed by default will end in '-Raw.bin'
  - compile
    - For every file extracted, checks if there's a replacement in 'custom_files'
    - Replacement files must have exact same naming as original file
    - All assets get appended to the back of the ROM
    - All assembly files get inserted back to their original location
