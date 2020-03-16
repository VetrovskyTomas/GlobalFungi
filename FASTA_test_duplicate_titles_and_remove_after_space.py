__author__ = 'Wietrack 2019'

import sys
import operator
import hashlib

fasta_file = sys.argv[1]

titles = {}
loaded = False
titleRead = False
i = 0
n = 0
out_file = open(fasta_file + "_noduplicates_nospaces.fa", 'w')
out_duplicates = open(fasta_file + "_duplicates.fa", 'w')
#load fasta sequences
for line in open(fasta_file):
    ch = line[0]
    if ch == '>':
        titleRead=True
        title = line[1:].strip().split(" ")[0]
    else:
        if titleRead:
            titleRead=False
            seq = line.strip()
            if titles.has_key(title):
                out_duplicates.write(">ORIGINAL:" + title +'\n')
                out_duplicates.write(titles[title] +'\n')
                out_duplicates.write(">DUPLICAT:" + title +'\n')
                out_duplicates.write(seq +'\n')
            else:
                titles[title] = seq
                out_file.write(">" + title +'\n')
                out_file.write(seq +'\n')
                n = n + 1
            i = i + 1

out_file.close()
out_duplicates.close()

print str(i) + " sequences processed - " + str(n) + " unique sequences " + str(i-n) + " duplicate sequences"
