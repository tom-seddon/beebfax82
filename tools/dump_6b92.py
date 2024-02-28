#!/usr/bin/python3
import sys,os,os.path,argparse
emacs=os.getenv('INSIDE_EMACS') is not None

def main2(options):
    with open(options.input_path,'rb') as f: data=f.read()

    base=0x6000
    addr=0x6b92

    As=set()
    Bs=set()
    Cs=set()
    Ds=set()
    
    assert (len(data)-(addr-base))%2==0
    num_entries=(len(data)-(addr-base))//2
    for index in range(num_entries):
        b0=data[addr-base+index*2+0]
        b1=data[addr-base+index*2+1]


        A=b0>>7
        B=b0&0x7f
        C=b1>>4
        D=b1&0xf

        As.add(A)
        Bs.add(B)
        Cs.add(C)
        Ds.add(D)

        print('$%04x: %d: %02x %02x (drive=%d track=%d C=%d sector=%d)'%(addr+index*2,index,b0,b1,A,B,C,D))

    print('All As: %s'%As)
    print('All Bs: %s'%Bs)
    print('All Cs: %s'%Cs)
    print('All Ds: %s'%Ds)

def main(argv):
    parser=argparse.ArgumentParser()
    parser.add_argument('input_path',metavar='FILE',help='''read main beebfax82 program from %(metavar)s''')
    main2(parser.parse_args(argv))

if __name__=='__main__': main(sys.argv[1:])
