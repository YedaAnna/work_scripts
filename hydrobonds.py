# @filename:hydrobonds.py
# @usage:
# @author: AbhiramG
# @description: Gives the hydrogen bond interactions with ligand in a pdb file
# @tags:ligand, interactions
# @version: 2.0 beta
# @date: Thursday Dec 18 2014
import os
import sys
import mds
import glob
import time
from collections import OrderedDict
start_time = time.time()


def HET():
    global unique_no
    global unique
    global pdb_file
    unique_no = 0
    pdb_file = open(index, 'r')
    for line in pdb_file:
        column = line.split()
        if column[0] == "HET":
            ligand.append(column[1])
            chain.append(column[2])
    print "list of ligands present:" + str(ligand)
    print "corresponding chains are:" + str(chain)
    unique = list(OrderedDict.fromkeys(ligand))
    unique_no = len(unique)
    print "List of unique ligands are : " + str(unique)
    pass


def RESOLUTION():
    global resolution
    resolution = 0
    pdb_file = open(index, 'r')
    for line in pdb_file:
        column = line.split()
        if column[0] == 'REMARK':
            if column[1] == '2':
                if len(column) > 2:
                    if column[2] == 'RESOLUTION.':
                        resolution = column[3]
    print "RESOLUTION of pdb is " + str(resolution) + " Angstroms"
    pass


def basic_info():
    HET()
    lig()
    RESOLUTION()
    pass


def lig():
    pdb_file = open(index, 'r')
    for line in pdb_file:
        column = line.split()
        if column[0] == 'HETNAM':
            if column[1] in unique:
                global temp
                joined = ' '.join(column[2:])
                lig_name.append(joined)
                temp = column[2]
            else:
                if column[1] == '3':
                    continue
                lig_name.remove(temp)
                joined2 = ' '.join(column[3:])
                temp2 = temp + joined2
                lig_name.append(temp2)

    print "Corresponding ligand name is : " + str(lig_name)

molecule_list = []
# read all the molecules in a directory and adds them to a list
molecule_list = glob.glob(os.getcwd() + '/*.pdb')
mds.enableDiagnosticOutput()  # enable verbose output
for index in molecule_list:
    print "start of molecule: " + os.path.basename(index)
    ligand = []
    chain = []
    lig_name = []
    pdb_file = open(index, 'r')
    basic_info()
    sys.stdout.flush()

    # read molecule from file  do operation on molecule object
    mol = mds.readMolecule(index)
    mds.addHydrogens(mol)  # add hydrogens to molecule object
    if len(ligand) == None:
        continue

    a = 0
    for a in range(len(ligand)):
        if len(chain[a]) != 1:
            print "chain name is not character"
            chain[a] = chain[a][0]
        if len(ligand[a]) < 3:
            print " Ligand name is less than 3 characters"
            ligand[a] = ' ' + ligand[a]
        ligand_molecule = mds.extractLigand(mol, ligand[a], chain[a])

        if ligand_molecule == None:
            print "ligand_molecule is none(not present)"
            continue
        mds.addHydrogens(ligand_molecule)  # add hydrogens to ligand object
        interactions = mds.computeReceptorLigandInteraction(
            mol, ligand_molecule)  # compute receptor-ligand interaction
        print "Current Ligand is " + str(ligand[a]) + " in Chain :" + str(chain[a])
        if interactions == None:
            print "interactions are none"
            continue
        print "Total no of interactions are: " + str(len(interactions))

        i = j = 0
        hbond = []
        for i in range(len(interactions)):

            for j in range(len(interactions[i])):

                if j == 3:
                    if (interactions[i][j]) == 0 or (interactions[i][j]) == 1:

                        hbond.append(interactions[i])
                    else:
                        continue
                    continue
        if len(hbond) == 0:
            print "No Hydrogen Bonds found"
            continue
        print "No of Hydrogen bonds are: " + str(len(hbond))
        print "List of interactions is :"
        print "Atom1\t Atom2\t grpName\t interaction_type\t distance"
        p = q = 0
        for p in range(len(hbond)):
            for q in range(len(hbond[p])):
                print str(hbond[p][q]) + "\t",
            print"\n"

    mds.deleteMolecule(mol)  # release memory
    pdb_file.close()
    print "interaction_type: 0==>Hydrogen Bond, 1==> Charge, \
	2==>vanderwalls, 3==>hydrophobic, 4==>aromatic "
    print "End of molecule: " + os.path.basename(index) + "\n\n"
    print "\t =================>\t XXXXXXXXXXXXXXXXXX\t <=================="
    print "\n\n"

    sys.stdout.flush()
print "End of program"
print "Total time taken :" + str((time.time() - start_time)) + " seconds"
