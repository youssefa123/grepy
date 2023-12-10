

# Testing Alphabet Learner 
Please cd grepy twice. So cd grepy..... cd grepy
Then to test the Alphabet Learner use the command: python src/alphabet_learner.py data/inputFile1.txt

It returns any number or alphabet letter from the inputFile1.txt. It then asks if you want to enter a word to find from that file and returns it. You can modify the file inputFile1.txt and test it using different words or find letters in a word. 

Heres an example:
youssefabdelhady@Youssefs-MBP grepy % python src/alphabet_learner.py data/inputFile1.txt

Alphabet: ['2', 'B', 'C', 'F', 'H', 'I', 'K', 'O', 'S', 'T', 'Y', 'a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u']
Enter a word to find: or
C[or]neliusTheC[or]n

# Testing Regex to NFA 
Go to the src directory 
So cd grepy....cd grepy....cd src
run: python rungrepy.py

Enter a regex, and it will test the NFA and DFA with the inputFile2.txt strings. 

# From there it tests the NFA, converts the NFA to DFA and tests the data on the inputFile2.txt
And returns the dot format for DFA.

Example:
Enter a REGEX: ab

NFA Simulation Results:
Input: ab, Result: Accepted
Input: aabb, Result: Rejected
Input: aaaa, Result: Rejected
Input: aaabbaaa, Result: Rejected
DFA State: <nfa_to_dfa.DFAState object at 0x100c60310>, Transitions: {'a': <nfa_to_dfa.DFAState object at 0x100c602b0>}, Is Final: False
DFA State: <nfa_to_dfa.DFAState object at 0x100c60310>, Transitions: {'a': <nfa_to_dfa.DFAState object at 0x100c602b0>}, Is Final: False
DFA State: <nfa_to_dfa.DFAState object at 0x100c602b0>, Transitions: {'b': <nfa_to_dfa.DFAState object at 0x100c60250>}, Is Final: False

DFA Simulation Results:
Input: ab, Result: Accepted
Input: aabb, Result: Rejected
Input: aaaa, Result: Rejected
Input: aaabbaaa, Result: Rejected

DFA in DOT format:
digraph DFA {
    S0 [shape=circle];
    S0 -> S1 [label="a"];
    S1 [shape=circle];
    S1 -> S2 [label="b"];
}



