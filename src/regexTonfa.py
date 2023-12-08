class NFAState:
    def __init__(self, identifier=None, final_state=False):
        self.identifier = identifier  # Identifier for the state
        self.final_state = final_state  # indicates if it's a final state
        self.state_transitions = {}  # holds the state transitions in an empty array 

    def define_transition(self, transition_char, next_state):
        # transition for a character
        self.state_transitions.setdefault(transition_char, set()).add(next_state)
    
    def compute_epsilon_closure(self):
        closure_set = {self}  
        search_stack = [self]  

        while search_stack:
            current_state = search_stack.pop()  # Retrieve a state from the stack
            # Process epsilon transitions (None)
            for next_state in current_state.state_transitions.get(None, []):
                if next_state not in closure_set:
                    closure_set.add(next_state)  # Add state to closure set
                    search_stack.append(next_state)  

        return closure_set  

#create NFA from regex Initialized start, current and accept state
def regex_to_nfa(regex):
    start_state = NFAState("start")
    current_state = start_state
    state_stack = []  # Stack to manage groups
    group_start_stack = []  # Stack to remember the start state of the group
    accept_state = NFAState("accept", final_state=True)

    i = 0
    while i < len(regex):
        char = regex[i]

        if char == '^':
            i += 1  # Skip '^' character
            continue

        elif char == '*':
            if group_start_stack:
                group_start_state = group_start_stack.pop()
                loopback_state = NFAState()
                skip_state = NFAState()

                # Create a loopback for zero or more occurrences
                group_start_state.define_transition(None, loopback_state)
                loopback_state.define_transition(None, skip_state)
                loopback_state.define_transition(None, group_start_state)

                current_state.define_transition(None, skip_state)
                current_state = skip_state
            else:
                # Handle * for non-grouped characters
                # Here, you would handle the * quantifier for individual characters
                pass
            i += 1
            continue

        elif char == '(':
            state_stack.append(current_state)
            group_start_state = NFAState()
            current_state.define_transition(None, group_start_state)
            current_state = group_start_state
            group_start_stack.append(group_start_state)

        elif char == ')':
            if state_stack:
                group_end_state = NFAState()
                current_state.define_transition(None, group_end_state)
                current_state = state_stack.pop()
                current_state.define_transition(None, group_end_state)
                current_state = group_end_state
            else:
                raise ValueError("Unbalanced parentheses in regex")

        elif i + 1 < len(regex) and regex[i + 1] == '+':
            new_state = NFAState(char)
            current_state.define_transition(char, new_state)
            new_state.define_transition(None, current_state)
            current_state = new_state
            i += 2
            continue

        elif char == '$':
            current_state.define_transition(None, accept_state)

        elif char == '|':
            # Handling for alternation (|) can be added here
            pass

        else:
            new_state = NFAState(char)
            current_state.define_transition(char, new_state)
            current_state = new_state

        i += 1

    if not state_stack:
        current_state.define_transition(None, accept_state)
    else:
        raise ValueError("Unclosed parenthesis in regex")

    return start_state


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
    regex = input("Enter a REGEX: ")
    nfa = regex_to_nfa(regex)

    test_inputs = ["ab", 'sss']  #  TEST it here
    for test_input in test_inputs:
        result = "Accepted" if simulate_nfa(nfa, test_input) else "Rejected"
        print(f"Input: {test_input}, Result: {result}")

if __name__ == "__main__":
    main()