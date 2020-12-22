#!/usr/bin/python3
# file virtualstorage.py
# created 20201221
# author Roch Schanen

from sys import exit

# 20201221 add virtual storage class

__DEBUG__ = True
# __DEBUG__ = False

class virtualstorage():

	wordSize 		= None 		# word size: depends on the data bus size ?
	blockSize 		= None		# block size: in units of wordsize
	blockStart      = None      # minimum block address value (depends on the header size ?)
	blockStop       = None      # maximum block address value (determines the device size)
	header 			= None      # record of the above values

	# additional parameters to use ? :
	# writing period, reading period, security access, ...
 
	blockAddress 	= None      # current block address: pointer to a block
	blockData 		= None      # data stored at the current block address

	# python implementation

	fileHandle 		= None
	filePath        = None


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

	def setBlockSize(self, value):
		if self.fileHandle:
			print('setBlockSize error:')
			print(' -> device locked')
			exit()
		if __DEBUG__: print(f'setBlockSize {value}')
		self.blockSize = value
		return

	def setBlocksNumber(self, value):
		if self.fileHandle:
			print('setBlocksNumber error:')
			print(' -> device locked')
			exit()
		if __DEBUG__: print(f'setBlocksNumber {value}')
		self.blockStop = value-1
		return		

	def setFilePath(self, value):
		if self.fileHandle:
			print('setFilePath error:')
			print(' -> device locked')
			exit()
		if __DEBUG__: print(f'setFilePath {value}')
		self.filePath = value
		return

	def createDevice(self):
		# check definitions
		error = False
		if not self.filePath:
			if not error: print('createDevice error')
			print(' -> filePath undefined')
			error = True
		if not self.wordSize:
			if not error: print('createDevice error')
			print(' -> wordSize undefined')
			error = True
		if not self.blockSize:
			if not error: print('createDevice error')
			print(' -> blockSize undefined')
			error = True
		if not self.blockStop:
			if not error: print('createDevice error')
			print(' -> blocksNumber undefined')
			error = True
		
		# encode wordSize 		
		ws, l = self.wordSize, 1
		while ws > 1:
			l  +=  1
			ws >>= 1
		
		print(ws, l)

		if error: exit()

		# # compute file size in bytes
		# fileSize = self.wordSize * self.blockSize * (self.blockStop + 1)
		# # create binary file to hold the data
		# f = open(self.filePath, "wb")
		# # fix the file size
		# f.seek(fileSize - 1)
		# f.write(b"\x00")

		return

	def closeDevice(self):
		# flush data		
		# close
		f.close()
		return

if __name__ == "__main__":
	print("""
	# file virtualstorage.py
	# created 20201221
	# author Roch Schanen
	""")

	vs = virtualstorage()

	vs.setFilePath('./VS1MB') 	# define a 1MB storage as an example
	vs.setWordSize(8)           # 8 bits data words
	vs.setBlockSize(256)        # 256 words/bytes per blocks
	vs.setBlocksNumber(4096)    # 4096 blocks in device

	vs.createDevice()           # create the new storage
	vs.setWordSize(7)           # 8 bits data words
	vs.createDevice()           # create the new storage
	vs.setWordSize(6)           # 8 bits data words
	vs.createDevice()           # create the new storage
	vs.setWordSize(5)           # 8 bits data words
	vs.createDevice()           # create the new storage
	vs.setWordSize(4)           # 8 bits data words
	vs.createDevice()           # create the new storage
	vs.setWordSize(3)           # 8 bits data words
	vs.createDevice()           # create the new storage
	vs.setWordSize(2)           # 8 bits data words
	vs.createDevice()           # create the new storage
	vs.setWordSize(1)           # 8 bits data words
	vs.createDevice()           # create the new storage


