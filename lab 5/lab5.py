freeGrammar = {
    "S": ["dB"],
    "A": ["a", "aA"],
    "B": ["c", "CcB"],
    "C": ["bA"]
}

freeGrammar_to_convert = {
    "S": ['d', 'B'],
    "A": ["a","|", "a", "A"],
    "B": ["c", "|", "C", "c", "B"],
    "C": ["b", "A"]
}

Vn_list = ["A", "B", "C", "S"]
Vt_list = ["a", "b", "d", "c"]

# left factoring
string_to_compare = ''
final_compare = ''
left_factor = []
key_prime = ''
for key in freeGrammar:
    if len(freeGrammar[key]) > 1:
        string_to_compare = ''
        string_to_compare += freeGrammar[key][0][0]
        match_count = 0
        for value in freeGrammar[key]:
            if value[0] == string_to_compare:
                match_count += 1

            if final_compare == '':
                if string_to_compare in value and string_to_compare[0] == value[0]:
                    left_factor.append(value)

        if match_count > 1:
            key_prime = key + "'"
            final_compare = string_to_compare
            left_factor.insert(0, key)

array_to_add = []
for i in range(1, len(left_factor)):

    string_to_add = left_factor[i].replace(final_compare, '')
    if left_factor[i] in freeGrammar[key_prime[0]]:
        freeGrammar[key_prime[0]].remove(left_factor[i])
    if string_to_add == '':
        string_to_add = '.'
    array_to_add.append(string_to_add)

freeGrammar[key_prime] = array_to_add
freeGrammar[key_prime[0]].append(final_compare + key_prime)

print(freeGrammar, "frg")

# first
first_dic = {
    "S": [],
    "A": [],
    "B": [],
    "C": [],
    "A'": []
}


def first(key_f, key_to_add, frg, first_dict):
    value_f = frg[key_f]

    # 1st rule
    if value_f[0][0] in Vt_list and value_f[0][0] not in first_dict[key_to_add]:
        first_dict[key_to_add].append(value_f[0][0])

    # 2nd rule
    elif value_f == '.':
        first_dict[key_to_add].append(value_f)

for key_1 in first_dic:
    for value_1 in freeGrammar[key_1]:
        for char_1 in value_1:
            if char_1 in Vt_list or char_1 == '.':
                if char_1 in first_dic[key_1]:
                    break
                first_dic[key_1].append(char_1)
                break
            else:
                first(char_1, key_1, freeGrammar, first_dic)

print(first_dic, "first")

# follow

follow_dic = {
    "S" : [],
    "A" : [],
    "B" : [],
    "C" : [],
    "A'": []
}

for key in freeGrammar:
    for value in freeGrammar[key]:
        if key == "S":
            follow_dic[key].append("$")
            for char in value:
                if char in Vn_list:
                    follow_dic[char].append("$")

        if len(value) > 1 and key != 'S':
            if value[-1] == "'":
                continue

            for i in range(len(value)):
                if value[i] in Vt_list and value[i-1] in Vn_list:
                    if key != value[-1]:
                        follow_dic[value[-1]].append(follow_dic[key][0])
                    else:
                        follow_dic[value[i-1]].append(value[i])

for key in freeGrammar:
    for value in freeGrammar[key]:
        if key[-1] == "'":
            if value != '.':
                follow_dic[key].append(follow_dic[value][0])

print(follow_dic, "follow")

# prediction
# how to generate table: use for rows keys from FRG, for columns use Vt_list + $
table = [["", "d", "a", "c", "b", "$"],
         ["S", "", "", "", "", ""],
         ["A", "", "", "", "", ""],
         ["A'", "", "", "", "", ""],
         ["B", "", "", "", "", ""],
         ["C", "", "", "", "", ""]
        ]


def check_first(key_f, value_f, frg):
    # 1st rule
    if value_f[0] in Vt_list:
        return value_f[0]

    # 2nd rule
    elif value_f == '.':
        return follow_dic[key_f][0]

    if value_f[0] not in Vt_list and len(value_f) > 1:
        new_value_f = frg[value_f[0]][0]
        check_first(key_f, new_value_f, frg)
        return new_value_f[0]

    if value_f[0] not in Vt_list and len(value_f) == 1 and value_f != '.':
        new_key_f = value_f[0]
        new_value_f = frg[new_key_f][0]
        check_first(new_key_f, new_value_f, frg)
        return new_value_f[0]


for key in freeGrammar:
    for value in freeGrammar[key]:
        column = check_first(key, value, freeGrammar)
        index = table[0].index(column)
        for i in range(6):
            if table[i][0] == key:
                table[i][index] = key + '->' + value
                continue


print("")
print("-------------predict---------table-------------")

for i in range(6):
    for j in range(6):
        print(table[i][j], end='\t\t')
    print('')

print("")

# string validation

# word_to_validate = str(input())

word_to_validate = "dbacbaaa$"

action = freeGrammar["S"][0]

# word_to_validate = 'cbaaa$'
# action = "A'cB"

def validate(action_set, word, frg):

    for char in action_set:

        if len(action_set) > 2 and action_set[0:2][1] == "'":
            buffer_set = action_set[2:]
            action_set = frg[action_set[0:2]][1] + buffer_set
            return action_set, word

        if char in Vt_list and char == word[0]:
            word = word[1:]
            action_set = action_set[1:]
            return action_set, word
        elif char in Vt_list and char != word[0]:
            action_set = action_set[3:]
            return action_set, word

        if char not in Vt_list:

            if len(action_set) > 1:
                buffer_set = action_set[1:]
            else:
                buffer_set = ''

            if len(frg[action_set[0]]) == 1:
                action_set = frg[action_set[0]][0] + buffer_set
            else:
                action_set = frg[action_set[0]][1] + buffer_set

            return action_set, word

print("-------------------------validation---of--", word_to_validate, "------------------")

while len(word_to_validate) != 1:
    action, word_to_validate = validate(action, word_to_validate, freeGrammar)
    validate(action, word_to_validate, freeGrammar)
    print(action, "action")
    print(word_to_validate, "word")
    print('')
