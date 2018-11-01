# Michael Giardina
# CS 472 Project 1 MIPS Disassembler
# This program takes an array of 32bit hex machine codes
#     and interprets them through a series of operations
#     to output the original source instructions


# a list to hold the 32 bit machine codes
hexcodeList = [0x022da822, 0x8ef30018, 0x12a70004, 0x02689820, 0xad930018, 0x02697824, 0xad8ffff4, 0x018c6020, 0x02a4a825, 0x158ffff6, 0x8e59fff0]

# This dictionary of the possible hex func values
#   maps to corresponding MIPS instructions
funcCodeDict = {0x04:"beq", 0x05:"bne", 0x20:"add", 0x22:"sub", 0x23:"lw", 0x24:"and", 0x25:"or", 0x2a:"slt", 0x2b:"sw"}

# Hex value corresponds to bits 26-31 on
ophexmask = 0xfc000000
# Hex value corresponds to bits 0-5 on
funchexmask = 0x0000003f
# Hex value corresponds to bits 21-25 on
rshexmask = 0x03e00000
# Hex value corresponds to bits 16-20 on
rthexmask = 0x001f0000
# Hex value corresponds to bits 11-15 on
rdhexmask = 0x0000f800
# Hex value corresponds to bits 0-15 on
addresshexmask = 0x0000ffff
# variable stores beginning he address
pc = 0x7A060

# function for sign extension of I format offset value
# this will take care of handling negative values correctly
#  FOR FULL DISCLOSURE : found how to implement this function
#  on Stack Overflow via user Patrick Maupin
def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

# Loop to iterate through values of list and run operations on the codes
for code in hexcodeList:

    pc += 4 # increment counter
    opcode = code & ophexmask # bitwise and of code to find out which format
    shiftedopcode = opcode >>26 # bitwise shift to get number to LSB position
    print "hexcode %08x to assembly is:" %(code) # Simple print for readability of output
    # Check for R format(value 0) if so break down the code according to OPCODE, RS, RT, RD, FUNC format
    if shiftedopcode == 0:
        rscode = (code & rshexmask) >> 21 # bitwise and/shift number of bits to get rs field

        rtcode = (code & rthexmask) >> 16 # bitwise and/shift number of bits to get rt field

        rdcode = (code & rdhexmask) >> 11 # bitwise and/shift numebr of bits to get rd field

        func = code & funchexmask # bitwise and, no shift needed as these are already bits 0-5

        #prints out disassembled code with address and R Format instruction
        print "%05x %s $%d $%d $%d\n" % (pc-4 , funcCodeDict[func], rdcode, rscode, rtcode)
    #  checks for values corresponding to I Format
    if shiftedopcode == 1 or (shiftedopcode >= 4 and shiftedopcode <=62):
        # mask and shift to get rs register value
        rscode = (code & rshexmask) >> 21
        # mask and shift to get rt value
        rtcode = (code & rthexmask) >> 16
        # sign extended mask and shift for the offset (deals with negative values for proper evaluation)
        iAddress = sign_extend((code & addresshexmask),16)
        # stores calculated address for shifts/loads
        branchAddress= pc+iAddress*4
        # printing format for output of shifts and loads
        if shiftedopcode == 35 or shiftedopcode == 43:
            print "%05x %s $%d, %d ($%d)\n" %(pc-4, funcCodeDict[shiftedopcode], rtcode, iAddress, rscode)
        else:
            # printing format for other I format instructions
            print "%05x %s $%d, $%d, address %08x\n" %(pc-4, funcCodeDict[shiftedopcode], rtcode, rscode, branchAddress)
