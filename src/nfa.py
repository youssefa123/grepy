import re

class NFA:
    def __init__(self):
        self.transitions = []
        self.accept_states = set()
        self.start_state = 0

    def add_transition(self, start_state, input_char, end_state):
        while max(start_state, end_state) >= len(self.transitions):
            self.transitions.append({})
        if input_char in self.transitions[start_state]:
            self.transitions[start_state][input_char].add(end_state)
        else:
            self.transitions[start_state][input_char] = {end_state}

    def set_accept_state(self, state):
        self.accept_states.add(state)

    def is_accepted(self, input_string):
        current_states = {self.start_state}
        for char in input_string:
            next_states = set()
            for state in current_states:
                if char in self.transitions[state]:
                    next_states.update(self.transitions[state][char])
                if 'e' in self.transitions[state]:  # epsilon transitions
                    next_states.update(self.transitions[state]['e'])
            current_states = next_states
        return bool(self.accept_states & current_states)  # check for intersection with accept states

    def to_dot(self):
        
        pass

def regex_to_nfa(postfix):
    nfa = NFA()
    keys = list(set(re.sub('[^A-Za-z0-9]+', '', postfix) + 'e'))
    s = []
    stack = []
    start = 0
    end = 1
    counter = -1

    for i in postfix:
        if i in keys:
            counter += 2
            s.extend([{} for _ in range(counter - len(s) + 1)])
            stack.append([counter - 1, counter])
            s[counter - 1][i] = {counter}  # Wrap in a set
        elif i == '*':
            r1, r2 = stack.pop()
            counter += 2
            s.extend([{} for _ in range(counter - len(s) + 1)])
            stack.append([counter - 1, counter])
            s[r2]['e'] = {r1, counter}
            s[counter - 1]['e'] = {r1, counter}
            if start == r1:
                start = counter - 1
            if end == r2:
                end = counter
        elif i == '.':
            r11, r12 = stack.pop()
            r21, r22 = stack.pop()
            stack.append([r21, r12])
            s[r22]['e'] = {r11}
            if start == r11:
                start = r21
            if end == r22:
                end = r12
        else:  # This is the union case (e.g., '|')
            counter += 2
            s.extend([{} for _ in range(counter - len(s) + 1)])
            r11, r12 = stack.pop()
            r21, r22 = stack.pop()
            stack.append([counter - 1, counter])
            s[counter - 1]['e'] = {r21, r11}
            s[r12]['e'] = {counter}
            s[r22]['e'] = {counter}
            if start in {r11, r21}:
                start = counter - 1
            if end in {r22, r12}:
                end = counter

    # Load the transitions into the NFA object
    for idx, trans in enumerate(s):
        for input_char, end_states in trans.items():
            for end_state in end_states:
                nfa.add_transition(idx, input_char, end_state)
    
    nfa.set_accept_state(end)

    # Set start and accept states
    nfa.start_state = start
    nfa.accept_states = {end}

    return nfa


def process_file(file_path, regex):
    nfa = regex_to_nfa(regex)
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if nfa.is_accepted(line):
                print(f"Accepted: {line}")
            else:
                print(f"Rejected: {line}")

# Example usage
regex = input("Enter a regex: ")
process_file('../data/inputFile2.txt', regex)