__author__ = 'Wietrack 2019'

import sys
import operator
import hashlib

fasta_file = sys.argv[1]
out_fasta = sys.argv[2]

md5_titles = set()
loaded = False
titleRead = False

i = 0
n = 0
out_file = open(out_fasta, 'w')
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
            if len(seq)>0:
                md5_title = hashlib.md5(seq.encode()).hexdigest()
                if md5_title not in md5_titles:
                    out_file.write(">" + md5_title +'\n')
                    out_file.write(seq +'\n')
                    md5_titles.add(md5_title)
                i=i+1
            else:
                n = n + 1

out_file.close()

print "{0} sequnces were empty - Omitted! Variants {1} out of {2}".format(str(n), str(len(md5_titles)), str(i))
