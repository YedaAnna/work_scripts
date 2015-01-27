# @filename:batch_clean_pdb_mds.py
# @usage: /VLife/bin/mds_cmd.exe batch_clean_pdb.py >& cleaning_log.log
# @author: AbhiramG
# @description: read all pdb files in directory and clean them
# @tags:pdb, clean
# @version: 2.5 beta
# @date: Tue Dec 16 2014

import os
import sys
import mds
import glob
import shutil
molecule_list = []
# read all the molecules in a directory and adds them to a list
molecule_list = glob.glob(os.getcwd() + '/*.pdb')
mds.enableDiagnosticOutput()  # enable verbose output
for index in molecule_list:
    print "start of molecule: " + os.path.basename(index)
    sys.stdout.flush()
    # read molecule from file  do operation on molecule object
    mol = mds.readMolecule(index)
    print ">> ADD HYDROGEN"
    sys.stdout.flush()
    mds.addHydrogens(mol)  # add hydrogens to molecule object
    print "<< ADD HYDROGEN"
    sys.stdout.flush()

    print ">> Retain chain "
    sys.stdout.flush()
    chain_ids = []
    chain_ids = mds.getChainIds(mol)  # get chain ids from a protein - molecule
    print "chains present in pdb:" + str(chain_ids)
    if len(chain_ids) == 1:
        # if only one chain is present
        mds.retainOnlyChainAndGroup(mol, chain_ids[0], [])
        print "retained chain :" + chain_ids[0]
    else:
        # retains chain A and all groups
        mds.retainOnlyChainAndGroup(mol, "A", [])
        print "retained chain : A"

    print "<< Retain chain "
    sys.stdout.flush()

    print ">> FIX INCOMPLETE"
    sys.stdout.flush()
    # fix incomplete residues for the protein - molecule by mutating them
    mds.fixIncompleteResidue(mol)
    print ">> FIX INCOMPLETE"
    sys.stdout.flush()

    print ">> FIX MODIFIED"
    sys.stdout.flush()
    # fix non-standard mutations to the protein molecule by substituting them
    # with appropriate well                                           known
    # amino-acid
    mds.fixModifiedResidue(mol)
    print "<< FIX MODIFIED"
    sys.stdout.flush()

    print ">> FIX MISSING"
    sys.stdout.flush()
    # fix missing residues in protein - molecule by subtituting loop from loop
    # database
    mds.fixMissingResidue(mol)
    print "<< FIX MISSING"
    sys.stdout.flush()

    # save a molecule object to disk
    mds.saveMolecule(mol, os.path.splitext(index)[0] + "_cleaned.mol2")
    mds.deleteMolecule(mol)  # release memory
    print "End of molecule: " + os.path.basename(index) + "\n\n"
    sys.stdout.flush()

clean_list = glob.glob(os.getcwd() + '/*.mol2')
os.makedirs(os.getcwd() + '/cleaned/')  # creates a directory called cleaned
for newindex in clean_list:
    # move all cleaned mol2 files in new folder called cleaned
    shutil.move(newindex, os.getcwd() + '/cleaned/')
print "End of program"
