# @filename:gripdock_interactions.py
# @usage:
# @author: AbhiramG
# @description: 1. reads gripdock log files and writes the best pose with score for each ligand to excel sheet
#		2. calculates interactions between best pose and receptor 
#		3. write the interactions in a excel sheet		
# @tags:Docking
# @version: 2.0 beta
# @date: Monday Jan 19 2015
import os
import sys
import glob
import time
import xlsxwriter as xl
import mds
from natsort import natsorted
start_time = time.time()

# read all the molecules in a directory and adds them to a list
base_address = os.getcwd() + '/output/'
receptor_address = os.getcwd() + '/pdb/'


folder = []
folder = os.listdir(base_address)
for x in folder:
     # read molecule from file  do operation on molecule object
    receptor = mds.readMolecule(receptor_address + x + '_cleaned.mol2')
    os.chdir(base_address + '/' + x + '/')
    logfile = []
    logfile = glob.glob(os.getcwd() + '/*.log')
    logfile = natsorted(logfile)
    logfile.pop(0)
    wb = xl.Workbook('best_poses.xlsx')
    ws = wb.add_worksheet()
    counter = 0
    inter = xl.Workbook('interactions.xlsx')
    row = 1
    col = 1
    worksheet = inter.add_worksheet()
    counter2 = 0
    interrow = 0
    intercol = 0
    for index in logfile:
        #worksheet = inter.add_worksheet()
        ws.write(0, 1, "Best pose ")
        ws.write(0, 2, "Score")
        interrow += 1
        print "receptor molecule is : " + str(x + '_cleaned.mol2')
        print "ligand molecule is : " + os.path.basename(index)
        file = open(index, 'r')
        best_pose = []
        score = []
        for lines in file:
            coloumn = lines.split()
            if len(coloumn) < 4:
                pass
            else:
                if coloumn[0] == 'Minimum':
                    best_pose.append(coloumn[5])
                    score.append(coloumn[8])

        sys.stdout.flush()
        #if not os.path.exists(os.getcwd() + '/best/'):
        #    os.makedirs(os.getcwd() + '/best/')
        for i in range(len(best_pose)):
            ws.write(row + counter, col, best_pose[i])
            ws.write(row + counter, col + 1, float(score[i].strip()))
            print "best pose is  " + str(best_pose[i])
            print "score is  " + str(score[i])
            #writelogfile(best_pose[i], score[i])
            row += 1
            #counter += 1
            ligand = mds.readMolecule(
                os.getcwd() + '/' + best_pose[i] + '.mol2')
            # shutil.copy(
            #    os.getcwd() + '/' + best_pose[i] + '.mol2',
            #    os.getcwd() + '/best')
            worksheet.write(
                interrow + 0, 0, ("The receptor is " + str(x + '_cleaned.mol2')))
            worksheet.write(
                interrow + 1, 0, ("Name of ligands : " + str(best_pose[i] + '.mol2')))
            worksheet.write(interrow + 2, 0, ("Score is " + str(score[i])))
            worksheet.write(interrow + 3, 2,  "Atom1")
            worksheet.write(interrow + 3, 3, "Atom2")
            worksheet.write(interrow + 3, 4, "grpName")
            worksheet.write(interrow + 3, 5, "interaction_type")
            worksheet.write(interrow + 3, 6, "distance")
            temp = interrow + 4
            interactions = mds.computeReceptorLigandInteraction(
                receptor, ligand)  # compute receptor-ligand interaction
            print "Current Ligand is " + str(best_pose[i])
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
            t = intercol + 2
            for p in range(len(hbond)):

                for q in range(len(hbond[p])):

                    worksheet.write(temp, t, hbond[p][q])
                    t += 1
                    print str(hbond[p][q]) + "\t",
                t = intercol + 2
                temp += 1
                print"\n"
        print "\t =================>\t XXXXXXXXXXXXXXXXXX\t <================="
        print "\n\n"
        interrow = temp + 1
        worksheet.write(interrow, 0, "XXXXXXXXXXXXXXXXXX")
    wb.close()
    inter.close()
print "End of program"
print "Total time taken :" + str((time.time() - start_time)) + " seconds"
