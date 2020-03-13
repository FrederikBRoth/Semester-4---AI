A = "A"
B = "B"
C = "C"
D = "D"

state = {}
action = None
model = {A: None, B: None, C: None, D: None}

RULE_ACTION = {
    1: "Suck",
    2: "Left",
    3: "Right",
    4: "NoOp"
}

rules = {
    (A, "Dirty"): 1,
    (B, "Dirty"): 1,
    (C, "Dirty"): 1,
    (D, "Dirty"): 1,
    (A, "Clean"): 3,
    (B, "Clean"): 3,
    (C, "Clean"): 3,
    (D, "Clean"): 3,
    (A, B, C, D, "Clean"): 4
}

Environment = {
    A: "Dirty",
    B: "Dirty",
    C: "Dirty",
    D: "Dirty",
    "Current": C
}


def INTERPRET_INPUT(input):
    return input


def RULE_MATCH(state, rules):
    rule = rules.get(tuple(state))
    return rule


def UPDATE_STATE(state, action, percept):
    (location, status) = percept
    state = percept
    if model[A] == model[B] == model[C] == model[D] == "Clean":
        state = (A, B, C, D, "Clean")
    model[location] = status
    return state


def REFLEX_AGENT_WITH_STATE(percept):
    global state, action
    state = UPDATE_STATE(state, action, percept)
    rule = RULE_MATCH(state, rules)
    action = RULE_ACTION[rule]
    return action


def Sensors():
    location = Environment["Current"]
    return (location, Environment[location])


def Actuators(action):
    location = Environment["Current"]
    if action == "Suck":
        Environment[location] = "Clean"
    elif action == "Right" and location == A:
        Environment["Current"] = B
    elif action == "Right" and location == B:
        Environment["Current"] = C
    elif action == "Right" and location == C:
        Environment["Current"] = D
    elif action == "Right" and location == D:
        Environment["Current"] = A


def run(n):
    print("    Current                           New")
    print("location    status   action  location    status")
    for i in range(1, n):
        (location, status) = Sensors()
        print("{:12s}{:8s}".format(location, status), end="")
        action = REFLEX_AGENT_WITH_STATE(Sensors())
        Actuators(action)
        (location, status) = Sensors()
        print("{:12s}{:8s}{:12s}".format(action, location, status))


run(20)

# Question: It still works since its only if else based. The names doesnt matter it just works
