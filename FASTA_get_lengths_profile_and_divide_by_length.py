__author__ = 'Wietrack 2019'

import sys
import operator
import hashlib

fasta_file = sys.argv[1]
cut_off = int(sys.argv[2])

lenghts_count = {}
loaded = False
titleRead = False

i = 0
n = 0
out_file_under = open(fasta_file + "_under_" +str(cut_off) + ".fa", 'w')
out_file_above = open(fasta_file + "_above_" +str(cut_off) + ".fa", 'w')
#load fasta sequences
for line in open(fasta_file):
    ch = line[0]
    if ch == '>':
        titleRead=True
        title = line[1:].strip()
    else:
        if titleRead:
            titleRead=False
            seq = line.strip()
            l = len(seq)
            # count the lengths
            if lenghts_count.has_key(l):
                lenghts_count[l] = lenghts_count[l] + 1
            else:
                lenghts_count[l] = 1
            # filter
            if len(seq) >= cut_off:
                out_file_above.write(">" + title +'\n')
                out_file_above.write(seq +'\n')
                i = i + 1
            else:
                out_file_under.write(">" + title +'\n')
                out_file_under.write(seq +'\n')
                n = n + 1

out_file_under.close()
out_file_above.close()

#save the lengths profile
out_file_profile = open(fasta_file + "_lengths_profile.txt", 'w')
s = set()
for l in lenghts_count:
    s.add(l)

s = sorted(s)
out_file_profile.write("length\tcounts\n")
for l in s:
    out_file_profile.write(str(l) + "\t" + str(lenghts_count[l]) +'\n')

out_file_profile.close()

print str(i + n) + " sequences processed by length - " + str(i) + " sequence above (>=) cutoff and " + str(n) + " uder cutoff : " + str(cut_off)
