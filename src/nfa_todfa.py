class NFAState:
    def __init__(self, final_state=False):
        # initialize state with final state and transition 
        self.final_state = final_state
        self.state_transitions = {}

     # transition for a given character to the next state
    def define_transition(self, transition_char, next_state):
        self.state_transitions[transition_char] = next_state

    #Get the next state for a given transition character
    def get_next_state(self, transition_char):
        return self.state_transitions.get(transition_char)

class DFAState:
    _id_counter = 0  # counter for assigning unique IDs


    # initialize DFA state with unique ID and final state flag
    def __init__(self, is_final):
        
        self.id = DFAState._id_counter
        DFAState._id_counter += 1
        self.is_final = is_final
        self.transitions = {}

    # Transition for any given input character to a state
    def add_transition(self, input_char, state):
        self.transitions[input_char] = state

def regex_to_nfa(regex):
    if not regex:
        # Raise error if regex is empty
        raise ValueError("Empty regex is not allowed")

    start_state = NFAState()
    current_state = start_state

    for i, char in enumerate(regex):
        # Create next state and define transition for each character
        next_state = NFAState(final_state=(i == len(regex) - 1))
        current_state.define_transition(char, next_state)
        current_state = next_state

    return start_state

def simulate_dfa(dfa_start_state, input_string):
    current_state = dfa_start_state
    for char in input_string:
        if char in current_state.transitions:
            current_state = current_state.transitions[char]
        else:
            return False
    return current_state.is_final

 # initialize the dictionaries for DFA states and other states 
def nfa_to_dfa(start_nfa_state):
    dfa_states = {}
    processed_states = set()
    unprocessed_states = [start_nfa_state]

    while unprocessed_states:
        # Process each NFA state
        current_nfa_state = unprocessed_states.pop()
        if current_nfa_state in processed_states:
            # Skip if already processed
            continue

        # Make new DFA state if not already created
        if current_nfa_state not in dfa_states:
            dfa_state = DFAState(current_nfa_state.final_state)
            dfa_states[current_nfa_state] = dfa_state
          
        # Mark the NFA state as processed
        processed_states.add(current_nfa_state)

        # transitions for each character
        for char, next_nfa_state in current_nfa_state.state_transitions.items():
            
            #Makw a new DFA state if not existing
            if next_nfa_state not in dfa_states:

                dfa_states[next_nfa_state] = DFAState(next_nfa_state.final_state)
            # Add transition to DFA state
            dfa_states[current_nfa_state].add_transition(char, dfa_states[next_nfa_state])
            # Add to unprocessed states
            unprocessed_states.append(next_nfa_state)

    return dfa_states