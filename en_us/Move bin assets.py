from sys import argv
from os import walk, path, remove, makedirs, path
from subprocess import run
from re import compile, sub, IGNORECASE, findall
from shutil import move

if len(argv) == 2:
    ignore = argv[0]
    first = argv[1]
else:
    print('Plz drag and drop a folder to the app!')

for_test = path.dirname(argv[0]) + '/ritobin/ritobin_cli.exe'
if not path.exists(for_test):
    print("Didn't found /ritobin/ritobin_cli.exe")
    input('')

will_move = input('It will move type "1" for yes, anything for no: ')
if will_move == '1':
    print('Rules for when moving:')
    print('*The search needs to starts without / and ends with a /')
    print('**Example: assets/characters/camille/skins/base/particles/')
    while True:
        search = input('What we will be searching here uwu?: ').lower().replace('\\', '/')
        if not search.endswith('/'):
            print('Plz add / in the end of the path! ')
        elif search.startswith('/'):
            print('Plz dont use / in the start of the path! ')
        elif not search.startswith('/') and search.endswith('/'):
            break
    
    print('*Same rules for replace, needs to start without / and ends with a /')
    print('**Example: assets/new_folder/particles/uwu/')
    while True:
        replace = input('We will be moving for which folder?: ').lower().replace('\\', '/')
        if not replace.endswith('/'):
            print('Plz add / in the end of the path! ')
        elif replace.startswith('/'):
            print('Plz dont use / in the start of the path! ')
        elif not replace.startswith('/') and replace.endswith('/'):
            break
else:
    search = input('What we will be searching here?: ').lower()
    replace = input('We will replace for what?: ').lower()

bins = compile('\.bin$', flags=IGNORECASE)
assets = compile(r'".+"')
found_files = []
new_files = []

for root, dirr, files in walk(first):
    for file in files:
        if file.lower().endswith('.bin'):
            fullpath = path.join(root, file)
            run(rf'ritobin/ritobin_cli.exe "{fullpath}"')
            remove(fullpath)
            newfile = sub(bins, '.py', fullpath)

            with open(newfile, 'r') as p:
                data = p.read()

            if will_move == '1':
                if not path.isdir(f'{first}/{sub("/$", "", replace)}'):
                    makedirs(f'{first}/{sub("/$", "", replace)}')

                with open(newfile, 'r') as p:
                    line = p.readline()
                    while line:
                        if search in line.lower():
                            try:
                                tempuw = findall(assets, line.lower())
                            
                                moving = tempuw[0]
                                moving = moving.replace('"', '/', 1).replace('"', '')
                                moving = first + moving
                                
                                if moving not in found_files:
                                    found_files.append(moving)
                                    
                                    new = sub(search, replace, moving.lower())
                                    new_files.append(new)
                                    

                            except Exception as e:
                                print(f'{e}')

                        line = p.readline()

            with open(newfile, 'w') as q:
                data = data.lower().replace(search, replace).replace('"prop"', '"PROP"')
                q.write(data)

            run(rf'ritobin/ritobin_cli.exe "{newfile}"')
            remove(newfile)

if will_move == '1':
    for index, _ in enumerate(found_files):
        try:
            move(found_files[index], new_files[index])
        except Exception as error:
            print(error)
