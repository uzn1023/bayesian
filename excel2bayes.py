##!/usr/bin/env python

import xlrd
import GPyOpt
import numpy as np

#excelファイルに読み込み
wb = xlrd.open_workbook("./BO_test.xlsx")
print(wb.sheet_names())
sheet = wb.sheet_by_name('Sheet1')
columns = [sheet.col_values(i) for i in range(sheet.ncols)]

inputs = []
inputs_numtype = []
inputs_domain = []
inputs_name = []
outputs = []
outputs_name = []
for i, column in enumerate(columns):
    if column[1] == "d":
        inputs_name.append(column[0])
        inputs.append(column[5:])
        inputs_numtype.append(column[1])
        inputs_domain.append(np.arange(float(column[2]), float(column[3]), float(column[4])))
    if column[1] == "io":
        inputs_name.append(column[0])
        inputs.append(column[5:])
        inputs_numtype.append(column[1])
        inputs_domain.append([int(column[2]), int(column[3])])
    if column[1] == "o":
        outputs_name.append(column[0])
        outputs.append(column[5:])

#予備実験のデータ
initial_x = np.array(inputs).T
initial_y = np.array(outputs[0])

initial_y = initial_y.reshape((-1,1))
#print(initial_x)

def f(x):
    print("next x")
    for n,value in zip(inputs_name,x[0]):
        print(n + ":" + str(value))
    score = float(input("Input y : "))
    return score

bounds = []
for i,input_name in enumerate(inputs_name):
    bound = {}
    bound["name"] = input_name
    if inputs_numtype[i] == "d":
        bound["type"] = "discrete"
    elif inputs_numtype[i] == "io":
        bound["type"] = "discrete"
    bound["domain"] = tuple(inputs_domain[i])
    
    bounds.append(bound)

myBopt = GPyOpt.methods.BayesianOptimization(f=f,
                                             domain=bounds,
                                             X = initial_x,
                                             Y = initial_y,
                                             normalize_Y=False,
                                             model_type = "GP",
                                             acquisition_type='LCB',               
                                             )

myBopt.run_optimization(max_iter=100)