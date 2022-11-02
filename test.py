import numpy as np
from time import *
import re
dict = {'H':1.00, 'He':4.002, 'Ti':47.867, 'Li':6.941, 'V':50.941, 'Cr':51.996, 'B':10.811,'Mn':54.938, 'Ag':107.868,
        'C':12.017,'Fe':55.845,'Cd':112.411, 'N':14.006, 'Co':58.933, 'In':114.818, 'Cu':63.546,'Na':22.989,'Mg':24.305,'Al':26.981,
        'Mo':95.94,'Ni':58.693,'Nb':92.90638,'Ta':180.9479,'W':183.84}
import sys



#控制台读取信息
#文件名
filename = str(sys.argv[1])
#元素数目
element_number = int(sys.argv[2])
fraction = []
ele = []

#读取种类名以及占比
for i in range(element_number):
    a = 2*i
    name = str(sys.argv[a+3])
    ele.append(name)
    fraction.append(float(sys.argv[a+4]))

#新文件名
new = str(sys.argv[element_number*2+3])


with open('%s'%filename) as file:
    lines = file.readlines()
    num_type = int(re.findall(r"\d+", lines[3])[0])
    matrix = np.loadtxt('%s'%filename, skiprows= 14 + num_type)
    np.random.seed(116)
    np.random.shuffle(matrix)
    number = [int(i * matrix.shape[0]) for i in fraction]
    total_number = []
    sum = 0
    for i in range(element_number):
        total_number.append(sum)
        sum += number[i]
    for i in range(element_number):
        if i != element_number - 1:
            matrix[total_number[i]:total_number[i + 1], 1] = i + 1
        else:
            matrix[total_number[i]:, 1] = i + 1
    matrix = matrix[np.argsort(matrix[:, 0])]
    np.savetxt('%s'%new, matrix, fmt='%10d%5d%17f%18f%17f', delimiter=' ')
#定义头文件信息
    data = ' # This script was writen by SSY' + '\n' + '\n'
    data += '        %d   atoms'%int(matrix.shape[0]) + '\n'
    data += "          %d   atom types"%element_number + '\n' + '\n'
    data += lines[5] + lines[6] + lines[7] + '\n' + 'Masses' + '\n' + '\n'
    for i in range(element_number):
        data += '           %d    %f   # %s'%(int(i+1), dict['%s'%ele[i]], ele[i]) + '\n'
    data += '\n' + 'Atoms # atomic' + '\n' + '\n'
#写入头文件
    with open('%s'%new, 'r+') as f:
        old = f.read()
        f.seek(0)
        f.write(data)
        f.write(old)



