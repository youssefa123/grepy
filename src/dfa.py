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