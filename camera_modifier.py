import mmap
import json
import struct
import binascii
import subprocess
import os
import glob

def float_to_valid_hex(f):
    hex_convert = hex(struct.unpack('<I', struct.pack('<f', f))[0])
    valid_hex = ''
    hex_convert = hex_convert[2:][::-1]
    for x in range(0, len(hex_convert)):
        valid_swap = x + 1
        if valid_swap % 2 == 0:
            chars = hex_convert[x-1:valid_swap]
            valid_hex += chars[::-1]
    return valid_hex

def parse_ue(file_names):
    for x in file_names:
        subprocess.run(['./john-wick-parse.exe', 'serialize', './' + directory_val + '/' + x])


directory_val = input("Enter directory to process: ")
print(directory_val)
list_of_uexp = glob.glob("./" + directory_val + "/*.uexp")
list_of_uasset = glob.glob("./" + directory_val + "/*.uasset")
if len(list_of_uasset) != len(list_of_uexp):
    print("size mismatch, is everything here?")
file_names = []
for name in list_of_uexp:
    file_names.append(os.path.basename(name).replace('.uexp', ''))

# john wick parse
parse_ue(file_names)

# open json and process

for file_to_parse in file_names:
    with open('./' + directory_val + '/' + file_to_parse + '.json') as x:
        y = json.load(x)
        hex_values = []
        values_to_convert = []
        anim_length = y[0]['AnimLength']
        print('Found anim length of', anim_length)
        bounding_box = y[0]['BoundingBox']
        if anim_length != 0.0:
            values_to_convert.append(anim_length)
        for axis in bounding_box:
            if isinstance(bounding_box[axis], dict):
                values_to_convert.extend(list(bounding_box[axis].values()))
        values_to_convert = list(filter((0.0).__ne__, values_to_convert))
        print('Found values of', values_to_convert)

        for x in values_to_convert:
            hex_values.append(float_to_valid_hex(x))

        with open('./' + directory_val + '/' + file_to_parse  + '.uexp', 'rb') as f:
            content = f.read().hex()
            f.close()
            for x in hex_values:
                content = content.replace(x, '00000000', 1)
            unhexify = binascii.unhexlify(content)
            g = open('./' + directory_val + '/' + file_to_parse  + '.uexp', "wb")
            g.write(bytes(unhexify))
            g.close()

parse_ue(file_names)
for file_to_parse in file_names:
    with open('./' + directory_val + '/' + file_to_parse + '.json') as x:
        y = json.load(x)
        value_check = []
        anim_length = y[0]['AnimLength']
        value_check.append(anim_length)
        bounding_box = y[0]['BoundingBox']
        for axis in bounding_box:
            if isinstance(bounding_box[axis], dict):
                value_check.extend(list(bounding_box[axis].values()))
    print('Processed with values', value_check)
print('Finished')