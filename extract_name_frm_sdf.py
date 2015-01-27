# @filename:extract_name_frm_sdf.py
# @usage:
# @author: AbhiramG
# @description: 1. reads complete sdf file and extracts molecule names
#               2. writes them in xlsx sheet
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

name = []
nameline = None

wb = xl.Workbook('activity_name.xlsx')
ws = wb.add_worksheet()
ws.write(0, 0, "molecule")
ws.write(0, 1, "Name")
row = 1
col = 0
for lines in ER_sdf:
    column = lines.split()
    if len(column) != 3:
        pass
    else:
        if column[1] == '<Name>':
            nameline = True
        else:
            nameline = False

    if nameline == True and column[0] != '>':
        """and len(column) != 0"""
        name.append(column[0])
        nameline = False
    else:
        pass
for i in range(len(name)):
    print " The molecule is " + str(i + 1)
    print " name  is " + str(name[i])
    ws.write(row, col, "molecule no" + str(i + 1))
    ws.write(row, col + 1, name[i])
    row += 1
    print 'XXXXXXXXXXX'
wb.close()
ER_sdf.close()
print "End of program"
print "Time taken= " + str(time.time() - start_time)
