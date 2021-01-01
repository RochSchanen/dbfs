#!/usr/bin/python3
# file p.py
# created 20201221
# author Roch Schanen

# add virtual drive:
# define header format
# block access commands
# code implementation

# cache
# journaling
# user file access:
# directories, sets, tags, properties, etc...
# this is the file manager system
# encryption
# file access system: readonly, small, large, fast write, fast read, fixed size, etc...
# file access system determines physical managment of the data: the geography for the storage.
# 

# def getWordSizeEncoding():
#     # find word size in bits 
#     y, n = self.wordSize, 1
#     while y > 1:
#         n  += 1
#         y >>= 1
#     # get ceiling in power of two 
#     z, m = 1, 0
#     while z < n:
#         m  += 1
#         z <<= 1
#     # return binary string
#     return f'1{"1"*m}0{self.wordSize:0{2**m}b}'

__DEVSTEP__ = 3

# if __name__ == "__main__":
#   print("""
#   # file p.py
#   # created 20201221
#   # author Roch Schanen
#   """)

if __DEVSTEP__ == 3:

    print("--- DEVSTEP 3 ---")

    ws = 8       # word size
    ww = 1 << ws # word weight
    bs = 256     # block size
    
    # find block size in words 
    y, n = 1, 0
    while y <= bs:
        n  += 1
        y <<= ws

    print(f'block size      = {bs}')
    print(f'word size       = {ws}')
    print(f'word weight     = {1<<ws}')
    print(f'number of words = {n}')
    print(f'max value       = {(1<<ws)**n-1}')

    print(f'')

if __DEVSTEP__ == 2:

    print("--- DEVSTEP 2 ---")

    def wordSizeEncoding(ws):
        # find word size in bits 
        y, n = ws, 1
        while y > 1:
            n  += 1
            y >>= 1
        # get ceiling in power of two 
        z, m = 1, 0
        while z < n:
            m  += 1
            z <<= 1
        # return binary string
        return f'1{"1"*m}0{ws:0{2**m}b}'

    ws = 24
    print(f'{ws} => {wordSizeEncoding(ws)}')

if __DEVSTEP__ == 1:
    
    print("--- DEVSTEP 1 ---")

    x = 65536

    print(x)

    # find word size in bits 
    y, n = x, 1
    while y > 1:
        n  += 1  # increment bit width
        y >>= 1  # shift word 

    print(n)

    # get ceiling power of two 
    z, m = 1, 0
    while z < n:
        m  += 1  # increment bit width
        z <<= 1  # shift word 
    
    print(m)

    # build binary string
    s = f'1{"1"*m}0{x:0{2**m}b}'
    print(s)
