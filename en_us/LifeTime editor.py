import sys

if len(sys.argv) == 2:
    ignore = sys.argv[0]
    text_file = sys.argv[1]

while True:
    add_or_subtract = input("You want to add % [+], or subtract % [-]: ")
    if add_or_subtract == "+" or add_or_subtract == "-":
        break
    else:
        print(f"Lmao, plz use + or -\n")

print("\nYou don't need to use % in the percentage value, just use a full number")
print("Like: 10, 15, 20")

while True:
    percentage = input("Whats the value of the percentage? ")
    if percentage.isnumeric():
        percentage = int(percentage)
        print(f"Ok, the value is: '{percentage}%'")
        break
    else:
        print("Plz use a real number LOL\n")

with open(rf'{text_file}', 'r') as fileuwu:
    line = fileuwu.readline()
    try:
        with open(rf'{text_file}.new.txt', 'x+') as copyuwu:
            while line:
                if line == "                ParticleLifetime: embed = ValueFloat {\n":
                    copyuwu.write(line)
                    line = fileuwu.readline()
                    start = len('                    ConstantValue: f32 = ')
                    value = line[41:]
                    value = float(value)
                    copyuwu.write(f'                    ConstantValue: f32 = {value - (value * percentage/100)}\n'
                                  if add_or_subtract == "-"
                                  else f'                    ConstantValue: f32 = {value + (value * percentage/100)}\n'
                                  )
                    line = fileuwu.readline()

                else:
                    copyuwu.write(line)
                    line = fileuwu.readline()
    except Exception as e:
        print(e)
        print()
        print(f"The file: '{text_file}.new.txt' probably already exists")

print()
