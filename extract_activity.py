# @filename:extract_activity.py
# @usage:
# @author: AbhiramG
# @description: reads complete sdf file and extracts activity and writes it in a xlsx sheet 
# @tags:sdf
# @version: 1.0 b
# @date: Tue Jan 20 2015

import time
import xlsxwriter as xl
start_time = time.time()

THRB_sdf = open(
    '/home/trainee3/Documents/project/THRB_ligands/THRB_lig.sdf', 'r')
# complete sdf file location

ER_sdf = open(
    '/home/trainee3/Documents/project/FDA/estrogen_receptor.sdf', 'r')

activity = []
activityline = None

wb = xl.Workbook('activity2.xlsx')
ws = wb.add_worksheet()
ws.write(0, 0, "molecule")
ws.write(0, 1, "activity")
row = 1
col = 0
for lines in ER_sdf:
    column = lines.split()

    if len(column) != 3:
        pass
    else:
        if column[1] == '<NCTRlogRBA>':
            activityline = True
        else:
            activityline = False

    if activityline == True and column[0] != '>' and len(column) != 0:
        activity.append(column[0])
        activityline = False
    else:
        pass

for i in range(len(activity)):
    print " The molecule is " + str(i + 1)
    print " activity is " + str(activity[i])
    ws.write(row, col, "molecule no" + str(i + 1))
    ws.write(row, col + 1, float(activity[i]))
    row += 1
    print 'XXXXXXXXXXX'
wb.close()
ER_sdf.close()
print "End of program"
print "Time taken= " + str(time.time() - start_time)
