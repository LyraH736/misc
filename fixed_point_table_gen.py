import argparse


def isStrInt(s):
    """Is the string an integer?"""
    try:
        int(s)
        return(True)
    except:
        return(False)

def errorQuit(e):
    if(e <= 1):
        print("Format doesn't contain 3 values")
        quit(1)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Fixed point value table generator')
    parser.add_argument(
        '-f','--format',help='Float format [SIGN:INTEGER:FRACTION]')
    parser.add_argument('-o','--output',help='output file')
    parser.add_argument('-d','--data',action='store_true',
        help='outputs only the data')
    args = parser.parse_args()
    
    fixedFormat = [
        (int(x) if isStrInt(x) else errorQuit(1))
        for x in args.format.split(':')]
    
    if(len(fixedFormat) != 3): errorQuit(1)
    
    outputName = args.output if args.output else 's'+\
        str(fixedFormat[0])+'i'+str(fixedFormat[1])+'f'+\
            str(fixedFormat[2])+'.csv'
    
    fixedFormat.append(1 << fixedFormat[2])
    table = []
    outfile = open(args.output if args.output else outputName,'w')
    
    if not args.data:
        outfile.writelines(['int\\fra,']
            +[str(x)+',' for x in range(0,fixedFormat[3])]+['\n'])
    
    
    
    for sign in range(0,fixedFormat[0]+1):
        for ex in range(0,(1<<fixedFormat[1])):
            for ma in range(0,fixedFormat[3]):
                temp = ex+(ma/fixedFormat[3])
                table.append(-temp if sign else temp)
            
            exponent = [str(ex)+',']
            values = [str(x)+',' for x in table[-(1<<fixedFormat[2]):]]
            
            if args.data:
                lineOut = values+['\n']
            else:
                lineOut = exponent + values + ['\n']
            
            outfile.writelines(lineOut)


if __name__ == '__main__':
    main()
