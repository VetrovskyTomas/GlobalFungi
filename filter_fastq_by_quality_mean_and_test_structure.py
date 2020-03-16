__author__ = 'vetrot'

import sys
import os

in_fastq = sys.argv[1]
out_file = sys.argv[2]
mean = int(sys.argv[3])
as_fasta_info = sys.argv[4]

as_fasta = False
if as_fasta_info.upper() == 'TRUE':
    as_fasta = True

print "Save as FASTA: "+str(as_fasta)

def Average(lst):
    return reduce(lambda a, b: a + b, lst) / float(len(lst))

def get_qm(quality_string):
    lst = []
    for i in range(0, len(quality_string)):
        val = ord(quality_string[i]) - 33
        lst.append(val)
    return Average(lst)

def save_error_report(n):
    print "fastq format error..."
    fe = open('error_format_'+os.path.basename(in_fastq), 'w')
    fe.write('%s\n' % ('line '+str(n)))
    fe.close()
    return n

r1_0 = ''
r1_1 = ''
r1_2 = ''
r1_3 = ''
filled = False
ign = 0
tot = 0;
fp = open(out_file, 'w')
for n, line in enumerate(open(in_fastq)):
    if n % 400000 == 0:
        print n / 4
    if n % 4 == 0:
        r1_0 = line.rstrip()
        if r1_0[0] != '@':
            save_error_report(n)
            break
    else:
        if n % 4 == 1:
            r1_1 = line.rstrip()
        if n % 4 == 2:
            r1_2 = line.rstrip()
            if r1_2[0] != '+':
                save_error_report(n)
                break
        if n % 4 == 3:
            r1_3 = line.rstrip()
            filled = True

    if filled:
        tot = tot + 1
        qm = get_qm(r1_3)
        #print "qm "+str(qm)
        if qm >= mean:
            if as_fasta:
                fp.write('%s\n' % ('>'+r1_0[1:]))
                fp.write('%s\n' % r1_1)
            else:
                fp.write('%s\n' % r1_0)
                fp.write('%s\n' % r1_1)
                fp.write('%s\n' % r1_2)
                fp.write('%s\n' % r1_3)
        else:
            #print "low qm "+str(qm)+" sequence ignored: " + r1_0
            ign = ign + 1
        filled = False

fp.close()
print "Done. Ignored " + str(ign) + " sequences from total " + str(tot)
