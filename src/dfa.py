from graphviz import Digraph

class DFA:
    def __init__(self):
        # States
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
            if char not in self.alphabet:
                return False  # Rejects strings with characters not in the alphabet (0, 1)
            if (current_state, char) in self.transitions:
                current_state = self.transitions[(current_state, char)]
            else:
                return False  
        return current_state in self.accept_states
    
    def to_dot(self):
        dot = Digraph()
        dot.node('', shape="plaintext")
        for state in self.states:
            if state in self.accept_states:
                dot.node(str(state), shape="doublecircle")
            else:
                dot.node(str(state), shape="circle")
        dot.edge('', str(self.start_state), label="start")  # This adds an arrow to indicate the start state
        for (start_state, input_char), end_state in self.transitions.items():
            dot.edge(str(start_state), str(end_state), label=input_char)
        return dot
    
# Function to test strings from the file with the DFA
def test_file_with_dfa(file_path, dfa):
    results = {}
    with open(file_path, 'r') as file:
        for line in file:
            cleaned_line = line.strip()
            if dfa.is_accepted(cleaned_line):
                results[cleaned_line] = "Accepted"
            else:
                results[cleaned_line] = "Rejected: Does not match the regex (0+1)*1"
    return results

def main 
if __name__ == '__main__':
    dfa = DFA()

    # Using 0,1 for the regex (0+1)*1
    dfa.add_alphabet('0')
    dfa.add_alphabet('1')

    # DFA states 
    dfa.add_states(0)
    dfa.add_states(1)

    # Start state 
    dfa.set_start_state(0)

    # Accept states
    dfa.set_accept_state(1)  # Only state 1 is an accepting state

    # Transitions 
    dfa.add_transition(0, '0', 0)
    dfa.add_transition(0, '1', 1)
    dfa.add_transition(1, '0', 1)
    dfa.add_transition(1, '1', 1)

    file_path = '../data/inputFile2.txt'

    results_from_file = test_file_with_dfa(file_path, dfa)
    for line, result in results_from_file.items():
        print(f"'{line}': {result}") 

    dot = dfa.to_dot()
    output_path = '../output/dfa_output'

    # Save the DOT file
    dot.render(output_path, format='dot', view=False)

    # Print to confirm the DOT file has been generated
    print(f"The DOT representation has been saved to {output_path}.dot")
