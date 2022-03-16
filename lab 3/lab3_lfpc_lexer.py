punctuationTokens = {
    ".": "DOT",
    ",": "COMMA",
    ";": "SEMICOLON",
    ":": "COLON",
    "{": "LBRACE",
    "}": "RBRACE",
    "(": "LPAREN",
    ")": "RPAREN",
    "[": "LBRACKET",
    "]": "RBRACKET",
}

mathTokens = {
    "+": "PLUS",
    "-": "MINUS",
    "/": "SLASH",
    "%": "MOD",
    "*": "MULT",
}

logicTokens = {
    "<": "SMALLER",
    ">": "BIGGER",
    "=": "EQUAL",
    "!": "NEGATION",
    "!=": "NEGATION_EQUAL",
    "==": 'EQUAL_EQUAL',
    ">=": "BIGGER_EQUAL",
    "<=": "SMALLER_EQUAL",
    "true": "TRUE",
    "false": "FALSE",
}

dataTypeTokens = {
    "int": "INT",
    "string": "STRING",
    "bool": "BOOLEAN",
}

keywordTokens = {
    "for": "FOR",
    "while": "WHILE",
    "do": "DO",
    "if": "IF",
    "else": "ELSE",
    "elif": "ELIF",
    "function": "FUNCTION",
    "return": "RETURN",
    "and": "AND",
    "or": "OR",
    "print": "PRINT"
}

# Using readline()
file1 = open('C:\lfpc\lab 3\input.txt', 'r')
storage_final = ''
storage_pair = ''

passing_count = 0

#keys
punctuation_keys = punctuationTokens.keys()
math_keys = mathTokens.keys()
logic_keys = logicTokens.keys()
dataType_keys = dataTypeTokens.keys()
keyword_keys = keywordTokens.keys()

while True:
    # Get next line from file
    line = file1.readline()
    storage_local = ''
    # if line is empty
    # end of file is reached
    if not line:
        break

    for char in line:

        if passing_count > 0:
            passing_count -= 1
            continue

        # searching for some text
        if char == "\"":
            x = line.index("\"")
            y = line.rindex("\"")
            storage_final += 'TEXT:\t'

            for i in range(x+1, y):
                storage_final += line[i]
                passing_count += 1

            # for ending "
            passing_count += 1
            storage_final += '\n'
            continue

        # storage_local = sum
        if (char == " " or char == "." or char == "(" or char == ")" or char == "," or char == "{" or char == '}' or \
           char == ':' or char == ';' or char == '[' or char == ']' or char == "+" or char == '-' or char == '/' or \
           char == "%" or char == '*' or char == '<' or char == '>' or char == '!=' or char == '==' or char == '<=' or \
           char == '>=' or char == '\t' or char == '\n'):

            if storage_local in punctuation_keys:
                storage_final += punctuationTokens[storage_local]
                storage_final += "\t" + storage_local + "\n"
                storage_local = ''

            elif storage_local in math_keys:
                storage_final += mathTokens[storage_local]
                storage_final += "\t" + storage_local + "\n"
                storage_local = ''

            elif storage_local in logic_keys:
                storage_final += logicTokens[storage_local]
                storage_final += "\t" + storage_local + "\n"
                storage_pair = storage_local
                storage_local = ''

            elif storage_local in dataType_keys:
                storage_final += dataTypeTokens[storage_local]
                storage_final += "\t" + storage_local + "\n"
                storage_local = ''

            elif storage_local in keyword_keys:
                storage_final += keywordTokens[storage_local]
                storage_final += "\t" + storage_local + "\n"
                storage_pair = storage_local
                storage_local = ''

            elif storage_local in punctuation_keys:
                storage_final += punctuationTokens[storage_local]
                storage_final += "\t" + storage_local + "\n"
                storage_local = ''

            elif storage_local in math_keys:
                storage_final += mathTokens[storage_local]
                storage_final += "\t" + storage_local + "\n"
                storage_local = ''

            elif storage_local in logic_keys:
                storage_final += logicTokens[storage_local]
                storage_final += "\t" + storage_local + "\n"
                storage_local = ''

            else:
                if storage_pair == '=' and storage_local.isnumeric():
                    storage_final += "VALUE\t" + storage_local + "\n"
                    storage_pair = ''
                    storage_local = ''

                if storage_pair == 'function':
                    storage_final += "FUNCTION NAME\t" + storage_local + "\n"
                    storage_pair = ''
                    storage_local = ''
                
                if storage_local.isnumeric():
                    storage_final += "INT\t" + storage_local + "\n"
                    storage_local = ''

                if storage_local != '':
                    storage_final += "IDENTIFIER\t" + storage_local + "\n"
                    storage_local = ''


            if char == "{":
                storage_final += punctuationTokens["{"]
                storage_final += "\t {"
                storage_final += "\n"
            elif char == "}":
                storage_final += punctuationTokens["}"]
                storage_final += "\t }"
                storage_final += "\n"
            elif char == ")":
                storage_final += punctuationTokens[")"]
                storage_final += "\t )"
                storage_final += "\n"
            elif char == "(":
                storage_final += punctuationTokens["("]
                storage_final += "\t ("
                storage_final += "\n"

        if char != " " and char != '(' and char != ')' and char != '{' and char != '}':
            storage_local += char

        # storage_local += char

    print(line.strip())


file_output = open("C:\lfpc\lab 3\output.txt", "r+")
file_output.seek(0)
# to erase all data
file_output.truncate()
file_output.close()

file_output = open('C:\lfpc\lab 3\output.txt', 'a')
file1 = open('C:\lfpc\lab 3\input.txt', 'r')
while True:
    # Get next line from file
    line = file1.readline()
    # if line is empty
    # end of file is reached
    if not line:
        storage_final += "EOF"
        storage_final += "\t''"
        storage_final += "\n"
        break
    file_output.write(line)

print('\n')
print(storage_final)
file1.close()

file_output.write('\n------------------------------------------------\n')
file_output.write(storage_final)
