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

    #index for checking through characters in Regex.
    i = 0
    
    # Iterate through the characters in the regex
    while i < len(regex):
        char = regex[i]

        #Check if the character is a '^'
        if char == '^':
            continue  # Skip '^' character
        
        # Check if the character is a '$'
        elif char == '$':
            # Add transitions from current states to the accept state
            for state in current_states:
                state.define_transition(None, accept_state)
        
        elif char == '|':
            # Create a new state for alternate paths
            new_state = NFAState()

            # transitions from current state to the new state
            for state in current_states:
                state.define_transition(None, new_state)
            current_states = [new_state]
            i += 1  # Skip the next character
        else:
            #if the character is not a special, make new states for each current state and add transitions
            new_states = []
            for state in current_states:
                new_state = NFAState(char)
                state.define_transition(char, new_state)
                new_states.append(new_state)
            current_states = new_states

        i += 1
    # transitions from the final current states to the accept state
    for state in current_states:
        state.define_transition(None, accept_state)

    return start_state


