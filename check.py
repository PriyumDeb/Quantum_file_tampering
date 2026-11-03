import qiskit as qk
import qiskit_aer as qe
import math
file0=input()
file1=input()
a0=[]
a1=[]
with open(file0,'rb') as f: #binary because it have strict 255 limit not any more than that
    c=f.readlines()
with open(file1,'rb') as f1: #binary because it have strict 255 limit not any more than that
    g=f1.readlines()
for i in c:
    for j in i:
        binary_to_angle=(j/255) * math.pi
        a0.append(binary_to_angle)
for i in g:
    for j in i:
        binary_to_angle=(j/255) * math.pi
        a1.append(binary_to_angle)