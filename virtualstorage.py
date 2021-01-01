#!/usr/bin/python3
# file virtualstorage.py
# created 20201221
# author Roch Schanen

from sys import exit

import numpy as np

# 20201221 add virtual storage class

__DEBUG__ = True
# __DEBUG__ = False

class virtualstorage():

    fileHandle  = None
    filePath    = None
    wordSize    = None # word size in bits
    blockSize   = None # block size in words
    deviceSize  = None # device size in blocks

    # writing delay, reading delay, security, ...
 
    def __init__(self):
        if __DEBUG__: print('__init__')
        return

    def setWordSize(self, value):
        if self.fileHandle:
            print('setWordSize error')
            print(' -> device locked')
            exit()
        if __DEBUG__: print(f'setWordSize {value}')
        self.wordSize = value
        return

    def getWordSize(self):
        return self.wordSize

    def setBlockSize(self, value):
        if self.fileHandle:
            print('setBlockSize error:')
            print(' -> device locked')
            exit()
        if __DEBUG__: print(f'setBlockSize {value}')
        self.blockSize = value
        return

    def getBlockSize(self):
        return self.block

    def setDeviceSize(self, value):
        if self.fileHandle:
            print('setDeviceSize error:')
            print(' -> device locked')
            exit()
        if __DEBUG__: print(f'setDeviceSize {value}')
        self.deviceSize = value
        return      

    def getDeviceSize(self):
        return self.deviceSize

    def setFilePath(self, value):
        if self.fileHandle:
            print('setFilePath error:')
            print(' -> device locked')
            exit()
        if __DEBUG__: print(f'setFilePath {value}')
        self.filePath = value
        return

    def getFilePath(self):
        return self.filePath

    def createDevice(self):
        if self.fileHandle:
            print('createDevice error:')
            print(' -> device already opened')
            print(' -> no operation')
            return
        # reset error flag
        error = False
        # check file path
        messg = 'createDevice() error'
        if not self.filePath:
            if not error: print(messg)
            print(' -> filePath undefined')
            error = True
        # check word size
        if not self.wordSize:
            if not error: print(messg)
            print(' -> wordSize undefined')
            error = True
        # check block size
        if not self.blockSize:
            if not error: print(messg)
            print(' -> blockSize undefined')
            error = True
        # check device size
        if not self.deviceSize:
            if not error: print(messg)
            print(' -> deviceSize undefined')
            error = True
        # exit on error        
        if error: exit()
        # compute file size in bits
        bitFileSize  = self.wordSize * self.blockSize * self.deviceSize
        # compute file size in bytes
        byteFileSize = bitFileSize >> 3
        # ceil completion
        if bitFileSize & 7: byteFileSize += 1  
        # create binary file to hold the data
        self.fileHandle = open(self.filePath, "wb")
        # set the file size
        self.fileHandle.seek(byteFileSize - 1)
        self.fileHandle.write(b"\x00")
        #done
        return

    def closeDevice(self):
        # flush data
        # ...        
        # close
        self.fileHandle.close()
        # unlock handle
        self.fileHandle = None
        # done
        return

    # blockAddress    = None      # current block address: pointer to a block
    # blockData       = None      # cache data stored at the current block address

    # def setAddress(self, a):
    #     # check boundaries
    #     if a > self.deviceSize:
    #         print('setAddress error:')
    #         print(' -> address exceeds device size')
    #         print(' -> no operation')
    #         return
    #     # flush data
    #     # ...        
    #     # set address
    #     self.blockAddress = a

    #     #done
    #     return        

if __name__ == "__main__":
    print("""
    # file virtualstorage.py
    # created 20201221
    # author Roch Schanen
    """)

    vs = virtualstorage()

    vs.setFilePath('./VS1MB')   # define a 1MB storage as an example
    vs.setWordSize(8)           # 8 bits
    vs.setBlockSize(256)        # 256 words
    vs.setDeviceSize(4096)      # 4096 blocks
    vs.createDevice()           # create the new storage
    vs.closeDevice()            # close storage
