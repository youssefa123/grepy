from graphviz import Digraph

class DFA:
    def __init__(self):
        #States 
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.start_state = None
        self.accept_states = set()

    def add_states(self, state):
        self.states.add(state)

    def add_alphabet(self, symbol):
        self.alphabet.add(symbol)

    def add_transition(self, start_state, input_char, end_state):
        self.transitions[(start_state, input_char)] = end_state

    def set_start_state(self, state):
        self.start_state = state

    def set_accept_state(self, state):
        self.accept_states.add(state)

    def is_accepted(self, input_string):
        current_state = self.start_state
        for char in input_string:
            if (current_state, char) in self.transitions:
                current_state = self.transitions[(current_state, char)]
            else:
                return False  # If no transition exists for the input char, reject the string
        return current_state in self.accept_states
    
# Function to test strings from the file with the DFA
def test_file_with_dfa(file_path, dfa):
    results = {} #set the result to an empty array 
    with open(file_path, 'r') as file: 
        for line in file: 
            cleaned_line = line.strip() #Strip white
            results[cleaned_line] = dfa.is_accepted(cleaned_line)
    return results

if __name__ == '__main__':
    dfa = DFA()

    #Using 0,1 for the regex (0+1)*1
    dfa.add_alphabet('0')
    dfa.add_alphabet('1')

    #DFA states 
    dfa.add_states(0)
    dfa.add_states(1)

    #Start state 
    dfa.set_start_state(0)

    #Accept states
    dfa.set_accept_state(0)  
    dfa.set_accept_state(1)

    #Transitions 
    dfa.add_transition(0, '0', 0)
    dfa.add_transition(0, '1', 1)
    dfa.add_transition(1, '0', 0)
    dfa.add_transition(1, '1', 1)

    file_path = '../data/inputFile2.txt'

    results_from_file = test_file_with_dfa(file_path, dfa)
    for line, result in results_from_file.items():
        print(f"'{line}': {'Accepted' if result else 'Rejected'}")

    dot = dfa.to_dot()
    output_path = '../output/dfa_output'

    # Save the DOT file
    dot.render(output_path, format='dot', view=False)

    # Print to confirm the DOT file has been generated
    print(f"The DOT representation has been saved to {output_path}.dot")