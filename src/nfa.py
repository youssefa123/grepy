from graphviz import Digraph

class NFA:
    def __init__(self):
        self.transitions = {}  # transitions
        self.accept_states = set()  # Accept states

    def add_transition(self, start_state, input_char, end_state):
        # Add a transition from start state to end state on input_char
        if (start_state, input_char) not in self.transitions:
            self.transitions[(start_state, input_char)] = set()
        self.transitions[(start_state, input_char)].add(end_state)

    def set_accept_state(self, state):
        
        self.accept_states.add(state)

    def is_accepted(self, input_string):
        
        current_states = {0}  # Start state is 0

        for char in input_string:
            next_states = set()
            for state in current_states:
                if (state, char) in self.transitions:
                    next_states.update(self.transitions[(state, char)])
            current_states = next_states

        # Check if any of the current states is an accept state
        return bool(current_states & self.accept_states)

    def to_dot(self):
        dot = Digraph()

        # Add all states
        all_states = set()
        for (start_state, _), end_states in self.transitions.items():
            all_states.add(start_state)
            all_states.update(end_states)

        for state in all_states:
            if state in self.accept_states:
                dot.node(str(state), shape="doublecircle")
            else:
                dot.node(str(state))

        # Add transitions
        for (start_state, input_char), end_states in self.transitions.items():
            for end_state in end_states:
                dot.edge(str(start_state), str(end_state), label=input_char)

        return dot

# Helper function to test strings from a file with the NFA
def test_file_with_nfa(file_path, nfa):
    results = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Remove newline and whitespace
            cleaned_line = line.strip()
            # Test with NFA
            results[cleaned_line] = nfa.is_accepted(cleaned_line)
    return results

# Main section to create the NFA for the regex (0+1)*1, test strings, and output DOT format
if __name__ == '__main__':
    nfa = NFA()

    # transitions  to the regex (0+1)*1
    nfa.add_transition(0, '0', 1)
    nfa.add_transition(0, '1', 1)
    nfa.add_transition(1, '0', 1)
    nfa.add_transition(1, '1', 1)
    nfa.add_transition(1, '1', 2)
    nfa.set_accept_state(1) #Fixed error
    nfa.set_accept_state(2)

    
    file_path = '../data/inputFile2.txt' 

    results_from_file = test_file_with_nfa(file_path, nfa)
    for line, result in results_from_file.items():
        print(f"'{line}': {'Accepted' if result else 'Rejected'}")

    # Generate and prints out the DOT format
    dot = nfa.to_dot()
    output_path = '../output/nfa_output'

    # Save the DOT file
    dot.render(output_path, format='dot', view=False)
    
    # Print to confirm the DOT file has been generated
    print(f"The DOT representation has been saved to {output_path}.dot")