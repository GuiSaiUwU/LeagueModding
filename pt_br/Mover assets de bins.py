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
    print('Regras para quando for mover arquivos:')
    print('*A Pesquisa precisa terminar com / no final.')
    print('*A Pesquisa precisa começar sem nenhuma / no inicio!!')
    print('**Exemplo: assets/characters/camille/skins/base/particles/')
    while True:
        search = input('O que estamos pesquisando? UwU: ').lower().replace('\\', '/')
        if not search.endswith('/'):
            print('Pfv adicione / no final do caminho de pesquisa! ')
        elif search.startswith('/'):
            print('Pfv não coloque / no inicio do caminho! ')
        elif not search.startswith('/') and search.endswith('/'):
            break

    print('*Mesmas regras, precisa começar sem / e terminar com /')
    print('**Exemplo: assets/nova_pasta/particles/uwu/')
    while True:
        replace = input('Estamos movendo para qual pasta? UwU: ').lower().replace('\\', '/')
        if not replace.endswith('/'):
            print('Pfv adicione / no final do caminho da nova pasta! ')
        elif replace.startswith('/'):
            print('Pfv não coloque / no inicio do caminho! ')
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
