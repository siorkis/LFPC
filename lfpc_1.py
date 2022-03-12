import networkx as nx
import numpy as np
import pylab
#Ex. 1
# Convert RG to FA
vn_unsorted = input("Input Vn elements (print space between letters)\n")
vn = vn_unsorted.split(" ")
vn.append(".")

print("VN = {}".format(vn))
connections = int(input ("Input number of connections\n"))

matrix_graph = [[0 for x in range(len(vn))] for y in range(len(vn))]

print('Input connection in "A b C" format OR "A b ." ')

for k in range(connections):
    i = 0
    j = 0
    vertex_start, weight, vertex_terminal = input().split(" ")
    for n in range(len(vn)):
        if vn[n] == vertex_start: i = n
        if vn[n] == vertex_terminal: j = n

    matrix_graph[i][j] = weight

for i in range(5):
    print(matrix_graph[i])


#Ex. 2
#Check if there could exist such word in FA
word = input ("Input word to verification:\n")
check_var = True
word_len = len(word)

h = 0 # counter for final values

final_values = [0 for i in range(len(vn))]
j = len(vn)-1

for i in range(j):
    if matrix_graph[i][j]!= '0':
        final_values[h] = matrix_graph[i][j]
        h = h + 1
for k in range(h):
    if word[word_len - 1] != final_values[k]:
        check_var = False
    else:
        check_var= True
        break

i = 0

for k in range(word_len):
    char = word[k]
    j = 0
    if check_var:
        if matrix_graph[i][j] == char:
            i = j
            j = 0
            check_var = True
    else:
        if j == len(vn) - 1:
            check_var = False
        else: j += 1

if check_var:
    print("Word is accepted with FA")
else:
    print("Word is NOT accepted with FA")