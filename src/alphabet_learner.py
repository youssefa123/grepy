import sys

#Function that takes 1 parameter which is the file path 
def learn_alphabet(file_path):

    # Empty set called alphabet to store charachters 
    alphabet = set() 
    
    #Open file with read only mode. 'r'
    with open(file_path, 'r', encoding='utf-8') as file:
        # Goes through each line in the file
        for line in file:
           
           # Update the alphabet set with characters from current line in file 
           # Then trim whitespaces 
            alphabet.update(line.strip())

    # Return the complete set of unique characters, like showing the completed puzzle.
    return alphabet

file_path = sys.argv[1]

# Executes the learn_alphabet function and stores the results in alphabet set
alphabet = learn_alphabet(file_path)

# Prints a sorted list of characters in the file 
print(f"Alphabet: {sorted(list(alphabet))}")

