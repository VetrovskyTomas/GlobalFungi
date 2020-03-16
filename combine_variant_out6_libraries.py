__author__ = 'Wietrack 2019'

import sys
import os
import hashlib

out6_library_old = sys.argv[1]
out6_library_new = sys.argv[2]
out6_library_out = sys.argv[3]

ot = open(out6_library_out, 'w')
er = open(out6_library_out+"_duplicates.txt", 'w')

blast_info = {}
i = 0
for line in open(out6_library_old):
    if i > 0:
        values = line.strip().split("\t")
        # "SEQ_HASH\tHIT\tSIMILARITY\tCOVERAGE\tEVALUE\tBITSCORE\tSH\tMARKER\tKINGDOM\n"
        hash = values[0]
        if not blast_info.has_key(hash):
            blast_info[hash] = line.strip()
            ot.write(line.strip()+"\n")
        else:
            er.write("OLD FILE LINE "+str(i)+" - DUPLICATE! - ORIGINAL: "+blast_info[hash]+"\n")
            er.write("OLD FILE LINE "+str(i)+" - DUPLICATE! NEW RECORD: "+line.strip()+"\n")
    else:
        ot.write(line.strip()+"\n")
    i = i + 1

records = len(blast_info)
print "Old library checked "+str(i)+" records - unique "+str(records)

i = 0
for line in open(out6_library_new):
    if i > 0:
        values = line.strip().split("\t")
        # "SEQ_HASH\tHIT\tSIMILARITY\tCOVERAGE\tEVALUE\tBITSCORE\tSH\tMARKER\tKINGDOM\n"
        hash = values[0]
        if not blast_info.has_key(hash):
            blast_info[hash] = line.strip()
            ot.write(line.strip()+"\n")
        else:
            er.write("NEW/OLD  LINE "+str(i)+" - DUPLICATE! - ORIGINAL: "+blast_info[hash]+"\n")
            er.write("NEW FILE LINE "+str(i)+" - DUPLICATE! NEW RECORD: "+line.strip()+"\n")
    i = i + 1

print "New library checked "+str(i)+" records - unique "+str(len(blast_info)-records)