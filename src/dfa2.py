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

    def is_accepted(self, input_string):
        #reset once we get to accepting state 
        self.reset()
        for char in input_string:
            self.transition(char)
        return self.current_state in self.accept_states
    
    def to_dot(self):
        dot = Digraph()
        # check every state in the DFA
        for state in self.transitions:
            # If the state is an accept state, represent it as a double circle, else represent it as a circle 
            shape = "doublecircle" if state in self.accept_states else "circle"
            dot.node(str(state), shape = shape)
            
            #transition between states in the DFA 
            for input_char, next_state in self.transitions[state].items():
                dot.edge(str(state), str(next_state), label=input_char)
        
        return dot
    
if __name__ == '__main__':
    dfa = DFA()

    # states for regex a+b*
    #Adding a dead state to fix error for accepting strings it shouldn't
    dfa.add_transition(0, 'a', 1)
    dfa.add_transition(1, 'a', 1)
    dfa.add_transition(1, 'b', 2)
    dfa.add_transition(2, 'b', 2)

    #dead state transition
    dfa.add_transition(0, 'b', 3) 
    dfa.add_transition(2, 'a', 3)
    dfa.add_transition(3, 'a', 3)
    dfa.add_transition(3, 'b', 3)

    dfa.set_accept_state(2)

    # Read the input file and test with DFA
    file_path = '../data/inputFile3.txt'
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            result = 'Accepted' if dfa.is_accepted(line) else 'Rejected'
            print(f"'{line}': {result}")

    # Output the DFA in DOT format
    dot = dfa.to_dot()
    output_path = '../output/dfa2_output'  
    dot.render(output_path, format='dot', view=False)
    print(f"The DOT representation has been saved to {output_path}.dot")
   
    