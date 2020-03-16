__author__ = 'vetrot'

import sys
import os
import hashlib

variants_table = sys.argv[1]
sh_table = sys.argv[2]
# 0 - SH
# 8 - species
# 7 - genus
variants_fasta = sys.argv[3]

out_name = variants_table
if out_name.endswith('.txt'):
    out_name = out_name[:-4]
print "Output file name root: " + out_name


taxonomy = {}

for n, line in enumerate(open(sh_table)):
    if n==0:
        vals = line.rstrip().split('\t')
        print "sh "+vals[0]+" sp "+vals[8]+" gen "+vals[7]
    else:
        vals = line.rstrip().split('\t')
        taxonomy[vals[0]] = vals[8]+";"+vals[7]

print "taxonomy loaded..."

sequnces = {}
titleRead=False
#load fasta sequences
for line in open(variants_fasta):
    ch = line[0]
    if ch == '>':
        titleRead=True
        title = line[1:].strip()
    else:
        if titleRead:
            sequnces[title] = line.strip()
            titleRead=False

print "sequences loaded..."

samples = {}
sh = {}
sp = {}
gen = {}

def process_samples_to_sh(dict, key, vals):
    keyid = sh[key]
    row_samples = vals[1].split(';')
    for s in row_samples:
        if dict.has_key(s):
            shset = dict[s]
            shset.add(keyid)
            dict[s] = shset
        else:
            shset = set()
            shset.add(keyid)
            dict[s] = shset

def process_taxon_table(taxon, key, vals):
    if taxon.has_key(key):
        # samples...
        sampl = taxon[key]["sampl"]
        aa = vals[2].split(';')
        ss = vals[1].split(';')
        for x in range(len(ss)):
            if sampl.has_key(ss[x]):
                sampl[ss[x]] = sampl[ss[x]] + int(aa[x])
            else:
                sampl[ss[x]] = int(aa[x])
        # hash...
        taxon[key]["varia"] = taxon[key]["varia"] + 1
    else:
        taxon[key] = {}
        # samples...
        sampl = {}
        aa = vals[2].split(';')
        ss = vals[1].split(';')
        for x in range(len(ss)):
            sampl[ss[x]] = int(aa[x])
        taxon[key]["sampl"] = sampl
        # hash...
        taxon[key]["varia"] = 1

def write_taxon_table(taxon, name, skip_key):
    out_file = open(out_name + name, 'w')
    for tax in taxon:
        if tax == skip_key:
            print name + " - key skipped: "+tax
            continue
        sampl_line = ""
        abund_line = ""
        shs_line = ""
        # samples and abundances
        sampl = taxon[tax]["sampl"]
        for s in sampl:
            sampl_line += ";" + str(samples[s])
            abund_line += ";" + str(sampl[s])
        # SAVE LINE <rod>;<vzorky>;<abundance>;<varianty>
        out_file.write(tax + "\t" + sampl_line[1:] + "\t" + abund_line[1:] + "\t" + str(taxon[tax]["varia"]) + "\n")
    out_file.close()
    print name + " table was saved..."
    print ""

not_found_keys = {}
sh_table = {}
sp_table = {}
gen_table = {}
all_table = {}
samples_to_sh = {}

out_file = open(out_name + '_PROCESSED.txt', 'w')
out_fasta = open(out_name + '_PROCESSED_VARIANTS.fa', 'w')

