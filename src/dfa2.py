from graphviz import Digraph

class DFA:
    def __init__(self):
        self.transitions = {}
        self.current_state = 0
        self.accept_states = set()
        
    # define the transition logic
    def add_transition(self, state, input_char, next_state):
        if state not in self.transitions:
            self.transitions[state] = {}
        self.transitions[state][input_char] = next_state

    #define the accept state logic.
    def set_accept_state(self, state):
        self.accept_states.add(state)

    #resets the state to current 
    def reset(self):
        self.current_state = 0
   
    #Transition logic 
    def transition(self, input_char):
        if input_char in self.transitions[self.current_state]:
            self.current_state = self.transitions[self.current_state][input_char]