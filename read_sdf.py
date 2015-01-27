# @filename:read_sdf.py
# @usage:
# @author: AbhiramG
# @description: reads complete sdf file and comapares with seperated mol2
# @tags:sdf
# @version: 1.0 b
# @date: Tue Jan 20 2015

import time

start_time = time.time()

ER_sdf = open(
    '/home/trainee3/Documents/project/THRB_ligands/THRB_lig.sdf', 'r')
# complete sdf file location

final = []
atoms = []
atomline = None
a = []
b = []
atom2 = []
other = []
for lines in ER_sdf:
    column = lines.split()
    if len(column) != 16:
        atomline = False
    else:
        atomline = True

    if atomline == True:
        if len(column[3]) > 2:
            pass
        else:
            atoms.append(column[3])
    else:
        a = atoms
        if len(a) == 0:
            pass
        else:
            final.append(a)
        atoms = []

sepdir = '/home/trainee3/Documents/project/THRB_ligands/THRB_lig/'
print len(final)
for i in range(len(final)):
    j = i + 1
    file = open(sepdir + 'THRB_lig_' + str(j) + '.mol2', 'r')
    for lines in file:
        column = lines.split()
        if len(column) != 10:
            aline = False
        else:
            aline = True

        if aline == True:
            atom2.append(column[1])
        else:
            b = atom2
            if len(b) == 0:
                pass
            else:
                other.append(b)
            atom2 = []
    h = 'H'
    while h in other[i]:
        other[i].remove(h)
    while h in final[i]:
        final[i].remove(h)

    if final[i] == other[i]:
        print "molecule " + str(j) + " matches perfectly in complete sdf and sepreated mol2"
    else:
        print "molecule " + str(j) + " does not match"
    file.close()
    """
    print str(j)
    print other[i]
    print final[i]
    print 'XXXXXXXXXXX'
    """
ER_sdf.close()
print "End of program"
print "Time taken= " + str(time.time() - start_time)
