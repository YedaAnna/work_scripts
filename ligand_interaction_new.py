# @filename:ligand_interactions.py
# @usage: 
# @author: AbhiramG
# @description: ligand interaction in in a pdb file 
# @tags:ligand, interactions
# @version: 2.0 beta 
# @date: Thursday Dec 18 2014
import os
import sys
import mds
import glob
global ligand
molecule_list=[]
molecule_list=glob.glob(os.getcwd() +'/*.pdb')# read all the molecules in a directory and adds them to a list
mds.enableDiagnosticOutput()# enable verbose output
for index in molecule_list:
	print "start of molecule: " + os.path.basename(index)
	ligand=[]
	chain=[]
	ligand_file= open(index, 'r')
	for line in ligand_file:
                column = line.split()
                if column[0] == "HET":

                    ligand.append(column[1])
                    chain.append(column[2])
                    
	print "ligand is:" + str(ligand)
	print "chain is:" + str(chain)
	
	sys.stdout.flush()
	mol = mds.readMolecule(index) # read molecule from file  do operation on molecule object
	mds.addHydrogens(mol) # add hydrogens to molecule object
	if len(ligand)==None: continue
	
	a=0
	for a in range(len(ligand)):
		if len(chain[a]) !=1:
			print "chain name is not character"
			chain[a]= chain[a][0] 
		if len(ligand[a]) <3:
			print " Ligand name is less than 3 characters"
			ligand[a]= ' '+ ligand[a]
		ligand_molecule=mds.extractLigand(mol,ligand[a],chain[a])
		
		if ligand_molecule==None:
			print "ligand_molecule is none"
			continue
		mds.addHydrogens(ligand_molecule) # add hydrogens to ligand object
		interactions=mds.computeReceptorLigandInteraction(mol,ligand_molecule) # compute receptor-ligand interaction
		print " current Ligand is " + str(ligand[a]) + " in Chain :" + str(chain[a]) 
		if interactions==None:
			print "interactions are none"
			continue
		print "no of interactions are: " + str(len(interactions)) 
		print "List of interactions is :" 
		print "Atom1\t Atom2\t grpName\t interaction_type\t distance"
		i=j=0
		
		for i in range(len(interactions)):
			
			for j in range(len(interactions[i])):
				
				print str(interactions[i][j]) + "\t", 
			print "\n"
		
	mds.deleteMolecule(mol) # release memory
	ligand_file.close()
	print "interaction_type: 0==>Hydrogen Bond, 1==> Charge, \
	2==>vanderwalls, 3==>hydrophobic, 4==>aromatic "
	print "End of molecule: " + os.path.basename(index) +"\n\n"
	sys.stdout.flush() 
print "End of program"
