
from regexTonfa import NFAState, regex_to_nfa, simulate_nfa
from nfa_to_dfa import DFAState, nfa_to_dfa, simulate_dfa, generate_dot

def main():
    
    regex = input("Enter a REGEX: ")

    # NFA from regex
    nfa = regex_to_nfa(regex)

    
    with open('../data/inputFile2.txt', 'r') as file:
        test_inputs = [line.strip() for line in file]

    print("\nNFA Simulation Results:")
    for test_input in test_inputs:
        result = "Accepted" if simulate_nfa(nfa, test_input) else "Rejected"
        print(f"Input: {test_input}, Result: {result}")

    # Convert NFA to DFA
    dfa = nfa_to_dfa(nfa)

    print("\nDFA Simulation Results:")
    for test_input in test_inputs:
        result = "Accepted" if simulate_dfa(dfa, test_input) else "Rejected"
        print(f"Input: {test_input}, Result: {result}")

    
    dot_output = generate_dot(dfa)
    print("\nDFA in DOT format:")
    print(dot_output)

if __name__ == "__main__":
    main()
