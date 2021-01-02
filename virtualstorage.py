#!/usr/bin/python3
# file virtualstorage.py
# created 20201221
# author Roch Schanen

from sys import exit

import numpy as np

# 20201221 add virtual storage class
# 20210101 create storage file

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
        # make header
        self.header  = self.wordSize.to_bytes(4, 'little')
        self.header += self.blockSize.to_bytes(4, 'little')
        self.header += self.deviceSize.to_bytes(4, 'little')
        # compute file size in bits
        bitFileSize  = self.wordSize * self.blockSize * self.deviceSize + 3*4*8
        # compute file size in bytes
        byteFileSize = bitFileSize >> 3
        # 8bits alignment
        if bitFileSize & 7: byteFileSize += 1  
        # create binary file to hold the data
        self.fileHandle = open(self.filePath, "wb+")
        # write header
        self.fileHandle.write(self.header)
        # point to the end-of-file
        self.fileHandle.seek(byteFileSize - 1)
        # write an arbitrary byte to fix the file size
        self.fileHandle.write(b"\x00")
        #done
        return

    def closeDevice(self):
        if not self.fileHandle:
            print('closeDevice error:')
            print(' -> no device')
            print(' -> no operation')
            return
        # flush data
        # ...        
        # close
        self.fileHandle.close()
        # unlock handle
        self.fileHandle = None
        # done
        return

    blockAddress  = None  # current block address: pointer to a block
    blockData     = None  # cache data stored at the current block address

    def getCache(self, ba):
        """ return a reference to a cache block (ndarray of uint8) 
        ba is the block address value (uint)
         - the device contains exactly "deviceSize" blocks
         - address of first block is 0
         - address of last block is deviceSize-1
        """
        if not self.fileHandle:
            print('getCache warning:')
            print(' -> no device')
            print(' -> no operation')
            return None
        # check upper bound
        if ba >= self.deviceSize:
            print('getCache warning:')
            print(' -> address exceeds device size')
            print(' -> no operation')
            return None
        # flush data
        # ...
        # set address
        self.blockAddress = ba
        # set file pointer
        self.fileHandle.seek(3*4 + ba*self.blockSize)
        # read one block
        d = self.fileHandle.read(self.blockSize)
        # convert byte string into numpy array (mutable)
        self.blockData = np.copy(np.frombuffer(d, np.uint8))
        # done
        return self.blockData # reference to a mutable ndarray

    def flushCache(self):
        if self.fileHandle is None:
            print('flushCache warning:')
            print(' -> no device')
            print(' -> no operation')
            return
        if self.blockData is None:
            print('flushCache warning:')
            print(' -> no cache to flush')
            print(' -> no operation')
            return
        # set file pointer
        self.fileHandle.seek(3*4 + self.blockAddress*self.blockSize)
        # convert numpy array to binary string
        bs = self.blockData.tobytes()
        # write block
        d = self.fileHandle.write(bs)
        # done        
        return

if __name__ == "__main__":
    print("""
    # file virtualstorage.py
    # created 20201221
    # author Roch Schanen
    """)

    vs = virtualstorage()

    vs.setFilePath('./VS1MB')   # define a 1MB storage as an example
    vs.setWordSize(8)           # 8 bits
    vs.setBlockSize(16)         # 256 words
    vs.setDeviceSize(16)        # 4096 blocks
    vs.createDevice()           # create the new storage

    b1 = vs.getCache(0)
    b1[0] = 16
    vs.flushCache()

    b1 = vs.getCache(15)
    b1[0:16] = [255]*16
    vs.flushCache()

    vs.closeDevice()            # close storage
