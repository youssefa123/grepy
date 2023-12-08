

# Testing Alphabet Learner 
Please cd grepy twice. So cd grepy..... cd grepy
Then to test the Alphabet Learner use the command: python src/alphabet_learner.py data/inputFile1.txt

It returns any number or alphabet letter from the inputFile1.txt. It then asks if you want to enter a word to find from that file and returns it. You can modify the file inputFile1.txt and test it using different words or find letters in a word. 

Heres an example:
youssefabdelhady@Youssefs-MBP grepy % python src/alphabet_learner.py data/inputFile1.txt

Alphabet: ['2', 'B', 'C', 'F', 'H', 'I', 'K', 'O', 'S', 'T', 'Y', 'a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u']
Enter a word to find: or
C[or]neliusTheC[or]n

# Testing NFA
To test the regex to NFA please go to the src directory and run python nfa.py to test the regex (0+1)*1 

From there you then convert the nfa to dfa by entering "python dfa" which will output the dot file and return if it accepts the strings or rejects from the inputFile2.txt.

To test the regex a+b*
Go to the src directory and run python nfa2.py
From there you then convert the nfa to dfa by entering "python dfa2.py" which will output the dot file and return if it accepts the strings or rejects from the inputFile3.txt.

