import argparse
import binascii
from math import sqrt

colourTable = []

def isStrInt(s):
	"""Is the string an integer?"""
	try:
		int(s)
		return(True)
	except:
		return(False)


def errorQuit(e):
	if(e == 1):
		print("Colour Format contains a non-number character")
		quit(1)
	elif(e == 2):
		print("Colour Format doesn't contain 3 channels")
		quit(2)
	elif(e == 3):
		print("Colour Format contains a channel over 16 bits")
		quit(3)
	elif(e == 4):
		print("Size doesn't contain 2 numbers")
		quit(4)
	else:
		print("Undefined error")
		quit(404)


# Formats a decimal number to a binary number of a specific length.
def binaryFormatter(num, length):
	"""Formatter for the binary numbers"""
	return((('0'*length)+bin(((1<<length)-1)&int(num))[2:])[-length:])


# Formats a binary number to a hexadecimal number of a specific length.
def binaryToHexFormatter(num, length):
	"""Formatter for hex numbers from binary"""
	return((('0'*length)+hex(int(num,2))[2:])[-length:])


def mapGen(colourFormat,formatInfo):
	"Colour Map Generator, given an RGB integer format"
	
	oRed = 0
	redRange = range(0,colourFormat[3])
	greenRange = range(0,colourFormat[4])
	blueRange = range(0,colourFormat[5])
	
	redSmall = (colourFormat[6] - colourFormat[0])
	greenSmall = (colourFormat[6] - colourFormat[1])
	blueSmall = (colourFormat[6] - colourFormat[2])
	
	for red in redRange:
		oRed = red
		red = binaryFormatter(red,colourFormat[0])
		red = [red,
				('1' if oRed else '0')*redSmall]
		red = binaryToHexFormatter(''.join(red),colourFormat[7])
		
		for green in greenRange:
			oGreen = green
			green = binaryFormatter(green,colourFormat[1])
			green = [green,
				('1' if oGreen else '0')*greenSmall]
			green = binaryToHexFormatter(''.join(green),colourFormat[7])
			
			
			for blue in blueRange:
				oBlue = blue
				blue = binaryFormatter(blue,colourFormat[2])
				blue = [blue,
					('1' if oBlue else '0')*blueSmall]
				blue = binaryToHexFormatter(''.join(blue),colourFormat[7])
				
				colourTable.append(red+green+blue)


def main():
	"""Main function"""
	parser = argparse.ArgumentParser(
		description='Colour palette image generator')
	parser.add_argument('-f','--format',help='Colour format [RED:GREEN:BLUE]')
	parser.add_argument('-s','--size',help='Image size [WIDTH:HEIGHT]')
	parser.add_argument('-o','--output',help='Output file')
	args = parser.parse_args()
	
	
	colourFormat = [
		(int(x) if isStrInt(x) else errorQuit(1))
		for x in args.format.split(':')]
	formatLength = []
	formatInfo = []
	
	colourFormat.append(2**colourFormat[0])
	colourFormat.append(2**colourFormat[1])
	colourFormat.append(2**colourFormat[2])
	colourFormat.append(max(colourFormat[:-3]))
	colourFormat.append(4 if colourFormat[6] > 8 else 2)
	colourFormat.append(sum(colourFormat[:-5]))
	
	if(colourFormat[6] > 16):
		errorQuit(3)
	
	
	if(args.size):
		size = [
			(int(x) if isStrInt(x) else errorQuit(4))
			for x in args.size.split(':')]
		formatInfo.extend([size[0],size[1]])
	else:
		if(colourFormat[8] % 2):
			formatInfo.append(int(sqrt(2**(colourFormat[8]+1))))
			formatInfo.append(int(sqrt(2**(colourFormat[8]-1))))
		else:
			formatInfo.append(int(sqrt(2**colourFormat[8])))
			formatInfo.append(formatInfo[0])
	
	
	if(len(colourFormat[:-6]) == 3):
		outputName = args.output if args.output else 'r'+str(colourFormat[0])+\
			'g'+str(colourFormat[1])+'b'+str(colourFormat[2])+'.pam'
		
		with open(outputName,'w') as outFile:
			outFile.writelines(
				'P7\n'+
				'WIDTH '+str(formatInfo[0])+'\n'+
				'HEIGHT '+str(formatInfo[1])+'\n'+
				'MAXVAL '+str(2**(colourFormat[6])-1)+'\n'+
				'DEPTH 3\n'+
				'TUPLTYPE RGB\n'+
				'ENDHDR\n'
				)
			
			mapGen(colourFormat,formatInfo)
			outFile.write(binascii.unhexlify(''.join(colourTable)))
	else:
		errorQuit(2)


if __name__ == '__main__':
	main()
