from regexTonfa import regex_to_nfa, simulate_nfa
from nfa_todfa import regex_to_nfa as regex_to_nfa_dfa, nfa_to_dfa, simulate_dfa, generate_dot, epsilon_closure

def main():
    while True:
        regex = input("Enter a REGEX (or 'exit' to quit): ")

        if regex.lower() == 'exit':
            break

        nfa = regex_to_nfa(regex)
        print("Regex to NFA conversion completed.")
        
        test_strings_nfa = ["aba", "ab", "sss"]
        print("Testing NFA with example strings:")
        for test_input in test_strings_nfa:
            result = "Accepted" if simulate_nfa(nfa, test_input) else "Rejected"
            print(f"Input: {test_input}, Result: {result}")

        regex_dfa = input("Enter a REGEX to convert to DFA: ")
        
        nfa_start_state, _ = regex_to_nfa_dfa(regex_dfa)
        dfa_states = nfa_to_dfa(nfa_start_state)

        dot_output = generate_dot(dfa_states)
        dot_file_name = "dfa_graph.dot"
        with open(dot_file_name, "w") as file:
            file.write(dot_output)

        print(f"DOT file generated as '{dot_file_name}'.")

        start_closure = frozenset(nfa_start_state.compute_epsilon_closure())
        dfa_start_state = dfa_states[start_closure]

        test_strings_dfa = ["ab", "ba", "sss"]
        print("Testing DFA with example strings:")
        for test_input in test_strings_dfa:
            result = "Accepted" if simulate_dfa(dfa_start_state, test_input) else "Rejected"
            print(f"Test Input: '{test_input}', Result: {result}")

if __name__ == "__main__":
    main()
