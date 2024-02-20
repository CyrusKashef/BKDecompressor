'''
Purpose:
* Class of constants used in this program
* Makes it easier to find and import constant values without typos
'''

class BK_CONSTANTS:
    ASSET_TABLE_START_INDEX:int = 0x5E98
    ASSET_TABLE_END_INDEX:int = 0x10CC8
    ASSET_TABLE_OFFSET:int = 0x10CD0
    ASSET_TABLE_INTERVAL:int = 0x8
    ASSET_TABLE_START_ID:int = 0x0000
    ASSET_TABLE_END_ID:int = 0x15C6
    ROM_END_INDEX:int = 0x1000000
    CIC:int = 0xA3886759
    CRC1_INDEX_START:int = 0x10
    CRC2_INDEX_START:int = 0x14
    CHECK_ROM_START_INDEX:int = 0x1000
    CHECK_ROM_END_INDEX:int = 0x101000
    WBITS:int = -15
    BK_COMPRESSED_FILE_HEADER:bytes = b"\x11\x72"
    CUSTOM_FILES_DIR:str = "decompressor/custom_files/"
    EXTRACTED_FILES_DIR:str = "decompressor/extracted_files/"
    CONFIG_FILE_PATH:str = "decompressor/src/config.json"
    BIN_EXTENSION:str = ".bin"
    COMPRESSED_BIN_EXTENSION:str = f"-Compressed.bin"
    DECOMPRESSED_BIN_EXTENSION:str = f"-Decompressed.bin"
    RAW_BIN_EXTENSION:str = f"-Raw.bin"
    DECOMPRESSED_STR:str = "Decompressed"
    COMPRESSED_STR:str = "Compressed"
    RAW_STR:str = "Raw"
    ASSET_FILE:str = "Asset"
    ASSEMBLY_FILE:str = "Assembly"
    PADDING_BYTE:str = "Padding Byte"
    PADDING_INTERVAL:str = "Padding Interval"
    PADDING_DICT:dict = {
        ASSET_FILE: {
            PADDING_BYTE: b"\xAA",
            PADDING_INTERVAL: 0x08,
        },
        ASSEMBLY_FILE: {
            PADDING_BYTE: b"\x00",
            PADDING_INTERVAL: 0x10,
        },
    }
    START_UPPER_STR:str = "Start Upper"
    LOWER_OFFSET_STR:str = "Lower Offset"
    END_OFFSET:int = 0x4
    ASSEMBLY_POINTER_DICT:dict = {
        "C Libraries": {
            START_UPPER_STR:  0x107A,
            LOWER_OFFSET_STR: 0x8,
        },
        "Game Engine": {
            START_UPPER_STR:  0x27FA,
            LOWER_OFFSET_STR: 0x28,
        },
        "Spiral Mountain": {
            START_UPPER_STR:  0x28F2,
            LOWER_OFFSET_STR: 0x28,
        },
        "Mumbo's Mountain": {
            START_UPPER_STR:  0x287A,
            LOWER_OFFSET_STR: 0x28,
        },
        "Treasure Trove Cove": {
            START_UPPER_STR:  0x2872,
            LOWER_OFFSET_STR: 0x28,
        },
        "Clanker's Cavern": {
            START_UPPER_STR:  0x280A,
            LOWER_OFFSET_STR: 0x28,
        },
        "Bubblegloop Swamp": {
            START_UPPER_STR:  0x2882,
            LOWER_OFFSET_STR: 0x28,
        },
        "Freezeezy Peak": {
            START_UPPER_STR:  0x2892,
            LOWER_OFFSET_STR: 0x28,
        },
        "Gobi's Valley": {
            START_UPPER_STR:  0x281A,
            LOWER_OFFSET_STR: 0x28,
        },
        "Mad Monster Mansion": {
            START_UPPER_STR:  0x2812,
            LOWER_OFFSET_STR: 0x28,
        },
        "Rusty Bucket Bay": {
            START_UPPER_STR:  0x288A,
            LOWER_OFFSET_STR: 0x28,
        },
        "Click Clock Wood": {
            START_UPPER_STR:  0x28EA,
            LOWER_OFFSET_STR: 0x28,
        },
        "Gruntilda's Lair": {
            START_UPPER_STR:  0x2902,
            LOWER_OFFSET_STR: 0x28,
        },
        "Cutscenes": {
            START_UPPER_STR:  0x28FA,
            LOWER_OFFSET_STR: 0x28,
        },
        "Final Battle": {
            START_UPPER_STR:  0x290A,
            LOWER_OFFSET_STR: 0x28,
        },
        "Unused Level": {
            START_UPPER_STR: 0x2802,
            LOWER_OFFSET_STR: 0x28,
        }
    }
    ASM_START_ADDRESS:int = 0xF19250
    ASM_END_ADDRESS:int = 0xFDAA30
    ### GRUNTILDA'S LAIR
    NOTE_DOOR_COST_START_INDEX:int = 0x7CC
    NOTE_DOOR_COST_END_INDEX:int = 0x7E4
    NOTE_DOOR_COST_INTERVAL:int = 0x2
    JIGSAW_PUZZLE_COST_START_INDEX:int = 0x1B48
    JIGSAW_PUZZLE_COST_END_INDEX:int = 0x1B74
    JIGSAW_PUZZLE_COST_INTERVAL:int = 0x4
    JIGSAW_PUZZLE_STARTING_BIT_OFFSET:int = 0x5D
    JIGSAW_PUZZLE_ALLOTED_BIT_COUNT:int = 0x25
    DEFAULT_NOTE_DOOR_LIST:list = [
        50, 180, 260, 350, 450, 640,
        765, 810, 828, 846, 864, 882]
    DEFAULT_JIGGY_PUZZLE_LIST:list = [
        1, 2, 5, 7, 8, 9,
        10, 12, 15, 25, 4]
    ### GENERIC
    TERMITE:str = "TERMITE"
    CROCODILE:str = "CROCODILE"
    WALRUS:str = "WALRUS"
    PUMPKIN:str = "PUMPKIN"
    BEE:str = "BEE"
    DEFAULT_TRANSFORMATION_COST_LIST:list = [
        5, 10, 15, 20, 25
    ]