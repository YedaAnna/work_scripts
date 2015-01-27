# @filename:ligand_ext.py
# @usage: 
# @author: AbhiramG
# @description: ligand extraction from pdb file 
# @tags:ligand, extracting
# @version: 2.0 beta 
# @date: Tue Dec 17 2014
import os
import sys
import mds
import glob
global ligand
import shutil
molecule_list=[]
molecule_list=glob.glob(os.getcwd() +'/*.pdb')# read all the molecules in a directory and adds them to a list
mds.enableDiagnosticOutput()# enable verbose output
for index in molecule_list:
	print "start of molecule: " + os.path.basename(index)
	ligand=[]
	chain=[] 
	atom_no=[]
	ligand_file= open(index, 'r')
	for line in ligand_file:
                column = line.split()
                if column[0] == "HET":
                    
                    ligand.append(column[1])
                    chain.append(column[2])
                    if len(column[2])!=1:
                    	atom_no.append(column[3])
                    	continue
                    atom_no.append(column[4])

	print ligand
	print chain 
	print atom_no            
	print "ligand is:" + str(ligand)
	
	sys.stdout.flush()
	mol = mds.readMolecule(index) # read molecule from file  do operation on molecule object
	if len(ligand)==None: continue
	
	i=0
	for i in range(len(ligand)):
		if atom_no[i]<=10:
			continue
		if len(chain[i]) !=1:
			print "chain is not char"
			chain[i]= chain[i][0] 
		ligand_molecule=mds.extractLigand(mol,ligand[i],chain[i])
		
		if ligand_molecule==None:
			print "ligand_molecule is none"
			continue
		mds.saveMolecule(ligand_molecule, os.path.splitext(index)[0] + "_" + ligand[i] +"_" + chain[i] +".mol2") # save a molecule object to disk
	mds.deleteMolecule(mol) # release memory
	ligand_file.close()
	print "End of molecule: " + os.path.basename(index) +"\n\n"
lig_list= glob.glob(os.getcwd() +'/*_*_*.mol2')	
os.makedirs(os.getcwd()+'/ligand/')	#creates a directory called cleaned
for newindex in lig_list:
	shutil.move(newindex, os.getcwd() +'/ligand/') # move all ligand mol2 files in new folder called ligand
sys.stdout.flush() 
print "End of program"