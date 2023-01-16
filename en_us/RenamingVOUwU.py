import os
import sys
import subprocess
import shutil
import re

if len(sys.argv) == 2:
    ignore = sys.argv[0]
    folder = sys.argv[1]

target = input('What is the target language that we are looking for? ').lower()
replace_by = input('We will replace it to which language? ').lower()

for root, direct, files in os.walk(folder):
    for file in files:
        if file.lower().endswith(f'{target}.wad.client'):
            try:
                full_path = os.path.join(root, file).lower()  # Full path for the file champion_target itself
                renamed = re.sub(f'{target}\.wad\.client$', f'{replace_by}.wad.client', full_path).lower() # The new full path
                os.rename(f'{full_path}', f'{renamed}')  # Renaming the wad
                # One step less since already renamed the main wad name
                subprocess.run(rf'wad-extract.exe "{renamed}"')  # Calling wad-extract

            except Exception as e:
                print(f'Error: {e}')


for root, direct, files in os.walk(folder):
    for file in files:
        if file.lower().endswith(f'{replace_by}.wad.client'):
            try:
                
                extracted_path = os.path.join(root, file).lower()
                
                new = re.sub(f'{replace_by}\.wad\.client$', f'{replace_by}.wad', extracted_path)
                
                # New_target is for searching the target folder inside the extracted wads
                new_target = rf'{new}\assets\sounds\wwise2016\vo\{target.lower()}'
                
                # The new folder that files will be moved
                new_replace = rf'{new}\assets\sounds\wwise2016\vo\{replace_by.lower()}'
                # Moving stuff uwu
                shutil.move(new_target, new_replace)
                
                # Now makes the wad >:D
                subprocess.run(rf'wad-make.exe "{new}"')
                
                # And deletes the folder that we did the wad right there
                shutil.rmtree(new)

            except Exception as e:
                print(f'Error: {e}')

input('')
