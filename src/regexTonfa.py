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

#create NFA from regex 
def regex_to_nfa(regex):
    start_state = NFAState("start")  
    current_state = start_state
    state_stack = []  # Stack to manage '('
    group_start_stack = [] 
    accept_state = NFAState("accept", final_state=True)  # Accepting state of the NFA

    i = 0
    while i < len(regex):
        char = regex[i]

        if char == '^':
            i += 1  # 
            continue

        #special character logic
        # Handle the Kleene star (zero or more occurrences)
        elif char == '*':
            if state_stack:
                # Inside a group
                group_start_state = state_stack[-1]
                loop_state = NFAState()
                skip_state = NFAState()

                # Loop back for multiple occurrences
                group_start_state.define_transition(None, loop_state)
                loop_state.define_transition(None, group_start_state)

                # Skip the group for zero occurrences
                loop_state.define_transition(None, skip_state)

                # Connect the current state to the skip state
                current_state.define_transition(None, skip_state)
                current_state = skip_state
            elif current_state:
                i += 1
            continue

        elif char == '+':
            if current_state:
                plus_state = NFAState()
                if state_stack:
                    # gets back the most recently added group start state from the stack
                    group_start_state = state_stack[-1]
                    #connects the group start state to the new state for one or more occurrences
                    group_start_state.define_transition(None, plus_state)
                    plus_state.define_transition(None, group_start_state)
                else:
                    previous_state = start_state if current_state == start_state else current_state
                    #connects the previous state to the new state for one or more occurrences
                    previous_state.define_transition(None, plus_state)
                    plus_state.define_transition(None, previous_state)
                current_state = plus_state
            i += 1
            continue
        # Handle opening parenthesis '('
        elif char == '(':
            # Push the current state onto the stack
            state_stack.append(current_state)
            # Create a new group start state
            new_group_start = NFAState()
            current_state.define_transition(None, new_group_start)
            # Movews to the new group start state
            current_state = new_group_start 
            # Track group start states
            group_start_stack.append(new_group_start) 

        elif char == ')':
            if state_stack: 
                # Create a new group end state
                group_end_state = NFAState()
                # Pop the group start state from the stack
                group_start_state = state_stack.pop()
                # how the epsilon transition from the current state to the group
                current_state.define_transition(None, group_end_state)
                group_start_state.define_transition(None, current_state)
                # Moves to the new group end state
                current_state = group_end_state
            else:
                # standalone closing parenthesis
                new_state = NFAState(char)
                current_state.define_transition(char, new_state)
                current_state = new_state
            i += 1
        
        #handles characters followed by '+'
        elif i + 1 < len(regex) and regex[i + 1] == '+':
            # creates a new state for the character
            new_state = NFAState(char)
            current_state.define_transition(char, new_state)
            new_state.define_transition(None, current_state)
            current_state = new_state
            i += 2
            continue
        
        
        elif char == '$':
            current_state.define_transition(None, accept_state)

        elif char == '|':
            
            pass

        else:
            new_state = NFAState(char)
            current_state.define_transition(char, new_state)
            current_state = new_state

        i += 1
    # Connects the final state of the NFA to the accepting state
    if not state_stack:
        current_state.define_transition(None, accept_state)
    else:
        raise ValueError("Null")

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

    test_inputs = ["aba", "ab", 'sss']  #  TEST it here
    for test_input in test_inputs:
        result = "Accepted" if simulate_nfa(nfa, test_input) else "Rejected"
        print(f"Input: {test_input}, Result: {result}")

if __name__ == "__main__":
    main()