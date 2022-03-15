vn_unsorted = input("Input Vn elements (print space between letters)\n")
vn = vn_unsorted.split(" ")
vn.append(".")

print("VN = ", vn)

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

#Check if there could exist such word in FA
word = input ("Input word to verification:\n")

final_values = []
                        # check last pos in row in matrix, if exist -> final value
for i in range(len(vn)):
    if matrix_graph[i][-1]!= '0':
        final_values.append(matrix_graph[i][-1])
# print(final_values, 'final')
                        # check if first letter is start
if word[0] not in matrix_graph[0]:
    print("word not accepted with FA")
    quit()
                        # check if last letter is final
if word[-1] not in final_values:
    print("word not accepted with FA")
    quit()

i = 0
next_index = 0

for k in range(len(word)):
    char = word[k] #c f n m
    j = 0

    if char in matrix_graph[0]:
        next_index = matrix_graph[0].index(char)

    elif char in matrix_graph[next_index]:
        for i in range(len(vn)):
            if char == word[-1] and char in final_values:
                break

            if matrix_graph[next_index][i] == char:
                next_index = i
                break
    else:
        print("Word is NOT accepted with FA")
        quit()

print("Word is accepted with FA")
