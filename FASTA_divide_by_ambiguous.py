__author__ = 'Wietrack 2019'

import sys
import operator
import hashlib

fasta_file = sys.argv[1]

loaded = False
titleRead = False

i = 0
n = 0
out_file_correct = open(fasta_file + "_correct.fa", 'w')
out_file_ambiguous = open(fasta_file + "_ambiguous.fa", 'w')
#load fasta sequences
for line in open(fasta_file):
    ch = line[0]
    if ch == '>':
        titleRead=True
        title = line[1:].strip()
    else:
        if titleRead:
            titleRead=False
            seq = line.strip().upper()
            l = len(seq)
            # count the lengths
            count_A = seq.count('A')
            count_C = seq.count('C')
            count_T = seq.count('T')
            count_G = seq.count('G')

            # filter
            if l == (count_A + count_C + count_T + count_G):
                out_file_correct.write(">" + title +'\n')
                out_file_correct.write(seq +'\n')
                i = i + 1
            else:
                out_file_ambiguous.write(">" + title +'\n')
                out_file_ambiguous.write(seq +'\n')
                n = n + 1

out_file_correct.close()
out_file_ambiguous.close()

print str(i + n) + " sequences processed by ambiguosity - " + str(i) + " correct sequences vs " + str(n) + " ambiguous sequences"
