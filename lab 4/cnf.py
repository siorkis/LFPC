freeGrammar = {
    "S": ["AC", "bA", "B", "aA"],
    "A": [".", "aS", "ABAb"],
    "B": ["a", "AbSA"],
    "C": ["abC"],
    "D": ["AB"]
}

Vn_list = ["A", "B", "C", "D", "S"]
Vt_list = ["a", "b"]
accesseble = ["S"]
print("Start Grammar:\n", freeGrammar)


def multiple_e_values(grammar, e_value_list, eps_list):
    mult_e_list = []
    for e in eps_list:
        for eValue in range(len(e_value_list)):
            if e_value_list[eValue].count(e) > 1:
                mult_e_list.append(e_value_list[eValue-1])
                mult_e_list.append(e_value_list[eValue])

    for z in range(len(mult_e_list)):
        values_to_add = []
        e_string = []
        if len(mult_e_list[z]) > 1: # ABAb | AbSA
            for char in mult_e_list[z]:
                e_string.append(char)
            x = 0
            while e_string.count(eps_list[0]) > 0:             
                buffer_e_string = e_string
                if buffer_e_string[x] in eps_list:
                    buffer_e_string.pop(x)
                    buf_string = ''.join([str(item) for item in buffer_e_string])
                    values_to_add.append(buf_string)
                x += 1
            for eps_value in values_to_add:
                if eps_value not in grammar[mult_e_list[z-1]]:
                    grammar[mult_e_list[z-1]].extend([eps_value])


#---------------PART 1---Replace E productions--------------------------
e_list = []
delete = False
# ----------Find epsilon values----------
for key, value in freeGrammar.items():
    for i in value:
        if i == ".":
            e_list.append(key)
# print(e_list, "- e_list")

# -----------Check if all connections with epsilon should be deleted-------------
for key in e_list:
    if len(freeGrammar[key]) > 1:
        delete = False
    else:
        delete = True

# ------------Create list with all values witch contain epsilon connection-------
eValueList = []
for key in freeGrammar:
    for value in freeGrammar[key]:
        if e_list[0] in value:                  
            eValueList.append(key)
            eValueList.append(value)
        if value == '.':
            freeGrammar[key].remove('.')

# print(eValueList, "- eValueList")


# ------------Add or Remove Epsilon connections-----------------------------------
for i in range(len(e_list)):
    for j in range(len(eValueList)):
        if j % 2:
            if eValueList[j].count(e_list[i]) == 1:
                string = eValueList[j].replace(e_list[i], "")

                if delete:
                    freeGrammar[eValueList[j - 1]].remove(eValueList[j])

                eValueList.remove(eValueList[j])
                eValueList.insert(j, string)
                freeGrammar[eValueList[j - 1]].append(string)

            elif eValueList[j].count(e_list[i]) > 1:
                if delete:
                    string = dict.fromkeys(map(ord, e_list[i]), None)
                    freeGrammar[eValueList[j-1]].remove(eValueList[j])
                    eValueList[j] = eValueList[j].translate(string)
                    freeGrammar[eValueList[j-1]].append(eValueList[j])
                else:
                    multiple_e_values(freeGrammar, eValueList, e_list)
    print("Replace Epsilon:\n", freeGrammar)



#----------------PART 2-----Renaming--------------------
key_to_delete = []
for key in freeGrammar:
    for value in freeGrammar[key]:
        if len(value) == 1 and value in Vn_list:
            values_to_add = freeGrammar[value]
            for value_add in values_to_add:
                if value_add not in freeGrammar[key]:
                    freeGrammar[key].extend([value_add])
            freeGrammar[key].remove(value)
            if value not in key_to_delete:
                key_to_delete.append(value)

print("Renaming:\n", freeGrammar)

#------------PART 3-------Non-Productive------------------

productive = []
non_productive = []
count = 0

