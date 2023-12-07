from graphviz import Digraph

class DFA:
    def __init__(self):
        #States 
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.start_state = None
        self.accept_states = set()

    def add_states(self, state):
        self.states.add(state)

    def add_alphabet(self, symbol):
        self.alphabet.add(symbol)

    def add_transition(self, start_state, input_char, end_state):
        self.transitions[(start_state, input_char)] = end_state

    def set_start_state(self, state):
        self.start_state = state

    def set_accept_state(self, state):
        self.accept_states.add(state)

    def is_accepted(self, input_string):
        current_state = self.start_state
        for char in input_string:
            if (current_state, char) in self.transitions:
                current_state = self.transitions[(current_state, char)]
            else:
                return False  # If no transition exists for the input char, reject the string
        return current_state in self.accept_states
    
    