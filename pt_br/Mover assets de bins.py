from sys import argv
from os import walk, path, remove, makedirs
from subprocess import run
from re import compile, sub, IGNORECASE, findall
from shutil import move

if len(argv) == 2:
    ignore = argv[0]
    first = argv[1]
else:
    print('Porfavor arraste uma pasta para o .exe !')
    input('')
    
for_test = path.dirname(argv[0]) + '/ritobin/ritobin_cli.exe'
if not path.exists(for_test):
    print("Não foi encontrado o /ritobin/ritobin_cli.exe")
    input('')
 
will_move = input('Quer mover os arquivos? digite 1 para move-los: ')
if will_move == '1':
    print('*Digite o caminho da pasta principal até a pasta com texturas')
    print('**Exemplo: assets/characters/camille/skins/base/particles')
    search = input('O que estamos pesquisando? UwU: ').lower().replace('\\', '/')
    search = search.rstrip('/')
    search = search.lstrip('/')
    search = f'{search}/'
    
    print('*Agora o caminho da nova pasta das texturas')
    print('**Exemplo: assets/nova_pasta/particles/uwu')
    replace = input('Estamos movendo para qual pasta? UwU: ').lower().replace('\\', '/')
    replace = replace.rstrip('/')
    replace = replace.lstrip('/')
    replace = f'{replace}/'
    
else:
    search = input('O que estamos procurando?: ').lower()
    replace = input('E devemos substituir por?: ').lower()

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
