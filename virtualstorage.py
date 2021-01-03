#!/usr/bin/python3
# file virtualstorage.py
# created 20201221
# author Roch Schanen

from sys import exit

import numpy as np

toByteString = int.to_bytes
frByteString = int.from_bytes 

# 20201221 add virtual storage class
# 20210101 create storage file
# 20210103 add openDevice, change class to virtuaLBlockDevice()

__DEBUG__ = True
# __DEBUG__ = False

class virtuaLBlockDevice():

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
            print('setWordSize warning')
            print(' -> device locked')
            print(' -> no operation')
            return
        if __DEBUG__: print(f'setWordSize {value}')
        self.wordSize = value
        return

    def getWordSize(self):
        return self.wordSize

    def setBlockSize(self, value):
        if self.fileHandle:
            print('setBlockSize warning:')
            print(' -> device locked')
            print(' -> no operation')
            return
        if __DEBUG__: print(f'setBlockSize {value}')
        self.blockSize = value
        return

    def getBlockSize(self):
        return self.block

    def setDeviceSize(self, value):
        if self.fileHandle:
            print('setDeviceSize warning:')
            print(' -> device locked')
            print(' -> no operation')
            return
        if __DEBUG__: print(f'setDeviceSize {value}')
        self.deviceSize = value
        return

    def getDeviceSize(self):
        return self.deviceSize

    def setFilePath(self, value):
        if self.fileHandle:
            print('setFilePath warning:')
            print(' -> device locked')
            print(' -> no operation')
            return
        if __DEBUG__: print(f'setFilePath {value}')
        self.filePath = value
        return

    def getFilePath(self):
        return self.filePath

    def writeHeader(self):
        if self.fileHandle is None:
            print('writeHeader error:')
            print(' -> no device')
            print(' -> exit')
            exit()
        # make buffer
        h = toByteString(self.wordSize, 4, 'little')
        h += toByteString(self.blockSize, 4, 'little')
        h += toByteString(self.deviceSize, 4, 'little')
        # write buffer
        self.fileHandle.write(h)
        # preserve
        self.header = h
        # done        
        return

    def readHeader(self):
        if self.fileHandle is None:
            print('readHeader error:')
            print(' -> no device')
            print(' -> exit')
            exit()
        # load buffer
        h = self.fileHandle.read(3*4)
        # extract parameters
        self.wordSize = frByteString(h[0:4], 'little')
        self.blockSize = frByteString(h[4:8], 'little')
        self.deviceSize = frByteString(h[8:12], 'little')
        # preserve
        self.header = h
        # done        
        return

    def createDevice(self, filePath = None):
        # option overload setup
        if filePath: self.filePath = filePath
        # check status
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
        # get parameters values
        ws, bs, ds = self.wordSize, self.blockSize, self.deviceSize
        # create binary file to hold the data
        self.fileHandle = open(self.filePath, "wb+")
        # make header
        self.writeHeader()
        # get header size in bits
        hs = len(self.header) << 3
        # compute file size in bits        
        bitFileSize  = ws*bs*ds + hs
        # compute file size in bytes
        byteFileSize = bitFileSize >> 3
        # fix 8 bits trucation
        if bitFileSize & 7: byteFileSize += 1  
        # point to the end-of-file
        self.fileHandle.seek(byteFileSize - 1)
        # write an arbitrary byte to set the file size
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
        self.flushCache()        
        # close
        self.fileHandle.close()
        # unlock handle
        self.fileHandle = None
        # done
        return

    def openDevice(self, filePath = None):
        # option overload setup
        if filePath: self.filePath = filePath
        # check status
        if self.fileHandle:
            print('openDevice error:')
            print(' -> device already opened')
            print(' -> no operation')
            return
        # open binary file
        self.fileHandle = open(self.filePath, "rb+")
        # read header
        self.readHeader()
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
        self.flushCache()
        # set address
        self.blockAddress = ba
        # get fileheader size
        hs = len(self.header)
        # set file pointer
        self.fileHandle.seek(hs+ba*self.blockSize)
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
            # print('flushCache warning:')
            # print(' -> no cache to flush')
            # print(' -> no operation')
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

    # EXAMPLE:

    vs = virtuaLBlockDevice()

    # -----------------------

    vs.setWordSize(8)
    vs.setBlockSize(8)
    vs.setDeviceSize(8)
    vs.createDevice('./VS1MB')

    # ---
    c = vs.getCache(0)
    c[0] = 1
    vs.flushCache()
    # ---

    vs.closeDevice()

    # -----------------------

    vs.openDevice('./VS1MB')

    # ---
    vs.getCache(1)[0] = 2
    vs.getCache(2)[0] = 3
    # ---

    vs.closeDevice()
