# @filename:read_conf.py
# @usage:
# @author: AbhiramG
# @description: reads log files
# @tags:Docking
# @version: 1.0 beta
# @date: Tuesday Jan 13 2015
import os
import sys
import glob
import time
import xlsxwriter as xl
start_time = time.time()

logfile = []
# read all the molecules in a directory and adds them to a list
base_address = '/home/trainee3/Documents/project/THRB_pdb'

logfile = glob.glob(base_address + '/grip/1nax/*.log')

wb = xl.Workbook('best_poses.xlsx')
worksheet = wb.add_worksheet()
counter = 0
for index in logfile:

    worksheet.write(0, 1, "Best pose ")
    worksheet.write(0, 2, "Score")
    row = 1
    col = 1
    print "start of molecule: " + os.path.basename(index)
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
    for i in range(len(best_pose)):
        row += 1
        worksheet.write(row + counter, col, best_pose[i])
        worksheet.write(row + counter, col + 1, score[i])
        print "best pose is  " + str(best_pose[i])
        print "score is  " + str(score[i])
    counter += 1
    print "\t =================>\t XXXXXXXXXXXXXXXXXX\t <=================="
    print "\n\n"
wb.close()
print "End of program"
print "Total time taken :" + str((time.time() - start_time)) + " seconds"
