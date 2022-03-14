
states = ['q0', 'q1', 'q2', 'q3', 'q4']
nr_states = 5
#--------input states----------
# a = int(input("Enter number of states : "))
# print("Define the states")
# # q0, q1, q2, q3, q4
#
# for i in range(0, a):
#     state = input()
#     states.append(state)  # ['q0', 'q1', 'q2', 'q3', 'q4']
#
# # print(states_unsorted)
# nr_states = len(states)
#------------------------------

path = ['a.', 'b.']
nr_path = 2
# #------------input path-------------------
# b = int(input("Enter number of path : "))
# print("Define the path")
#
# for i in range(0, b):
#     element = input()
#     path.append(element)  # a, b
# # print(path)
# nr_path = len(path)
# #-------------------------------------

final = ['q4']
nr_final = 1
# #------------input final--------------------
# c = int(input("Enter number of final states : "))
# print("Define the final")
#
# for i in range(0, b):
#     element_final = input()
#     final.append(element_final)  # q4
# # print(final)
# nr_final = len(final)
# #-------------------------------------------


# number_of_states = int(input("Enter the number of states"))


# for i in range(nr_states):
#     nfa.append([states[i]])

# print(nfa)
lent=3
ways = [['q0', 'a', 'q1'], ['q1', 'b', 'q1'], ['q1', 'b', 'q2'], ['q2', 'b', 'q3'], ['q3', 'a', 'q1'], ['q2', 'a', 'q4']]
blank = ' '

#-----------------------------------NFA-----------------------------
nfa = [['S.']]
# head of NFA
for i in range(nr_path):
    nfa[0].append(path[i])
    if nr_path != (i + 1):
        nfa[0].append('/')

existence = False

for state in states:
    for i in range(len(ways)):
        # print(nfa)
        if state == ways[i][0]:
            if state not in nfa[-1][0]:
                nfa.append([state])
                nfa[-1].append('/')
# ways [['q0', 'a', 'q1'], ['q1', 'b', 'q1'], ['q1', 'b', 'q2'], ['q2', 'b', 'q3'], ['q3', 'a', 'q1'], ['q2', 'a', 'q4']]
            ad_z = 0
            if ways[i][1] == 'a':
                for z in range(len(nfa[-1])):
                    if nfa[-1][z+ad_z] == "/":
                        nfa[-1].insert(z, ways[i][2])
                        ad_z += 1
            if ways[i][1] == 'b':
                for z in range(len(nfa[-1])):
                    if nfa[-1][z+ad_z] == "/":
                        nfa[-1].insert(z+1, ways[i][2])
                        ad_z += 1

    # no connection lines
    for i in range(len(nfa)):
        if state == nfa[i][0]:
            existence = True
    if not existence:
        nfa.append([state])
        for j in range(nr_path):
            if nr_path != (j + 1):
                nfa[-1].append('/')
    existence = False
#-------------------------------------------------------------
nfa_print = nfa
print("------------NFA:------------")
for line in nfa:
    for i in range(len(line)):
        if line.index('/') == 1:
            line.insert(1, '  ')
    print(line)


def new_line(array, dfa_array, heads_dfa):
    new_a = []
    new_b = []
    new_dfa_line = []
    string = ''

    # print('start array', array)
    for elem in array:
        for head in range(len(nfa)):
            if nfa[head][0] == elem:
                for element in range(1, len(nfa[head])):
                    if nfa[head][element] == '/':
                        for n_a in range(1, element):
                            if nfa[head][n_a] != '/':
                                new_a.append(nfa[head][n_a])
                        for n_b in range(element, len(nfa[head])):
                            if nfa[head][n_b] != '/':
                                new_b.append(nfa[head][n_b])
    # print("new-a", new_a)
    # print("new-b", new_b)

    for conc in array:
        string += conc

    new_dfa_line.append(string)

    for i in new_a:
        new_dfa_line.append(i)

    new_dfa_line.append('/')

    for i in new_b:
        new_dfa_line.append(i)

    if string not in heads_dfa:
        heads_dfa.append(string)
        # print("new dfa line - ", new_dfa_line)
        dfa_array.append(new_dfa_line)
#-----------------------DFA------------------------
dfa = [['S.']]
dfa_a = []
dfa_b = []
dfa_heads = []

# head of DFA
for i in range(nr_path):
    dfa[0].append(path[i])
    if nr_path != (i + 1):
        dfa[0].append('/')

end = False
row = 0
slash_index = 0
heads_compare = -1
heads_number = len(dfa_heads)

while not end:
    if len(dfa) == 1:
        dfa.append(nfa[1])
        dfa_heads.append(nfa[1][0])
    else:
        for i in range(len(dfa[row])): # get position of '/'
            if dfa[row][i] == '/':
                slash_index = dfa[row].index('/')

        # get elements and check for existing
        for i in range(1, slash_index): # get A elements
            if dfa[row][i] != "  " and dfa[row][i] != "/":
                dfa_a.append(dfa[row][i])
            # print('dfa_a:', dfa_a)

        if len(dfa_a) <= 1:
            for line in dfa:
                for i in range(len(dfa)):
                    for a in dfa_a:
                        if a not in dfa_heads:
                            dfa.append([a]) # add head from a column
                            dfa_heads.append(a)
                            # print('dfa_heads:', dfa_heads)
                            for j in range(len(nfa)):  # add line from NFA with this head
                                if nfa[j][0] == a:
                                    for k in range(1, len(nfa[j])):
                                        dfa[-1].append(nfa[j][k])
        else:
            new_line(dfa_a, dfa, dfa_heads)

        if (len(dfa[row]) - slash_index) > 1:
            for i in range(slash_index, len(dfa[row])): # get B elements
                if dfa[row][i] != "  " and dfa[row][i] != "/":
                    dfa_b.append(dfa[row][i])
                # print('dfa_b:', dfa_b)

            if len(dfa_b) <= 1:
                for line in dfa:
                    for i in range(len(dfa)):
                        for b in dfa_b:
                            if b not in dfa_heads:
                                dfa.append([b])  # add head from a column
                                dfa_heads.append(b)
                                # print('dfa_heads:', dfa_heads)
                                for j in range(len(nfa)):  # add line from NFA with this head
                                    if nfa[j][0] == b:
                                        for k in range(1, len(nfa[j])):
                                            dfa[-1].append(nfa[j][k])
            else:
                new_line(dfa_b, dfa, dfa_heads)
    dfa_a = []
    dfa_b = []
    heads_number = len(dfa_heads)
    heads_compare += 1

    if heads_compare == heads_number:
        end = True

    row += 1
#---------------------------------------------------

dfa_print = dfa
print("------------DFA:------------")
for line in dfa_print:
    if line[0] != "S.":
        slash_index = line.index('/')
        conc_a = ''
        conc_b = ''

        if slash_index > 2:
            for j in range(1, slash_index):
                if line[j] != '  ' and line[j] != '/':
                    conc_a += line[j]
            for jj in range(1, slash_index):
                line.pop(1)
            line.insert(1, conc_a)

        slash_index = line.index('/')

        if line[-1] != "/":
            for k in range(slash_index, len(line)):
                if line[k] != '  ' and line[k] != '/':
                    conc_b += line[k]
            for kk in range(slash_index+1, len(line)):
                line.pop(-1)
            line.append(conc_b)
    print(line)
# print("final heads - ", dfa_heads)
