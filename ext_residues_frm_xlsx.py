# @filename:ext_residue_frm_xlsx.py
# @usage:
# @author: AbhiramG
# @description: extracts the residues involved in docking from the interactions.xlsx file
# @tags:Docking
# @version: 1.0 beta
# @date: Tue Jan 20 2015
import os
import time
import xlrd


def res():
    wb = xlrd.open_workbook('interactions.xlsx')
    ws = wb.sheet_by_name('Sheet1')

    collno = 4
    for rowno in range(ws.nrows):
        residues = []
        n = 1
        if ws.cell_value(rowno, collno) == 'grpName':
            while ws.cell_type(rowno + n, collno) != 0:
                residues.append(ws.cell_value(rowno + n, collno))
                n += 1
            print "\n"
            print "xxxxxxxxxxxxxxxxx"
            print ws.cell_value(rowno - 3, 0)
            print ws.cell_value(rowno - 2, 0)
            print ws.cell_value(rowno - 1, 0)
            # print ws.cell_value(rowno + 1, 4)
        if len(residues) == None:
            print "no interactions found"
        else:
            for res in range(len(residues)):
            	print residues[res]


start_time = time.time()
base_address = os.getcwd() + '/output/'
receptor_address = os.getcwd() + '/pdb/'
folder = []
folder = os.listdir(base_address)
for x in folder:
    os.chdir(base_address + '/' + x + '/')
    workbook = xlrd.open_workbook('best_poses.xlsx')
    worksheet = workbook.sheet_by_name('Sheet1')
    cellvalue = []
    print "The pdb is " + str(x)
    res()
print "End of program"
print "Time taken= " + str(time.time() - start_time)
