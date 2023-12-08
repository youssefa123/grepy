import sys

#Function that takes 1 parameter which is the file path 
def learn_alphabet(file_path):

    # Empty set called alphabet to store charachters 
    alphabet = set()
    
    #Open file with read only mode. 'r'
    with open(file_path, 'r', encoding='utf-8') as file:
        # Goes through each line in the file
        for line in file:
           
           # Update the alphabet set with characters from current line in file. 
           # Then trim whitespaces. 
            alphabet.update(line.strip())

    
    return alphabet

# Function to search for a word in the file and return a formatted string
def find_word_in_file(file_path, word):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if word in line:
                # Format the line by enclosing the word in brackets
                formatted_line = line.strip().replace(word, f'[{word}]')
                return formatted_line
    return "Word not found"

file_path = sys.argv[1]

# Executes the learn_alphabet function and stores the results in alphabet set
alphabet = learn_alphabet(file_path)

# Prints a sorted list of characters in the file 
print(f"Alphabet: {sorted(list(alphabet))}")
word_to_find = input("Enter a word to find: ")

formatted_output = find_word_in_file(file_path, word_to_find)
print(formatted_output)


