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
        description='IEEE-compliant floating point value table generator')
    parser.add_argument(
        '-f','--format',help='Float format [SIGN:EXPONENT:MANTISSA]')
    parser.add_argument('-o','--output',help='output file')
    parser.add_argument('-d','--data',action='store_true',
        help='outputs only the data')
    parser.add_argument('-g','--greedy',action='store_true',
        help='Non-IEEE 754 compliant mode with only 2 NaNs')
    args = parser.parse_args()
    
    floatFormat = [
        (int(x) if isStrInt(x) else errorQuit(1))
        for x in args.format.split(':')]
    
    if(len(floatFormat) != 3): errorQuit(1)
    
    outputName = args.output if args.output else 's'+\
        str(floatFormat[0])+'e'+str(floatFormat[1])+'m'+\
            str(floatFormat[2])+'.csv'
    
    floatFormat.append(2**floatFormat[2])
    bias = 2**(floatFormat[1]-1)-1
    table = []
    outfile = open(args.output if args.output else outputName,'w')
    
    if not args.data:
        outfile.writelines(
            ['fra\\exp,']+
                [str(x)+',' for x in range(0,1<<floatFormat[2])]+
                    ['Precision','\n'])
    
    
    
    for sign in range(0,floatFormat[0]+1):
        for ex in range(0,(1<<floatFormat[1])):
            ex = float(ex)
            
            exbias = 2**(ex-bias)
            
            for ma in range(0,(1<<floatFormat[2])):
                ma = float(ma)
                if(ex == 0):
                    temp = exbias*(0+(ma/floatFormat[3]))
                    table.append(-temp if sign else temp)
                elif(ex == (1<<floatFormat[1])-1):
                    if args.greedy:
                        temp = (1<<floatFormat[2])-3
                        if(ma == temp):
                            table.append('-Inf' if sign else 'Inf')
                        elif(ma > temp):
                            table.append('NaN')
                        else:
                            temp = exbias*(1+(ma/floatFormat[3]))
                            table.append(-temp if sign else temp)
                    elif(ma == 0): table.append('-Inf' if sign else 'Inf')
                    else: table.append('NaN')
                else:
                    temp = exbias*(1+(ma/floatFormat[3]))
                    table.append(-temp if sign else temp)
            ex = int(ex)
            
            exponent = [str(ex)+',']
            values = [str(x)+',' for x in table[-(1<<floatFormat[2]):]]
            precision = [str('NaN' if ex == (1<<floatFormat[1])-1 and not args.greedy else
                exbias*(1+(ma/floatFormat[3]))-exbias*(1+((ma-1)/floatFormat[3]))),'\n']
            
            if args.data:
                lineOut = values+['\n']
            else:
                lineOut = exponent + values + precision
            
            outfile.writelines(lineOut)


if __name__ == '__main__':
    main()
