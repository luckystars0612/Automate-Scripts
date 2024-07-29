import idaapi
import idc

start_address = 0x400000
end_address = 0x40b200
output_file = "dumped.bin"

with open(output_file, "wb") as fp:
    for ea in range(start_address, end_address):
        byte = idc.get_wide_byte(ea)
        fp.write(byte.to_bytes(1, 'little'))
