import numpy as np

"""
Hidden Markov Model using Viterbi algorithm to find most
likely sequence of hidden states.

The problem is to find out the most likely sequence of states
of the weather (hot, cold) from a describtion of the number
of ice cream eaten by a boy in the summer.
"""


def main():
    np.set_printoptions(suppress=True)

    states = np.array(["initial", "hot", "cold", "final"])

    # To simulate starting from index 1, we add a dummy value at index 0
    observationss = [
        [None, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    ]

    # Markov transition matrix
    # transitions[start, end]
    transitions = np.array([[.0, .8, .2, .0],  # Initial state
                            [.0, .6, .3, .1],  # Hot state
                            [.0, .4, .5, .1],  # Cold state
                            [.0, .0, .0, .0],  # Final state
                            ])

    # P(v|q)
    # emission[state, observation]
    emissions = np.array([[.0, .0, .0, .0],  # Initial state
                          [.0, .2, .4, .4],  # Hot state
                          [.0, .5, .4, .1],  # Cold state
                          [.0, .0, .0, .0],  # Final state
                          ])

    for observations in observationss:
        print("Observations: {}".format(' '.join(map(str, observations[1:]))))

        probability = compute_forward(states, observations, transitions, emissions)
        print("Probability: {}".format(probability))

        path = compute_viterbi(states, observations, transitions, emissions)
        #print(path)
        #print("Path: {}".format(' '.join(path)))

        print('')


def inclusive_range(a, b):
    return range(a, b + 1)


def compute_forward(states, observations, transitions, emissions):
    forward = np.empty(shape=(len(states)+1,len(observations)), dtype=object)
    # Initialization Step
    for s in range(0, len(states)):

        forward[s][0] = transitions[0][s] * emissions[s][observations[1]]
    # Recursion step
    for t in range(1, len(observations)):
        for s in range(0, len(states)):
            sum = 0
            for smark in range(0, len(states)):
                forwardval = forward[smark][t-1]
                transval = transitions[s][smark]
                emissionval = emissions[s][observations[t]]
                sum += forwardval * transval * emissionval
            forward[s][t] = sum
    # Termination Step
    probability = 0
    for s in range(0, len(states)):
        probability += forward[s][len(observations)-1] * transitions[s][len(transitions) - 1]
    return probability
def compute_viterbi(states, observations, transitions, emissions):

    viterbi = np.empty(shape=(len(states)+1,len(observations)), dtype=object)
    pathList = np.empty(shape=(len(states),len(observations)), dtype=object)
    # Initialization Step
    for s in range(0, len(states)):
        viterbi[s][0] = transitions[0][s] * emissions[s][observations[1]]
        pathList[s][0] = 0
    # Recursion step
    for t in range(1, len(observations)):
        for s in range(0, len(states)):
            list1 = list()
            for smark in range(0, len(states)):
                forwardval = viterbi[smark][t - 1]
                transval = transitions[smark][s]
                emissionval = emissions[s][observations[t]]
                list1.append(forwardval * transval * emissionval)
            viterbi[s][t] = max(list1)
            pathList[s][t] = argmax(list1)
    # Termination Step
    list2 = list()
    for s in range(0, len(states)):
        list2.append(viterbi[s][len(observations) - 1] * transitions[s][len(transitions) - 2])
    viterbi[s][t] = max(list2)
    pathList[s][t] = argmax(list2)
    return pathList


def argmax(sequence):
    # Note: You could use np.argmax(sequence), but only if sequence is a list.
    # If it is a generator, first convert it: np.argmax(list(sequence))
    return max(enumerate(sequence), key=lambda x: x[1])[0]


if __name__ == '__main__':
    main()
