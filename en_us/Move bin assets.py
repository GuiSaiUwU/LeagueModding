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
    input('')

for_test = path.dirname(argv[0]) + '/ritobin/ritobin_cli.exe'
if not path.exists(for_test):
    print("Didn't found /ritobin/ritobin_cli.exe")
    input('')

will_move = input('It will move type "1" for yes, anything for no: ')
if will_move == '1':
    print('')
    print('*Example: assets/characters/camille/skins/base/particles/')
    search = input('What we will be searching here uwu?: ').lower().replace('\\', '/')
    search = search.rstrip('/')
    search = search.lstrip('/')
    search = f'{search}/'
    
    print('')
    print('*So, now its the folder that the particles will be moved')
    print('**Example: assets/new_folder/particles/uwu')
    replace = input('We will be moving for which folder?: ').lower().replace('\\', '/')
    replace = replace.rstrip('/')
    replace = replace.lstrip('/')
    replace = f'{replace}/'
    
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
            run([for_test, fullpath])
            remove(fullpath)
            newfile = sub(bins, '.py', fullpath)

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

            with open(newfile, 'r') as q:
                data = q.readlines()

            with open(newfile, 'w') as fileuwu:
                for line in data:
                    if search in line.lower():
                        temp = findall(search, line, IGNORECASE)
                        newline = line.replace(temp[0], replace)
                        fileuwu.write(newline)
                    else:
                        fileuwu.write(line)

            run([for_test, newfile])
            remove(newfile)

if will_move == '1':
    for index, _ in enumerate(found_files):
        try:
            move(found_files[index], new_files[index])
        except Exception as error:
            print(error)
