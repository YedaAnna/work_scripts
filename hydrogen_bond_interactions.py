# @filename:hydrogen_bond_interaction.py
# @usage:
# @author: AbhiramG
# @description: 1. Gives information about all co crystal ligands present in receptor pdb_file
#		2. extracts each co-crystal ligand from pdb filename 
# 		3. Gives the hydrogen bond interactions with ligand and pdb and 
#		4. writes interaction in individual excel sheets
# @tags:ligand, interactions
# @version: 2.0 beta
# @date: wed Dec 31 2014
import os
import sys
import mds
import glob
import time
import xlsxwriter as xl
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
wb = xl.Workbook('hb_complete.xlsx')
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
    row = 8
    col = 0
    #wb=xl.Workbook('hb_' + str(os.path.basename(index))+'.xlsx')
    worksheet = wb.add_worksheet()

    worksheet.write(0, 0, ("The pdb is " + str(os.path.basename(index))))
    worksheet.write(1, 0, ("The resolution is " + (str(resolution))))
    worksheet.write(2, 0, ("list of ligands present are: " + str(ligand)))
    worksheet.write(3, 0, ("Corresponding chains are: " + str(chain)))
    worksheet.write(4, 0, ("List of unique ligands are: " + str(unique)))
    worksheet.write(5, 0, ("Name of ligands are: " + str(lig_name)))
    worksheet.write(6, 0, "Ligand")
    worksheet.write(6, 1, "chain")
    worksheet.write(6, 2, "Atom1")
    worksheet.write(6, 3, "Atom2")
    worksheet.write(6, 4, "grpName")
    worksheet.write(6, 5, "interaction_type")
    worksheet.write(6, 6, "distance")
    a = 0
    for a in range(len(ligand)):
        worksheet.write(row - 1, 0, "\n")
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
        worksheet.write(row, col, ligand[a])
        worksheet.write(row, col + 1, chain[a])
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
        t = col + 2
        for p in range(len(hbond)):

            for q in range(len(hbond[p])):

                worksheet.write(row, t, hbond[p][q])
                t += 1
                print str(hbond[p][q]) + "\t",
            t = col + 2
            row += 1
            print"\n"

    worksheet.write(row + 1, 0, "interaction_type: 0==>Hydrogen Bond, 1==> Charge, \
	2==>vanderwalls, 3==>hydrophobic, 4==>aromatic ")
    worksheet.write(row + 2, 0, "End of molecule: " + os.path.basename(index))
    worksheet = None

    mds.deleteMolecule(mol)  # release memory
    pdb_file.close()
    print "interaction_type: 0==>Hydrogen Bond, 1==> Charge, \
	2==>vanderwalls, 3==>hydrophobic, 4==>aromatic "
    print "End of molecule: " + os.path.basename(index) + "\n\n"
    print "\t =================>\t XXXXXXXXXXXXXXXXXX\t <=================="
    print "\n\n"

    sys.stdout.flush()
wb.close()
print "End of program"
print "Total time taken :" + str((time.time() - start_time)) + " seconds"
