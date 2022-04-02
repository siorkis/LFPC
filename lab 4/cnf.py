freeGrammar = {
    "S": ["AC", "bA", "B", "aA"],
    "A": [".", "aS", "ABAb"],
    "B": ["a", "AbSA"],
    "C": ["abC"],
    "D": ["AB"]
}

Vn_list = ["A", "B", "C", "D", "S", "E"]
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
            while e_string.count(eps_list[0]) > 0:             #TO DO: iterate all eps values (now working only with 2)
                buffer_e_string = e_string                     # not correctly deleting: ABAb -> bAb, Bb | missing ABb
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
        if e_list[0] in value:                  # TO DO: iterate all values from e_list
            eValueList.append(key)
            eValueList.append(value)
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

# for key in key_to_delete:
#     del freeGrammar[key]

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

print("Exclude unaccessble transactions:\n", freeGrammar)


#--------------------PART 5-----------CNF---------
