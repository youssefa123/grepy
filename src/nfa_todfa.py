class NFAState:
    def __init__(self, final_state=False):
        self.final_state = final_state
        self.state_transitions = {}  # Maps characters to sets of states

    def define_transition(self, transition_chars, next_state):
        if transition_chars not in self.state_transitions:
            self.state_transitions[transition_chars] = set()
        self.state_transitions[transition_chars].add(next_state)


class DFAState:
    _id_counter = 0  # Counter for assigning unique IDs

    def __init__(self, is_final):
        self.id = DFAState._id_counter
        DFAState._id_counter += 1
        self.is_final = is_final
        self.transitions = {}

    def add_transition(self, input_char, state):
        self.transitions[input_char] = state


def epsilon_closure(nfa_state, visited=None):
    if visited is None:
        visited = set()

    closure = {nfa_state}
    if 'ε' in nfa_state.state_transitions:
        for next_state in nfa_state.state_transitions['ε']:
            if next_state not in visited:
                visited.add(next_state)
                closure.update(epsilon_closure(next_state, visited))

    return closure


def regex_to_nfa(regex):
    if not regex:
        raise ValueError("Empty regex is not allowed")

    def parse_subregex(subregex):
        start_state = NFAState()
        current_state = start_state

        stack = []
        i = 0
        while i < len(subregex):
            char = subregex[i]

            if char == '(':
                stack.append(current_state)
                count = 1
                j = i + 1
                while j < len(subregex) and count > 0:
                    if subregex[j] == '(':
                        count += 1
                    elif subregex[j] == ')':
                        count -= 1
                    j += 1

                if count != 0:
                    raise ValueError("Unbalanced parentheses in regex")

                nested_start, nested_end = parse_subregex(subregex[i + 1 : j - 1])
                current_state.define_transition('ε', nested_start)
                current_state = nested_end
                i = j - 1
            elif char == '[':
                # Handle two characters inside square brackets
                j = i + 1
                if j < len(subregex) and subregex[j] == '[':
                    j += 1  # Skip the opening square bracket
                    if j + 2 < len(subregex) and subregex[j + 2] == ']':
                        # Two characters inside square brackets
                        transition_chars = subregex[j:j + 2]
                        j += 3  # Skip the two characters and the closing square bracket
                    else:
                        raise ValueError("Invalid square bracket expression")
                else:
                    raise ValueError("Invalid square bracket expression")

                next_state = NFAState()
                current_state.define_transition(transition_chars, next_state)
                current_state = next_state
                i = j - 1
            else:
                next_state = NFAState()
                current_state.define_transition(char, next_state)
                current_state = next_state

            i += 1

        current_state.final_state = True
        while stack:
            prev_state = stack.pop()
            prev_state.define_transition('ε', current_state)

        return start_state, current_state

    return parse_subregex(regex)


def nfa_to_dfa(start_nfa_state):
    dfa_states = {}
    processed_states = set()
    start_closure = frozenset(epsilon_closure(start_nfa_state))
    unprocessed_states = [start_closure]

    while unprocessed_states:
        current_nfa_states = unprocessed_states.pop()
        if current_nfa_states in processed_states:
            continue

        is_final = any(state.final_state for state in current_nfa_states)
        dfa_state = DFAState(is_final)
        dfa_states[current_nfa_states] = dfa_state

        transitions = {}
        for nfa_state in current_nfa_states:
            for char, next_states in nfa_state.state_transitions.items():
                if char != 'ε':
                    for next_state in next_states:
                        next_states_set = frozenset(epsilon_closure(next_state))
                        if char not in transitions:
                            transitions[char] = set()
                        transitions[char].add(next_states_set)

        for char, next_states_sets in transitions.items():
            next_states_set = frozenset().union(*next_states_sets)
            if next_states_set not in dfa_states:
                unprocessed_states.append(next_states_set)
                is_final = any(state.final_state for state in next_states_set)
                new_dfa_state = DFAState(is_final)
                dfa_states[next_states_set] = new_dfa_state
            dfa_states[current_nfa_states].add_transition(char, dfa_states[next_states_set])

        processed_states.add(current_nfa_states)

    return dfa_states


def generate_dot(dfa_states):
    dot_output = "digraph DFA {\n"
    dot_output += "    rankdir=LR;\n"
    dot_output += "    size=\"9,5\"\n"
    dot_output += "    node [shape = doublecircle]; "

    for state in dfa_states.values():
        if state.is_final:
            dot_output += f" S{state.id} "

    dot_output += ";\n    node [shape = circle];\n"

    for state in dfa_states.values():
        for char, next_state in state.transitions.items():
            char_label = char if char not in ('(', ')') else f'"{char}"'
            dot_output += f"    S{state.id} -> S{next_state.id} [ label = \"{char_label}\" ];\n"

    dot_output += "}\n"
    return dot_output


def simulate_dfa(dfa_start_state, input_string):
    current_state = dfa_start_state
    for char in input_string:
        if char in current_state.transitions:
            current_state = current_state.transitions[char]
        else:
            return False  # No valid transition for this character

    return current_state.is_final  # Check if the final state is a valid end state


def main():
    regex = input("Enter a simple REGEX (like 'a', 'ab', '[ab]'): ")
    print(f"Building DFA for the regex: '{regex}'")

    # To handle (ab) as a literal string
    if regex.startswith("(") and regex.endswith(")"):
        regex = "\\" + regex

    nfa_start_state, _ = regex_to_nfa(regex)
    dfa_states = nfa_to_dfa(nfa_start_state)

    dot_output = generate_dot(dfa_states)
    dot_file_name = "dfa_graph.dot"
    with open(dot_file_name, "w") as file:
        file.write(dot_output)

    print(f"DOT file generated as '{dot_file_name}'.")

    start_closure = frozenset(epsilon_closure(nfa_start_state))
    dfa_start_state = dfa_states[start_closure]

    print("\nTesting the DFA with example inputs:")
    test_inputs = ["a", "ab", "b", "ba", "[ab]"]
    for test_input in test_inputs:
        result = "Accepted" if simulate_dfa(dfa_start_state, test_input) else "Rejected"
        print(f"Test Input: '{test_input}', Result: {result}")

if __name__ == "__main__":
    main()

