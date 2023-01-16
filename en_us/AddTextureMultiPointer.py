#  ✓ParticleUvScrollRateMult -> 0x22c3cf3e
#  ✓Include UvScrollClampMult: flag = true inside the pointer
#  ✓ParticleUvRotateRateMult -> 0xdd36a38c

import sys

fucked_line = "                TextureMult: string ="
bracket = "{"
if len(sys.argv) == 2:
    first = sys.argv[0]
    folder = sys.argv[1]

uv_scroll_multi = False
new = f"{folder.replace('.py', '.new.py')}"

with open(rf"{folder}", "r") as file:
    with open(rf"{new}", "x+") as copy:
        line = file.readline()
        while line:
            if "                UvScrollClampMult: flag = true" == line.strip("\n"):
                line = file.readline()
                uv_scroll_multi = True

            if fucked_line in line.strip("\n"):
                copy.write(f"                TextureMult: pointer = 0xb097c1bd {bracket}\n    {line}")
                line = file.readline()
                while True:
                    if "            }" == line.strip("\n"):
                        copy.write("                }\n            }\n")
                        line = file.readline()
                        break
                    else:
                        if uv_scroll_multi:
                            copy.write("                    UvScrollClampMult: flag = true\n")
                            uv_scroll_multi = False
                        copy.write(f"    {line.replace('ParticleUvScrollRateMult', '0x22c3cf3e').replace('ParticleUvRotateRateMult', '0xdd36a38c')}")
                        line = file.readline()

            else:
                copy.write(f"{line}")
                line = file.readline()

