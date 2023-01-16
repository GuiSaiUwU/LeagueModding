import sys
# TODO: Make a proprely bone reader lol reading from bytes are probably bad :L
if len(sys.argv) == 2:
    ignoraoexe = sys.argv[0]
    osso = sys.argv[1]


lista = []
boneid = 1
bracket = '{'
make_list = input('Want to write a list with BoneIDs and names? [yes] ').lower()

with open(rf'{osso}', 'rb') as file:
    bytesuwu = file.readlines()
    bytesuwu = bytesuwu[-1]
    bytesuwu = str(bytesuwu).split(r'\x00')
    for i in bytesuwu:
        if len(i) == 1 or i == '' or i == "b'":
            pass
        else:
            for letra in i:
                if letra == '\\':
                    i = 0
            if i == 0:
                pass
            else:
                print(f'{boneid}: {i}')
                if make_list == 'yes' or make_list == 'y':
                    with open(rf'{osso.replace(".skl", "_list.txt")}', 'a+') as txtuwu:
                        txtuwu.write(f'BoneID: {boneid}, {i}\n')
                boneid += 1

print(f'\nNumber of total bones = {boneid-1}')

make_mask = input('Do you wanna make a mask? [yes] ').lower()
if make_mask == 'yes' or make_mask == 'y':
    boneid = 1
    mask_name = input('What will be your mask name? ')
    print(f'\nYou can use "," to separate more than one Bone name or ID.')
    print(f'Do not use spacebar or the ID // Name will be ignored.')
    print('Example of how to write:\nL_Hand,R_Hand,132')
    bones_with_mask = input("Type the Bones IDs or Bone Names for the mask:\n").lower()
    bones_with_mask = bones_with_mask.split(",")
    print('\nDo not use a mask value bigger than 1')
    print("Mask value needs to be bigger than 0 and smaller or equal than 1\n")
    while True:
        mask_value = input("Which is the value of the mask? ")
        try:
            mask_value = float(mask_value)
            if 0 >= mask_value:
                print("Mask value can't be zero! ")

            elif mask_value == 1:
                break
            if mask_value != 0 and mask_value > 0:
                break
        except Exception as error:
            error = error

    with open(rf'{osso}', 'rb') as file:
        with open(rf'{osso.replace(".skl", "_mask.txt")}', 'x+') as maskuwu:
            bytesuwu = file.readlines()
            bytesuwu = bytesuwu[-1]
            bytesuwu = str(bytesuwu).split(r'\x00')
            maskuwu.write("Writing Mask:\n\n")
            maskuwu.write("        mMaskDataMap: map[hash,embed] = {\n")
            maskuwu.write(f'            "{mask_name}" = MaskData {bracket}\n')
            maskuwu.write('                mWeightList: list[f32] = {\n')

            for i in bytesuwu:
                if len(i) == 1 or i == '' or i == "b'":
                    pass
                else:
                    for letra in i:
                        if letra == '\\':
                            i = 0
                    if i == 0:
                        pass
                    else:
                        if str(boneid) in bones_with_mask or i.lower() in bones_with_mask:
                            maskuwu.write(f"                    {mask_value}\n")
                            boneid += 1
                        else:
                            maskuwu.write("                    0\n")
                            boneid += 1

            maskuwu.write("                }\n            }")

input('Press enter to close. ')