for n, line in enumerate(open(variants_table)):
    if n == 0:
        print "HEADER: "+line.strip()
    else:
        l = line.rstrip()
        vals = l.split('\t')
        shkey = vals[len(vals) - 1]
        if (taxonomy.has_key(shkey)) or (shkey == "-"):
            sample_line = ""
            ss = vals[1].split(';')
            for s in ss:
                if samples.has_key(s):
                    sample_line += ";" + str(samples[s])
                else:
                    samples[s] = len(samples) + 1
                    sample_line += ";" + str(samples[s])
            # All samples counts
            process_taxon_table(all_table, vals[3], vals)
            # save FASTA
            out_fasta.write(">" + vals[0] +'\n')
            out_fasta.write(sequnces[vals[0]] +'\n')
            if shkey == "-":
                out_file.write(vals[0] + "\t" + sample_line[1:] + "\t" + vals[2] + "\t" + vals[3] + "\t0\t0\t0\t" + sequnces[vals[0]] + "\n")
            else:
                if not sh.has_key(shkey):
                    sh[shkey] = len(sh) + 1
                spgen = taxonomy[shkey].split(';')
                if not sp.has_key(spgen[0]):
                    sp[spgen[0]] = len(sp) + 1
                if not gen.has_key(spgen[1]):
                    gen[spgen[1]] = len(gen) + 1
                # write main table...
                out_file.write(vals[0] + "\t" + sample_line[1:] + "\t" + vals[2] + "\t" + vals[3] + "\t" + str(sh[shkey]) + "\t" + str(sp[spgen[0]]) + "\t" + str(gen[spgen[1]]) + "\t" + sequnces[vals[0]] + "\n")
                # SH table
                process_taxon_table(sh_table, shkey, vals)
                # Species table
                process_taxon_table(sp_table, spgen[0], vals)
                # Genus table
                process_taxon_table(gen_table, spgen[1], vals)
                # Samples to SH
                process_samples_to_sh(samples_to_sh, shkey, vals)
        else:
                if not_found_keys.has_key(shkey):
                    not_found_keys[shkey] = not_found_keys[shkey] + 1
                else:
                    not_found_keys[shkey] = 1

out_fasta.close()
out_file.close()

##################
# WRITE WARNINGS #
##################
out_file = open(out_name + '_WARNINGS.info', 'w')
for key in not_found_keys:
    out_file.write("Key not found: " + key + " - count: " + str(not_found_keys[key]) + "\n")
out_file.close()
print "Warnings " + str(len(not_found_keys))
######################
# WRITE TAXON TABLES #
######################

write_taxon_table(sh_table, '_TAB_SH.txt','-')
write_taxon_table(sp_table, '_TAB_SPECIES.txt','Fungi sp.')
write_taxon_table(gen_table, '_TAB_GENUS.txt','unidentified')

# write all sample counts
out_file = open(out_name + "_ALL_SAMPLES_COUNTS.info", 'w')
i1 = 0
i2 = 0
for s in samples:
    ITS1 = 0
    ITS2 = 0
    if all_table["ITS1"]["sampl"].has_key(s):
        ITS1 = all_table["ITS1"]["sampl"][s]
        i1 += 1
    if all_table["ITS2"]["sampl"].has_key(s):
        ITS2 = all_table["ITS2"]["sampl"][s]
        i2 += 1
    out_file.write(s + "\t" + str(ITS1) + "\t" + str(ITS2) + "\n")
out_file.close()
print "All samples counts table was saved... ITS1 " + str(i1) + " ITS2 " + str(i2)
print ""

# write samples to SH
out_file = open(out_name + "_SAMPLES_TO_SH.txt", 'w')
for s in samples_to_sh:
    out_file.write(str(samples[s])+"\t"+';'.join(str(x) for x in samples_to_sh[s])+"\n")
out_file.close()

############################
# WRITE ALL PAIRING TABLES #
############################

out_file = open(out_name + '_SAMPLES.txt', 'w')
for s in samples:
    out_file.write(str(samples[s]) + "\t" + s + "\n")
out_file.close()
print "Samples found " + str(len(samples))
print ""

out_file = open(out_name + '_SH.txt', 'w')
for s in sh:
    out_file.write(str(sh[s]) + "\t" + s + "\n")
out_file.close()
print "SH found " + str(len(sh))
print ""

out_file = open(out_name + '_SPECIES.txt', 'w')
for s in sp:
    out_file.write(str(sp[s]) + "\t" + s + "\n")
out_file.close()
print "SPECIES found " + str(len(sp))
print ""

out_file = open(out_name + '_GENUS.txt', 'w')
for s in gen:
    out_file.write(str(gen[s]) + "\t" + s + "\n")
out_file.close()
print "GENUS found " + str(len(gen))
print ""

print "DONE :]"
