import shutil
import subprocess

### UNINSTALL BY DELETING FOLDER ###

package_dir:str = "C:/Users/Cyrus/AppData/Local/Programs/Python/Python311/Lib/site-packages/"
package_name:str = "BKDecompressor-0.0.1-py3.11.egg"

try:
    shutil.rmtree(package_dir + package_name)
except FileNotFoundError:
    print("Folder Already Deleted/Doesn't Exist")
else:
    print("Folder Deleted")

### INSTALL USING SETUP.PY SCRIPT ###

setup_file_dir:str = "C:/Users/Cyrus/Documents/VS_Code/BKDecompressor/BKDecompressor/"
setup_file_name:str = "setup.py"

subprocess.Popen(f"python {setup_file_dir}{setup_file_name} install",
                 universal_newlines=True, shell=True).communicate()