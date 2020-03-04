A = 'A'
B = 'B'
percepts = []
table = {
    ((A, 'Clean'), ): 'Right',
    ((A, 'Dirty'), ): 'Suck',
    ((B, 'Clean'), ): 'Left',
    ((B, 'Dirty'), ): 'Suck',
    ((A, 'Clean'), (A, 'Clean')): 'Right',
    ((A, 'Clean'), (A, 'Dirty')): 'Suck',
    # ...
    ((A, 'Clean'), (A, 'Clean'), (A, 'Clean')): 'Right',
    ((A, 'Clean'), (A, 'Clean'), (A, 'Dirty')): 'Suck',
    ((A, 'Clean'), (A, 'Dirty'), (B, 'Clean')): 'Left',
    # ...
}

def LOOKUP(percepts, table):
    action = table.get(tuple(percepts))
    return action

def TABLE_DRIVEN_AGENT(percept):
    percepts.append(percept)
    action = LOOKUP(percepts, table)
    return action

def run():
    print("Actions")
    print(TABLE_DRIVEN_AGENT((A, "Clean")), "\t", percepts)
    print(TABLE_DRIVEN_AGENT((A, "Dirty")), "\t", percepts)
    print(TABLE_DRIVEN_AGENT((B, "Clean")), "\t", percepts)

run()

#It looks at the table and acts accordingly to it.
#Question 3: Just four entries for this agent, as there is only four actions to take. Meaning, as many entries as
#possible actions

#Question 4: For each step the complexity would increase in the power of 2. So T^2.