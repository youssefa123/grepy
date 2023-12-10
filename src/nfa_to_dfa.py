from regexTonfa import NFAState, regex_to_nfa, simulate_nfa

# DFA state class with epsilon closure and transitions.
class DFAState:
    def __init__(self, nfa_states):
        self.nfa_states = frozenset(nfa_states)  # store nfa states as a frozen set becuase the elements cannot be modified after created. This is good for making DFA's 
        self.is_final = any(state.final_state for state in self.nfa_states)  # Check if any NFA state is final
        self.transitions = {}  # transitions

    def add_transition(self, input_char, state):
        self.transitions[input_char] = state  # Add a transition to the state

    #  hash for state comparison
    def __hash__(self):
        return hash(self.nfa_states)  

     #equality for state comparison
    def __eq__(self, other):
        return self.nfa_states == other.nfa_states 


def nfa_to_dfa(start_state):
    
    initial_dfa_state = DFAState(start_state.compute_epsilon_closure())
    states = {initial_dfa_state}  # set to store DFA states
    unmarked_states = [initial_dfa_state]  # list with the initial state
    dfa = {}  #DFA structure as a dictionary

    while unmarked_states:
        current_dfa_state = unmarked_states.pop()  # Processes the current DFA state

        # Check if the current state includes the state reached after 'a'
        includes_state_after_a = any('a' in state.state_transitions for state in current_dfa_state.nfa_states)
        
        print(f"Processing DFA State: {current_dfa_state}")  

        for input_char in set(char for state in current_dfa_state.nfa_states for char in state.state_transitions if char is not None):
            next_nfa_states = set()
            for nfa_state in current_dfa_state.nfa_states:
                next_nfa_states.update(nfa_state.state_transitions.get(input_char, []))

            closure = set()
            for state in next_nfa_states:
                closure.update(state.compute_epsilon_closure())

            next_dfa_state = DFAState(closure)  # Create the next DFA state
            print(f"  On '{input_char}', Next DFA State: {next_dfa_state}, Closure: {closure}")  

            # Check if any state in the closure is final
            if any(state.final_state for state in closure):
                next_dfa_state.is_final = True
                print(f"    Marked as Final: {next_dfa_state.is_final}") 

            # Check if the next state is the same as the current state so self-loop
            if next_dfa_state == current_dfa_state:
                print(f"    Self-loop detected on '{input_char}'")  
                current_dfa_state.add_transition(input_char, current_dfa_state)
            else:
                if next_dfa_state not in states:
                    states.add(next_dfa_state)
                    unmarked_states.append(next_dfa_state)
                current_dfa_state.add_transition(input_char, next_dfa_state)

            dfa[current_dfa_state] = current_dfa_state.transitions  # Updates the DFA structure

   
    for dfa_state, transitions in dfa.items():
        print(f"DFA State: {dfa_state}, Transitions: {transitions}, Is Final: {dfa_state.is_final}")

    return dfa  
