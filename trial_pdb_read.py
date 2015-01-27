import os
import sys
import glob
global ligand
import shutil
molecule_list=[]
molecule_list=glob.glob(os.getcwd() +'/*.pdb')# read all the molecules in a directory and adds them to a list
RESOLUTION=0
for index in molecule_list:
	print "start of molecule: " + os.path.basename(index)
	ligand_file= open(index, 'r')
	for line in ligand_file:
		column=line.split()
		print column

	
	print RESOLUTION
	ligand_file.close()
	print "End of molecule: " + os.path.basename(index) +"\n\n"
print "Endof program"