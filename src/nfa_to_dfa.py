class NFAState:
    def __init__(self, final_state=False):
        self.final_state = final_state
        self.state_transitions = {}

    def define_transition(self, transition_char, next_state):
        self.state_transitions[transition_char] = next_state

    def get_next_state(self, transition_char):
        return self.state_transitions.get(transition_char)
