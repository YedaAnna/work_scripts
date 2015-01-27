# @filename:gripdock.py
# @usage:
# @author: AbhiramG
# @description: does grip Docking
# @tags:Docking
# @version: 2.0 beta
# @date: Thursday Jan 15 2015
import os
import sys
import mds
import glob
import time
start_time = time.time()

base_address =  os.getcwd()
receptor_list = []
refrence_ligand = []
ligand_address = base_address + '/ligand_lib/'
# read all the molecules in a directory and adds them to a list
receptor_list = glob.glob(base_address + '/pdb/*.mol2')
refrence_ligand = glob.glob(base_address + '/ref_ligand/*.mol2')
mds.enableDiagnosticOutput()  # enable verbose output

for index in receptor_list:
    print "start of molecule: " + os.path.basename(index)
    actual_ref = []
    ind = []
    cavity = 1
    actualname = os.path.basename(index)
    actualname = actualname.replace('_cleaned.mol2', '')
    """ grip dock paranters are:
    mds.gripDock(receptorfile, ligand_directory, output dir, cavityno,
    refrence_lig, angle, plpgridmethod*true=>Fast, ligand placement,
    ligandwiseoutput*true/false, no of ligand wise outputs,
    is ligand flexible*true/False) """
    
    for names in refrence_ligand:
        if actualname in names:
            ind.append(refrence_ligand.index(names))
    if len(ind) == 0:
        pass
    else:
        for indx in ind:
            actual_ref.append(refrence_ligand[indx])
    if len(actual_ref) == 0:
        print "No refrence ligand found"
        cavity = 1
        actual_ref = [""]
    if not os.path.exists(base_address + '/output/' + actualname + '/'):
        os.makedirs(base_address + '/output/' + actualname + '/')

    output_dir = (base_address + '/output/' + actualname + '/')

    print index
    print ligand_address
    print output_dir
    print cavity
    print actual_ref[0]

    mds.gripDock(
        index,
        ligand_address,
        output_dir,
        cavity,
        actual_ref[0],
        15,
        True,
        30,
        True,
        10,
        True)  # do grip docking in batch mode

    print "\t =================>\t XXXXXXXXXXXXXXXXXX\t <=================="
    print "\n\n"

    sys.stdout.flush()
print "End of program"
print "Total time taken :" + str((time.time() - start_time)) + " seconds"
