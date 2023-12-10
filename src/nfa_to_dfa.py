from regexTonfa import NFAState, regex_to_nfa, simulate_nfa

# DFA state class with epsilon closure and transitions.
class DFAState:
    def __init__(self, nfa_states):
        self.nfa_states = frozenset(nfa_states)  # store nfa states as a frozen set becuase the elements cannot be modified after created. This is good for making DFA's 
        self.is_final = any(state.final_state for state in self.nfa_states)  # Check if any NFA state is final
        self.transitions = {}  # transitions

    def add_transition(self, input_char, state):
        self.transitions[input_char] = state  # Add a transition to the state

    def __hash__(self):
        return hash(self.nfa_states)  # Define hash for state comparison

    def __eq__(self, other):
        return self.nfa_states == other.nfa_states  # Define equality for state comparison
