__author__ = 'Wietrack 2016'

import sys
import operator

derep_fasta = sys.argv[1]
derep_table = sys.argv[2]
out_rerep_fasta = sys.argv[3]

fasta = {}

i = 0
#load fasta sequences
for line in open(derep_fasta):
    ch = line[0]
    if ch == '>':
        titleRead=True
        title = line[1:].strip()
    else:
        if titleRead:
            titleRead=False
            vals = title.split("|")
            fasta[vals[0]]=line.strip()
            i=i+1

print str(i)+" sequences loaded"

#process table
sr = 0
sf = 0
of = open(out_rerep_fasta, 'w')
for line in open(derep_table):
    vals = line.strip().split("\t")
    if fasta.has_key(vals[0]):
        of.write('>'+vals[1]+'\n')
        of.write(fasta[vals[0]]+'\n')
        sf = sf + 1
    else:
        #print vals[0]+" sequences loaded"
        sr = sr + 1
of.close()

print 'Dereplication is done - '+str(sf)+' sequences rereplicated / '+str(sr)+' sequences were not found...'


