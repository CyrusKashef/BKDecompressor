'''
Purpose:
* Removes the previous package for the BK Decompressor
* Creates the package for the BK Decompressor
'''

import shutil
import subprocess
import os

### UNINSTALL BY DELETING FOLDER ###

package_dir = "C:/Users/Cyrus/AppData/Local/Programs/Python/Python311/Lib/site-packages/"
package_name:str = "BKDecompressor-0.0.1-py3.11.egg"
bk_rando_egg_info_dir = "BKDecompressor.egg-info"
build_dir = "build"
dist_dir = "dist"

try:
    shutil.rmtree(package_dir + package_name)
    shutil.rmtree(bk_rando_egg_info_dir)
    shutil.rmtree(build_dir)
    shutil.rmtree(dist_dir)
except FileNotFoundError:
    print("Folder Already Deleted/Doesn't Exist")
else:
    print("Folder Deleted")

def remove_pycache_folders(curr_dir:str):
    if(os.path.isdir(curr_dir)):
        if(curr_dir.endswith("__pycache__")):
            print(f"Removing PyCache Dir: {curr_dir}")
            shutil.rmtree(curr_dir)
            return
        folder_list:list = os.listdir(curr_dir)
        for item in folder_list:
            remove_pycache_folders(f"{curr_dir}/{item}")

remove_pycache_folders("decompressor")

### INSTALL USING SETUP.PY SCRIPT ###

setup_file_dir:str = "C:/Users/Cyrus/Documents/VS_Code/BKDecompressor/BKDecompressor/"
setup_file_name:str = "setup.py"

subprocess.Popen(f"python {setup_file_dir}{setup_file_name} install",
                 universal_newlines=True, shell=True).communicate()