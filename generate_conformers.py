# @filename:generate_conformers.py
# @usage:
# @author: AbhiramG
# @description: generates conformers for each mol2 file in folder
# @tags:Docking
# @version: 1.0 beta
# @date: Tuesday Jan 13 2015
import os
import sys
import mds
import glob
import time
start_time = time.time()
library_ligand = []

# read all the molecules in a directory and adds them to a list

library_ligand = glob.glob(os.getcwd() + '/*.mol2')
mds.enableDiagnosticOutput()  # enable verbose output

for index in library_ligand:
    print "start of molecule: " + os.path.basename(index)
    mol = mds.readMolecule(index)
    rotBonds = mds.getRotatableBonds(mol)  # get rotatable bonds
    print "no of rotatable bonds: " + str(len(rotBonds))
    # generate conformers, conformers are stored in caFileName
    caFileName = mds.generateConformer(
        mol,
        caType=2,
        noOfSeeds=10,
        FF=mds.FF.MMFF,
        rmsdCutoff=0.8,
        dieleFunc=1,
        rotatableBondList=rotBonds)
    print "\t =================>\t XXXXXXXXXXXXXXXXXX\t <=================="
    print "\n\n"
    mds.deleteMolecule(mol)

    sys.stdout.flush()
print "End of program"
print "Total time:" + str(round(((time.time() - start_time)), 3)) + " seconds"
