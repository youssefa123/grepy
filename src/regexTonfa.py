class NFAState:
    def __init__(self, identifier=None, final_state=False):
        self.identifier = identifier  # Identifier for the state
        self.final_state = final_state  # indicates if it's a final state
        self.state_transitions = {}  # holds the state transitions in an empty array 

    def define_transition(self, transition_char, next_state):
        # transition for a character
        self.state_transitions.setdefault(transition_char, set()).add(next_state)
    
    
#create NFA from regex Initialized start, current and accept state
def regex_to_nfa(regex):
    start_state = NFAState("start")
    current_states = [start_state]
    accept_state = NFAState("accept", final_state=True)

