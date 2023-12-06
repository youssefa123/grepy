class NFA:
    def __init__(self):
        
        self.transitions = {}  #transitions
        self.accept_states = set()  #Accept states

    def add_transition(self, start_state, input_char, end_state):
        # Add a transition from start state to end state on input_char
        if (start_state, input_char) not in self.transitions:
            self.transitions[(start_state, input_char)] = set()
        self.transitions[(start_state, input_char)].add(end_state)

    def set_accept_state(self, state):
        # Mark a state as an accept state
        self.accept_states.add(state)

    def is_accepted(self, input_string):
        # Checks to see if the input string is accepted by the NFA
        current_states = {0}  # Start state is 0

        for char in input_string:
            next_states = set()
            for state in current_states:
                if (state, char) in self.transitions:
                    next_states.update(self.transitions[(state, char)])
            current_states = next_states

        # Check if any of the current states is an accept state
        return bool(current_states & self.accept_states)


# NFA for the regular (0+1)*1
nfa = NFA()

# Adding transitions according to the regex (0+1)*1
nfa.add_transition(0, '0', 1)
nfa.add_transition(0, '1', 1)
nfa.add_transition(1, '0', 1)
nfa.add_transition(1, '1', 1)
nfa.add_transition(1, '1', 2)  # Transition to accept state on reading '1'

nfa.set_accept_state(2)

def test_file_with_nfa(file_path, nfa):
    results = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Remove newline and whitespace
            cleaned_line = line.strip()
            # Test with NFA
            results[cleaned_line] = nfa.is_accepted(cleaned_line)
    return results



file_path = '../data/inputFile2.txt'

results_from_file = test_file_with_nfa(file_path, nfa)
for line, result in results_from_file.items():
    print(f"'{line}': {'Accepted' if result else 'Rejected'}")