while count != 2:
    for key in freeGrammar:
        for value in freeGrammar[key]:
            if len(value) == 1 and value not in Vn_list and value != '.' and key not in productive:
                productive.append(key)

            if count == 1:
                for char in value:
                    if char in Vn_list and char in productive and key not in productive:
                        productive.append(key)
    count += 1

for vn in Vn_list:
    if vn not in productive:
        non_productive.append(vn)

for key in non_productive:
    del freeGrammar[key]

print("Delete Non-Productive:\n", freeGrammar)


#------------------PART 4----------unacceseble------
for vn in Vn_list:
    for key in freeGrammar:
        for value in freeGrammar[key]:
            if vn in value and key in accesseble and vn not in accesseble:
                accesseble.append(vn)

for key in Vn_list:
    if key in freeGrammar and key not in accesseble:
        del freeGrammar[key]

for key in accesseble:
    if key not in freeGrammar:
        accesseble.remove(key)

for key in freeGrammar:
    for value in freeGrammar[key]:
        for char in value:
            if char not in Vt_list and char not in accesseble:
                freeGrammar[key].remove(value)


print("Exclude unaccessble transactions:\n", freeGrammar)


#--------------------PART 5-----------CNF---------
map_for_cnf = {}
cnf = {}
for key in freeGrammar:
    cnf[key] = []

index_list_y = []
index_list_x = []
index_list = []
cnf_value = ''
index = 0
bivalue = []
bivalue_cnf = []

first_rule = True

for key in freeGrammar:
    for value in freeGrammar[key]:
        # Vt
        if len(value) == 1:
            cnf[key].append(value)
        # Vn+Vn
        if len(value) == 2:
            for char in value:
                bivalue.append(char)

            for char in Vt_list:
                if char in bivalue:
                    first_rule = False

            if first_rule:
                cnf[key].append(value)
                break

            bivalue = []
            first_rule = True
        # Vt+Vn / Vt+Vt
        if len(value) == 2:
            for char in value:
                bivalue.append(char)
                if char in Vt_list:
                    if char not in map_for_cnf:
                        index = 1
                        end = False
                        while not end:
                            if index in index_list_x:
                                index += 1
                            else:
                                end = True
                        index_list_x.append(index)
                        cnf_value += "X" + str(index)
                        map_for_cnf[char] = cnf_value
            end = False
            # while not end:
            for char in bivalue:
                if char in Vt_list:
                    end = True
                    ind = bivalue.index(char)
                    if cnf_value == '':
                        bivalue[ind] = map_for_cnf[char]
                    else:
                        bivalue[ind] = cnf_value

            cnf_value = ''
            for char in bivalue:
                cnf_value += char
            cnf[key].append(cnf_value)

            cnf_value = ''
            bivalue = []

cnf_value_final = ''
for key in freeGrammar:
    for value in freeGrammar[key]:
        if len(value) >= 3:
            left = len(value) // 2
            right = len(value) - left

            for char in value:
                bivalue.append(char)
            left_part = []
            right_part = []
            for i in range(left):
                left_part.append(bivalue[i])

            for i in range(left, len(value)):
                right_part.append(bivalue[i])

            for char in left_part:
                cnf_value += char
            left_part = [cnf_value]

            cnf_value = ''
            for char in right_part:
                cnf_value += char
            right_part = [cnf_value]

            final = [left_part[0], right_part[0]]

            for part in final:
                cnf_value = ''
                if part not in map_for_cnf:
                    index = 1
                    end = False
                    while not end:
                        if index in index_list_y:
                            index += 1
                        else:
                            end = True
                    index_list_y.append(index)
                    cnf_value += "Y" + str(index)
                    map_for_cnf[part] = cnf_value

            for part in final:
                cnf_value_final += map_for_cnf[part]

            cnf[key].append(cnf_value_final)

            bivalue = []
            cnf_value = ''
            cnf_value_final = ''

print("------------------------------------------------------------")
print("Final CNF:\n", cnf)
print("Map for CNF:\n", map_for_cnf)
