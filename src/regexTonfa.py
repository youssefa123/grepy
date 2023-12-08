class NFAState:
    def __init__(self, identifier=None, final_state=False):
        self.identifier = identifier  # Identifier for the state
        self.final_state = final_state  # indicates if it's a final state
        self.state_transitions = {}  # holds the state transitions in an empty array 

    def define_transition(self, transition_char, next_state):
        # transition for a character
        self.state_transitions.setdefault(transition_char, set()).add(next_state)
    
    def compute_epsilon_closure(self):
        closure_set = {self}  # Initialize closure set with the state itself
        search_stack = [self]  # Stack for depth-first search in the closure set

        while search_stack:
            current_state = search_stack.pop()  # Retrieve a state from the stack
            # Process epsilon transitions (None)
            for next_state in current_state.state_transitions.get(None, []):
                if next_state not in closure_set:
                    closure_set.add(next_state)  # Add state to closure set
                    search_stack.append(next_state)  # Append state for further exploration

        return closure_set  # Return the computed epsilon closure
    
#create NFA from regex Initialized start, current and accept state
def regex_to_nfa(regex):
    start_state = NFAState("start")
    current_states = [start_state]
    accept_state = NFAState("accept", final_state=True)

    i = 0
    while i < len(regex):
        char = regex[i]

        if char == '^':
            i += 1  # Skip '^' character and continue
            continue

        elif char == '$':
            for state in current_states:
                state.define_transition(None, accept_state)

        elif char == '|':
            new_state = NFAState()
            for state in current_states:
                state.define_transition(None, new_state)
            current_states = [new_state]
            i += 1  # Skip the next character

        else:
            new_states = []
            for state in current_states:
                new_state = NFAState(char)
                state.define_transition(char, new_state)
                new_states.append(new_state)
            current_states = new_states

        i += 1

    for state in current_states:
        state.define_transition(None, accept_state)

    return start_state  # This should be outside the while loop


def simulate_nfa(nfa, test_input):
    current_states = nfa.compute_epsilon_closure()
    for char in test_input:
        next_states = set()
        for state in current_states:
            next_states.update(state.state_transitions.get(char, []))
        current_states = set()
        for state in next_states:
            current_states.update(state.compute_epsilon_closure())

    return any(state.final_state for state in current_states)

def main():
    regex = input("Enter a regular expression: ")
    nfa = regex_to_nfa(regex)

    test_inputs = ["ab"]  # Sample test inputs
    for test_input in test_inputs:
        result = "Accepted" if simulate_nfa(nfa, test_input) else "Rejected"
        print(f"Input: {test_input}, Result: {result}")

if __name__ == "__main__":
    main()