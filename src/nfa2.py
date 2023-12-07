from graphviz import Digraph

class NFA:
    def __init__(self):
        self.transitions = {}
        self.accept_states = set()

    def add_transition(self, start_state, input_char, end_state):
        if (start_state, input_char) not in self.transitions:
            self.transitions[(start_state, input_char)] = set()
        self.transitions[(start_state, input_char)].add(end_state)

    def set_accept_state(self, state):
        self.accept_states.add(state)

    def is_accepted(self, input_string):
        current_states = {0}
        for char in input_string:
            next_states = set()
            for state in current_states:
                if (state, char) in self.transitions:
                    next_states.update(self.transitions[(state, char)])
            current_states = next_states

        return bool(current_states & self.accept_states)
    
    #handle the Dot format Ouput 
    def to_dot(self):
        dot = Digraph()
        all_states = set()
        for (start_state, _), end_states in self.transitions.items():
            all_states.add(start_state)
            all_states.update(end_states)

        #Loop iterates over every state in the all states set
        # For each state it checks whether the state is an accepting state 
        for state in all_states:
           # If the current state is found in the  the self.accept_states it's an accepting state
            if state in self.accept_states:
                dot.node(str(state), shape="doublecircle")
            # If the current state isn't accepting state then it's a single circle without any destination
            else:
                dot.node(str(state))
        # Iterates over each transition in the NFA's transition table
        for (start_state, input_char), end_states in self.transitions.items():
            # For each transition it then iterate over the set of end states
            for end_state in end_states:
                 # creates an edge in the graphviz dot object from start state to each end state
                # The edge is labeled with the character that then triggers the transition in the NFA
                dot.edge(str(start_state), str(end_state), label=input_char)
        
        #After all the transitions are added then return the dot object which is the NFA 
        return dot


    



