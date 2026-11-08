
class DFA:
    def __init__(self, name, description, states, alphabet,
                 transitions, start_state, final_states):

        self.name = name
        self.description = description
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def simulate(self, input_string):

        current_state = self.start_state
        path = [current_state]

        for symbol in input_string:

            if symbol not in self.alphabet:
                return False, path, "Invalid input symbol"

            if (current_state, symbol) not in self.transitions:
                return False, path, "No transition defined"

            current_state = self.transitions[
                (current_state, symbol)
            ]

            path.append(current_state)

        if current_state in self.final_states:
            return True, path, "String Accepted"

        return False, path, "String Rejected"


# ---------------- DFA 1 ----------------
# Binary strings ending with 01

dfa1 = DFA(
    "DFA 1 - Ends with 01",
    "Binary strings ending with 01",
    {"q0", "q1", "q2"},
    {"0", "1"},
    {
        ("q0", "0"): "q1",
        ("q0", "1"): "q0",
        ("q1", "0"): "q1",
        ("q1", "1"): "q2",
        ("q2", "0"): "q1",
        ("q2", "1"): "q0"
    },
    "q0",
    {"q2"}
)


# ---------------- DFA 2 ----------------
# Even number of 1s

dfa2 = DFA(
    "DFA 2 - Even Number of 1s",
    "Strings containing an even number of 1s",
    {"A", "B"},
    {"0", "1"},
    {
        ("A", "0"): "A",
        ("A", "1"): "B",
        ("B", "0"): "B",
        ("B", "1"): "A"
    },
    "A",
    {"A"}
)


# ---------------- DFA 3 ----------------
# Binary strings starting with 1

dfa3 = DFA(
    "DFA 3 - Starts with 1",
    "Binary strings starting with 1",
    {"S", "A", "D"},
    {"0", "1"},
    {
        ("S", "0"): "D",
        ("S", "1"): "A",
        ("A", "0"): "A",
        ("A", "1"): "A",
        ("D", "0"): "D",
        ("D", "1"): "D"
    },
    "S",
    {"A"}
)


# ---------------- DFA 4 ----------------
# Contains substring 101

dfa4 = DFA(
    "DFA 4 - Contains 101",
    "Binary strings containing substring 101",
    {"q0", "q1", "q2", "q3"},
    {"0", "1"},
    {
        ("q0", "0"): "q0",
        ("q0", "1"): "q1",

        ("q1", "0"): "q2",
        ("q1", "1"): "q1",

        ("q2", "0"): "q0",
        ("q2", "1"): "q3",

        ("q3", "0"): "q3",
        ("q3", "1"): "q3"
    },
    "q0",
    {"q3"}
)


# ---------------- DFA 5 ----------------
# Binary numbers divisible by 3

dfa5 = DFA(
    "DFA 5 - Divisible by 3",
    "Binary numbers divisible by 3",
    {"R0", "R1", "R2"},
    {"0", "1"},
    {
        ("R0", "0"): "R0",
        ("R0", "1"): "R1",

        ("R1", "0"): "R2",
        ("R1", "1"): "R0",

        ("R2", "0"): "R1",
        ("R2", "1"): "R2"
    },
    "R0",
    {"R0"}
)


# ---------------- COLLECTION ----------------

DFA_LIST = {
    dfa1.name: dfa1,
    dfa2.name: dfa2,
    dfa3.name: dfa3,
    dfa4.name: dfa4,
    dfa5.name: dfa5
}
