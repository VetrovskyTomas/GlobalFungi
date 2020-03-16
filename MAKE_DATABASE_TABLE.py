__author__ = 'vetrot'

import sys
import os
import hashlib

its1_fasta_file = sys.argv[1]
its2_fasta_file = sys.argv[2]
#>S000924|McHugh_2014_F229|Seq97787038@

processed_blast = sys.argv[3]
#SEQ_HASH        HIT     SIMILARITY      COVERAGE        EVALUE  BITSCORE        SH      MARKER  KINGDOM
#6629a42f30fec4c0b02c454271661ee6        NO_HIT  -       -       -       -       NO_HIT  ITS1    NO_HIT
#9687f5c29339d76584e98baa47c59d52        GS11_sp|JQ666719|SH1566775.08FU|reps|k__Fungi;p__Rozellomycota;c__Rozellomycotina_cls_Incertae_sedis;o__GS11;f__unidentified;g__unidentified;s__GS11_sp 95.968  96.062992126    3.80e-51        200     SH1566775.08FU  ITS1    k__Fungi

out_table = sys.argv[4]
out_fasta = sys.argv[5]

# Tresholds
th_similarity = float(sys.argv[6]) #98.5
th_coverage = float(sys.argv[7])   #90.0

# errors and warnings...
out_error = open("LOG_ERRORS_AND_WARNINGS.txt", 'w')
#############################################
# GET ANNOTATION
#############################################
identification={}
i = 0
k = 0
l = 0
for n, line in enumerate(open(processed_blast)):
    if n>0:
        vals = line.rstrip().split('\t')
        if vals[6] == 'NO_HIT':
            vals[6] = '-'
        if identification.has_key(vals[0]):
            info = "ANNOTATION_DUPLICATE: " + vals[0] + "\t" + identification[vals[0]] + "\t" + vals[6] + "|" + vals[7]
            out_error.write(info + "\n")
            print info
            l = l + 1
        else:
            if vals[6] != '-' and float(vals[2]) >= th_similarity and float(vals[3]) >= th_coverage:
                identification[vals[0]] = vals[6] + "|" + vals[7]
                i = i + 1
            else:
                identification[vals[0]] = "-|" + vals[7]
        k = n

info = str(k)+" annotations loaded -> "+str(i)+" fulfill the criteria tresholds - similarity " + str(th_similarity) + " and coverage " + str(th_coverage)
out_error.write(info + "\n")
print info

info = str(l)+" annotations duplicates !!! (MUST BE 0)"
out_error.write(info + "\n")
print info

#############################################
# PROCESS FASTA FUNCTION
#############################################
# errors and warnings...
out_not_found = open("VARIANTS_NOT_FOUND.fa", 'w')

samples = {}
variants = {}
seq_variants = {}

def process_fasta(fasta_file,marker):
    i = 0
    n = 0
    titleRead = False
    #load fasta sequences for replacement
    for line in open(fasta_file):
        ch = line[0]
        if ch == '>':
            titleRead=True
            title = line[1:].strip()
        else:
            if titleRead:
                titleRead=False
                seq = line.strip()
                hash = hashlib.md5(seq.encode()).hexdigest()
                vals = title.split('|')
                # store and check all the sequences variants...
                if seq_variants.has_key(hash):
                    if seq_variants[hash] != seq:
                        info = "ERROR - MD5 HASH NOT UNIQUE: " + hash
                        out_error.write(info + "\n")
                        out_error.write(seq_variants[hash] + "\n")
                        out_error.write(seq + "\n")
                        print info
                else:
                    seq_variants[hash] = seq
                # get annotation
                if identification.has_key(hash):
                    n = n + 1
                    ids = identification[hash].split('|')
                    if marker == ids[1]:
                        # add all sample counts for every hash...
                        if variants.has_key(hash):
                            if variants[hash].has_key(vals[0]):
                                variants[hash][vals[0]] = variants[hash][vals[0]] + 1
                            else:
                                variants[hash][vals[0]] = 1
                        else:
                            variants[hash] = {}
                            variants[hash][vals[0]] = 1
                    else:
                        info = "ERROR - MARKER DIFFERS:" + marker + " vs " + ids[1] + " for: " + hash + " title " + title
                        out_error.write(info + "\n")
                        print info
                else:
                    info = "ERROR - MD5 HASH NOT FOUND: " + hash
                    out_error.write(info + "\n")
                    out_not_found.write(">" + hash + "\n")
                    out_not_found.write(seq + "\n")
                    print info
                i = i + 1
    return str(i) + ' sequences processed - ' + str(n) + ' correctly ' + str(i-n) + " ERRORS!!!"

#############################################
# PROCESS ITS1 and ITS2
#############################################
info = process_fasta(its1_fasta_file, 'ITS1')
out_error.write(info + "\n")
print info
info = process_fasta(its2_fasta_file, 'ITS2')
out_error.write(info + "\n")
print info

#############################################
# WRITE TABLE
#############################################
fp = open(out_table, 'w')
fa = open(out_fasta, 'w')
#header
line_new = 'hash\tsamples\tabundances\tmarker\tSH'
fp.write(line_new + "\n")
#lines...
for hash in variants:
    samples = ''
    abundances = ''
    i = 0
    for sample in variants[hash]:
        if i == 0:
            samples = samples + sample
            abundances = abundances + str(variants[hash][sample])
        else:
            samples = samples + ';' + sample
            abundances = abundances + ';' + str(variants[hash][sample])
        i = i + 1
    ###############################################
    #compose...
    ids = identification[hash].split('|')
    line_new = hash + '\t' + samples + '\t' + abundances + '\t' + ids[1] + '\t' + ids[0]
    fp.write(line_new + "\n")
    fa.write(">" + hash + "\n")
    fa.write(seq_variants[hash] + "\n")
fp.close()
fa.close()

###############
out_error.close()
out_not_found.close()

print 'table saved successfuly...'
