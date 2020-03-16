__author__ = 'vetrot'

import sys

in_text = sys.argv[1]
in_table = sys.argv[2]
out_text = sys.argv[3]
append = sys.argv[4]

app = False
if append.lower() == 'true':
    app = True
print 'appending '+ str(app)

#process pairing table...
repl_lenghts = {}
for line in open(in_table):
    dat = line.rstrip().split('\t')
    if repl_lenghts.has_key(len(dat[0])):
        to_replace = repl_lenghts[len(dat[0])]
        to_replace[dat[0]] = dat[1]
        repl_lenghts[len(dat[0])] = to_replace
    else:
        to_replace = {}
        to_replace[dat[0]] = dat[1]
        repl_lenghts[len(dat[0])] = to_replace
print "search table loaded - lenght distributions:"
for le in repl_lenghts:
    print "lenght "+str(le)+" has "+str(len(repl_lenghts[le]))+" of items..."

#text...
#write down the output...
n = 0
fp = open(out_text, 'w')
for line in open(in_text):
    l = line.rstrip()
    a = ''
    for i in range(0, len(l)):
        for le in repl_lenghts:
            word = l[i:i+le]
            if repl_lenghts[le].has_key(word):
                if app:
                    #append
                    a = repl_lenghts[le][word] + '|' + a
                else:
                    #replace
                    new_word = repl_lenghts[le][word]
                    l = l[0:i]+new_word+l[i+le:]
                    i = i+len(new_word)
                n = n + 1
    if app:
        if len(a) > 0:
            fp.write('>'+a+l[1:]+'\n')
        else:
            fp.write(l + '\n')
    else:
        fp.write(l + '\n')
fp.close()
print "done - "+str(n)+" of items replaced..."