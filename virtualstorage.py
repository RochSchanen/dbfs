#!/usr/bin/python3
# file virtualstorage.py
# created 20201221
# author Roch Schanen

from sys import exit

# 20201221 add virtual storage class
# 20201221 

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
		print('__init__')
		return

	def setWordSize(self, value):
		if fileHandle:
			print('setWordSize error')
			print(' -> device locked')
			exit()
		print(f'setWordSize {value}')
		self.wordSize = value
		return

	def setBlockSize(self, value):
		if fileHandle:
			print('setBlockSize error:')
			print(' -> device locked')
			exit()
		print(f'setBlockSize {value}')
		self.setBlockSize = value
		return

	def setBlocksNumber(self, value):
		if fileHandle:
			print('setBlocksNumber error:')
			print(' -> device locked')
			exit()
		print(f'setBlocksNumber {value}')
		self.blockStop = value-1
		return		

	def setFilePath(self, value):
		if fileHandle:
			print('setFilePath error:')
			print(' -> device locked')
			exit()
		print(f'setFilePath {value}')
		self.filePath = value
		return

	def createDevice(self):
		# check definitions
		error = False
		if not self.filePath:
			if not error: print('createDevice error')
			print('-> filePath undefined')
			error = True
		if not self.wordSize:
			if not error: print('createDevice error')
			print('-> wordSize undefined')
			error = True
		if not self.blockSize:
			if not error: print('createDevice error')
			print('-> blockSize undefined')
			error = True
		if not self.blockStop:
			if not error: print('createDevice error')
			print('-> blocksNumber undefined')
			error = True
		if error: exit()

		# compute file size in bytes
		# fileSize = self.wordSize * self.blockSize * (self.blockStop + 1)
		# f = open(self.filePath, "wb")
		# f.seek(fileSize - 1)
		# f.write(b"\x00")
		# f.close()

		return

if __name__ == "__main__":
	print("""
	# file virtualstorage.py
	# created 20201221
	# author Roch Schanen
	""")

	vs = virtualstorage()
	vs.createDevice()