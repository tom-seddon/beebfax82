#!/usr/bin/python3
import sys,os,os.path,argparse

def fatal(msg):
    sys.stderr.write('FATAL: %s\n'%msg)
    sys.exit(1)

def main2(options):
    with open(options.runner_path,'rb') as f: runner_data=f.read()
    with open(options.disk_path,'rb') as f: disk_data=f.read()

    base=0x6000
    addr=0x6b92

    b0b1_seen=set()
    page_numbers_seen=set()

    assert (len(runner_data)-(addr-base))%2==0
    num_entries=(len(runner_data)-(addr-base))//2
    for index in range(num_entries):
        b0=runner_data[addr-base+index*2+0]
        b1=runner_data[addr-base+index*2+1]

        if (b0,b1) in b0b1_seen: continue
        b0b1_seen.add((b0,b1))

        drive=0 if (b0&0x80)==0 else 2
        if drive==2: fatal('page on drive 2 encountered')

        track=b0&0x7f
        sector=b1&0xf

        offset=(track*10+sector)*256
        raw_page_data=disk_data[offset:offset+1024]

        unpacked_page_data=bytearray()
        i=0
        while i<len(raw_page_data):
            if raw_page_data[i]==0xff: break
            elif (raw_page_data[i]&0x80)==0:
                unpacked_page_data.append(raw_page_data[i])
                i+=1
            else:
                n=2+(raw_page_data[i+0]&0x7f)
                unpacked_page_data+=n*raw_page_data[i+1:i+2]
                i+=2

        if not (unpacked_page_data[0]==32 and
                unpacked_page_data[1]==32 and
                unpacked_page_data[2]==ord('P') and
                chr(unpacked_page_data[3]).isdigit() and
                chr(unpacked_page_data[4]).isdigit() and
                chr(unpacked_page_data[4]).isdigit()):
            fatal('index %d not obviously a teletext page'%index)

        page_number=(chr(unpacked_page_data[3])+
                     chr(unpacked_page_data[4])+
                     chr(unpacked_page_data[5]))
        if page_number in page_numbers_seen:
            fatal('seen page number more than once: %s'%page_number)
        page_numbers_seen.add(page_number)
                
        if options.output_path is not None:
            def save(suffix,data):
                with open(os.path.join(options.output_path,
                                       '%s.%s.dat'%(page_number,suffix)),
                          'wb') as f:
                    f.write(data)

            save('raw',raw_page_data)
            save('unpacked',unpacked_page_data)

def main(argv):
    parser=argparse.ArgumentParser()
    parser.add_argument('-o',metavar='FOLDER',dest='output_path',help='''write output files to %(metavar)s''')
    parser.add_argument('runner_path',metavar='RUNNER-FILE',help='''read main runner program from %(metavar)s''')
    parser.add_argument('disk_path',metavar='DISK-FILE',help='''read ssd file from %(metavar)s''')
    main2(parser.parse_args(argv))

if __name__=='__main__': main(sys.argv[1:])
